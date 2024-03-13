'''
A script to convert all HEC-DSS v6 files in a directory tree to HEC-DSS v7.

* Uses UI to select top-level directory and monitor operation
* Logs operations to log file
* Only HEC-DSS v6 files are altered
* HEC-DSS v6 files are renamed from *.dss to *.dss_v6
* The HEC-DSS v7 files are named the same as the original v6 files

Version history:
1.0     2024-03-13  MDP     Original version

Developers
MDP     Mike Perryman, USACE Hydrologic Engineering Center
'''
from hec.heclib.dss    import HecDSSUtilities
from hec.heclib.util   import Heclib
from java.awt          import Color
from java.awt          import Cursor
from java.awt          import Dimension
from java.awt          import Frame
from java.awt          import Toolkit
from java.io           import ByteArrayInputStream
from java.io           import File
from java.lang         import Exception as JavaException
from java.lang         import System
from java.nio.file     import Files
from java.nio.file     import Paths
from java.nio.file     import StandardCopyOption
from javax.swing       import JButton
from javax.swing       import JFileChooser
from javax.swing       import JFrame
from javax.swing       import JLabel
from javax.swing       import JProgressBar
from javax.swing       import JScrollPane
from javax.swing       import JTextArea
from javax.swing       import JTextField
from javax.swing       import JTree
from javax.swing       import SpringLayout
from javax.swing       import SwingWorker
from javax.swing       import Timer
from javax.swing       import UIManager
from javax.swing       import WindowConstants
from javax.swing.event import TreeWillExpandListener
from javax.swing.tree  import DefaultMutableTreeNode
from javax.swing.tree  import DefaultTreeCellRenderer
from javax.swing.tree  import DefaultTreeModel
from javax.swing.tree  import ExpandVetoException
import array, base64, copy, datetime, os, re, sys, threading, time, traceback

hms_pattern = re.compile(r"\s*(\d+)\s*hr\s*(\d+)\s*min\s*(\d+)\s*sec\s*", re.I)
var_pattern = re.compile(r"(%(\w+)%|\$(\w+)|\$\((\w+)\))")
center_on_x = None
center_on_y = None

class DssConverterFrame(JFrame):
    def __init__(self, title=None, gc=None):
        super(DssConverterFrame, self).__init__(title, gc)
        self._title = "DSS v6 to v7 Converter"
        self._width = 826
        self._height = 826
        self.logLock = threading.RLock()
        self.dss_files = []
        self.root = DefaultMutableTreeNode(os.sep)
        self.nodes = {os.sep : self.root}
        self.paths = {self.root : os.sep}
        self.rows = {}
        self.file_versions = {}
        self.file_sizes = {}
        self.files_to_convert = 0
        self.bytes_to_convert = 0
        self.top_level_dir = None
        self.conversion_done = False
        self.timer = Timer(1000, self.updateEta)
        self.program_name = "DssConverter"
        log_dir = System.getProperty("scripts.directory")
        if not log_dir :
            log_dir = System.getProperty("CWMS_HOME")
            if log_dir :
                log_dir = os.path.join(log_dir, "..", "HEC", "HEC-DSSVue", "scripts")
            else :
                log_dir = "."
        while True :
            m = var_pattern.search(log_dir)
            if not m : break
            if m.group(2) :
                log_dir = log_dir.replace(m.group(1), os.getenv(m.group(2)))
            elif m.group(3) :
                log_dir = log_dir.replace(m.group(1), os.getenv(m.group(3)))
            if m.group(4) :
                log_dir = log_dir.replace(m.group(1), os.getenv(m.group(4)))
        self.log_file_name = File(Paths.get(os.path.join(log_dir, "{}.log".format(self.program_name))).toString()).getCanonicalPath()
        self.dss_message_file = self.log_file_name.replace(".log", ".dssmsg.log")
        for i in range(5)[::-1] :
            p1 = Paths.get("{0}.{1}".format(self.log_file_name, i) if i > 0 else self.log_file_name)
            p2 = Paths.get("{0}.{1}".format(self.log_file_name, i+1))
            if Files.exists(p1) :
                Files.move(p1, p2, StandardCopyOption.REPLACE_EXISTING)
            p1 = Paths.get("{0}.{1}".format(self.dss_message_file, i) if i > 0 else self.log_file_name)
            p2 = Paths.get("{0}.{1}".format(self.dss_message_file, i+1))
            if Files.exists(p1) :
                Files.move(p1, p2, StandardCopyOption.REPLACE_EXISTING)
        self.initComponents()

    def initComponents(self):
        self.setPreferredSize(Dimension(self._width, self._height))
        self.setResizable(False)
        if center_on_x :
            # center on ListSelection window
            self.setLocation(max(0, center_on_x - self._width / 2), max(0, center_on_y - self._height / 2))
        else :
            # center on primary screen
            screen_size = Toolkit.getDefaultToolkit().getScreenSize()
            self.setLocation(max(0, (screen_size.width - self._width) / 2), max(0, (screen_size.height - self._height) / 2))
        self.setDefaultCloseOperation(WindowConstants.DO_NOTHING_ON_CLOSE)
        self.setTitle(self._title)
        springLayout = SpringLayout()
        self.getContentPane().setLayout(springLayout)
        
        lblTopLevelDir = JLabel("Top Level Directory")
        springLayout.putConstraint(SpringLayout.NORTH, lblTopLevelDir, 10, SpringLayout.NORTH, self.getContentPane())
        springLayout.putConstraint(SpringLayout.WEST, lblTopLevelDir, 10, SpringLayout.WEST, self.getContentPane())
        self.getContentPane().add(lblTopLevelDir)
        
        self.tfTopLevelDir = JTextField()
        self.tfTopLevelDir.setEditable(False)
        self.tfTopLevelDir.setColumns(10)
        springLayout.putConstraint(SpringLayout.NORTH, self.tfTopLevelDir, -4, SpringLayout.NORTH, lblTopLevelDir)
        springLayout.putConstraint(SpringLayout.WEST, self.tfTopLevelDir, 6, SpringLayout.EAST, lblTopLevelDir)
        springLayout.putConstraint(SpringLayout.EAST, self.tfTopLevelDir, 450, SpringLayout.EAST, lblTopLevelDir)
        self.getContentPane().add(self.tfTopLevelDir)

        lblV6DssFile = JLabel("Version 6 DSS file")
        lblV6DssFile.setForeground(Color.RED)
        springLayout.putConstraint(SpringLayout.NORTH, lblV6DssFile, 10, SpringLayout.SOUTH, lblTopLevelDir)
        springLayout.putConstraint(SpringLayout.WEST, lblV6DssFile, 0, SpringLayout.WEST, lblTopLevelDir)
        self.getContentPane().add(lblV6DssFile)

        lblV7DssFile = JLabel("Version 7 DSS file")
        lblV7DssFile.setForeground(Color.BLUE)
        springLayout.putConstraint(SpringLayout.NORTH, lblV7DssFile, 2, SpringLayout.SOUTH, lblV6DssFile)
        springLayout.putConstraint(SpringLayout.WEST, lblV7DssFile, 0, SpringLayout.WEST, lblV6DssFile)
        self.getContentPane().add(lblV7DssFile)
        
        self.tree = JTree(self.root)
        self.tree.addTreeWillExpandListener(CustomTreeWillExpandListener())
        self.tree_cell_renderer = CustomTreeCellRenderer()
        self.tree.setCellRenderer(self.tree_cell_renderer)
        self.treeScrollPane = JScrollPane(self.tree)
        springLayout.putConstraint(SpringLayout.NORTH, self.treeScrollPane, 2, SpringLayout.SOUTH, lblV7DssFile)
        springLayout.putConstraint(SpringLayout.SOUTH, self.treeScrollPane, 506, SpringLayout.NORTH, self.getContentPane())
        springLayout.putConstraint(SpringLayout.WEST, self.treeScrollPane, 10, SpringLayout.WEST, self.getContentPane())
        springLayout.putConstraint(SpringLayout.EAST, self.treeScrollPane, 0, SpringLayout.EAST, self.tfTopLevelDir)
        self.getContentPane().add(self.treeScrollPane)
        
        lblLogFileName = JLabel("Log file: {}".format(self.log_file_name))
        springLayout.putConstraint(SpringLayout.NORTH, lblLogFileName, 10, SpringLayout.SOUTH, self.treeScrollPane)
        springLayout.putConstraint(SpringLayout.WEST, lblLogFileName, 0, SpringLayout.WEST, self.treeScrollPane)
        self.getContentPane().add(lblLogFileName)
        
        self.taLog = JTextArea()
        self.taLog.setEditable(False)
        self.logScrollPane = JScrollPane(self.taLog)
        springLayout.putConstraint(SpringLayout.NORTH, self.logScrollPane, 10, SpringLayout.SOUTH, lblLogFileName)
        springLayout.putConstraint(SpringLayout.WEST, self.logScrollPane, 0, SpringLayout.WEST, self.treeScrollPane)
        springLayout.putConstraint(SpringLayout.SOUTH, self.logScrollPane, 200, SpringLayout.SOUTH, self.treeScrollPane)
        springLayout.putConstraint(SpringLayout.EAST, self.logScrollPane, 802, SpringLayout.WEST, self.getContentPane())
        self.getContentPane().add(self.logScrollPane)
        
        lblFiles = JLabel("Files")
        springLayout.putConstraint(SpringLayout.NORTH, lblFiles, 10, SpringLayout.SOUTH, self.logScrollPane)
        springLayout.putConstraint(SpringLayout.WEST, lblFiles, 0, SpringLayout.WEST, self.logScrollPane)
        self.getContentPane().add(lblFiles)
        
        self.pbFiles = JProgressBar()
        springLayout.putConstraint(SpringLayout.NORTH, self.pbFiles, 0, SpringLayout.NORTH, lblFiles)
        springLayout.putConstraint(SpringLayout.WEST, self.pbFiles, 12, SpringLayout.EAST, lblFiles)
        springLayout.putConstraint(SpringLayout.SOUTH, self.pbFiles, 0, SpringLayout.SOUTH, lblFiles)
        springLayout.putConstraint(SpringLayout.EAST, self.pbFiles, 224, SpringLayout.EAST, lblFiles)
        self.getContentPane().add(self.pbFiles)
        
        lblBytes = JLabel("Bytes")
        springLayout.putConstraint(SpringLayout.NORTH, lblBytes, 10, SpringLayout.SOUTH, lblFiles)
        springLayout.putConstraint(SpringLayout.WEST, lblBytes, 10, SpringLayout.WEST, self.getContentPane())
        self.getContentPane().add(lblBytes)
        
        self.pbBytes = JProgressBar()
        springLayout.putConstraint(SpringLayout.NORTH, self.pbBytes, 0, SpringLayout.NORTH, lblBytes)
        springLayout.putConstraint(SpringLayout.WEST, self.pbBytes, 6, SpringLayout.EAST, lblBytes)
        springLayout.putConstraint(SpringLayout.SOUTH, self.pbBytes, 0, SpringLayout.SOUTH, lblBytes)
        springLayout.putConstraint(SpringLayout.EAST, self.pbBytes, 0, SpringLayout.EAST, self.pbFiles)
        self.getContentPane().add(self.pbBytes)
        
        self.lblFilesCount = JLabel("000000 / 000000")
        springLayout.putConstraint(SpringLayout.NORTH, self.lblFilesCount, 0, SpringLayout.NORTH, lblFiles)
        springLayout.putConstraint(SpringLayout.WEST, self.lblFilesCount, 6, SpringLayout.EAST, self.pbFiles)
        springLayout.putConstraint(SpringLayout.EAST, self.lblFilesCount, 110, SpringLayout.EAST, self.pbFiles)
        self.getContentPane().add(self.lblFilesCount)
        self.lblFilesCount.setText("")
        
        self.lblBytesCount = JLabel("000.00 MB / 000.00 MB")
        springLayout.putConstraint(SpringLayout.NORTH, self.lblBytesCount, 0, SpringLayout.NORTH, lblBytes)
        springLayout.putConstraint(SpringLayout.WEST, self.lblBytesCount, 6, SpringLayout.EAST, self.pbBytes)
        springLayout.putConstraint(SpringLayout.SOUTH, self.lblBytesCount, 0, SpringLayout.SOUTH, lblBytes)
        springLayout.putConstraint(SpringLayout.EAST, self.lblBytesCount, 0, SpringLayout.EAST, self.lblFilesCount)
        self.getContentPane().add(self.lblBytesCount)
        self.lblBytesCount.setText("")
        
        lblEta = JLabel("ETA")
        springLayout.putConstraint(SpringLayout.NORTH, lblEta, 10, SpringLayout.SOUTH, lblBytes)
        springLayout.putConstraint(SpringLayout.WEST, lblEta, 10, SpringLayout.WEST, self.getContentPane())
        self.getContentPane().add(lblEta)
        
        self.lblEtaValue = JLabel("0 hrs 00 min 00 sec")
        springLayout.putConstraint(SpringLayout.NORTH, self.lblEtaValue, 0, SpringLayout.NORTH, lblEta)
        springLayout.putConstraint(SpringLayout.WEST, self.lblEtaValue, 0, SpringLayout.WEST, self.pbFiles)
        springLayout.putConstraint(SpringLayout.SOUTH, self.lblEtaValue, 0, SpringLayout.SOUTH, lblEta)
        springLayout.putConstraint(SpringLayout.EAST, self.lblEtaValue, 120, SpringLayout.WEST, self.pbFiles)
        self.getContentPane().add(self.lblEtaValue)
        self.lblEtaValue.setText("")
        
        self.btnChooseDir = JButton("Choose Directory")
        self.btnChooseDir.addActionListener(self.chooseTopLevelDir)
        springLayout.putConstraint(SpringLayout.NORTH, self.btnChooseDir, 180, SpringLayout.NORTH, self.getContentPane())
        springLayout.putConstraint(SpringLayout.WEST, self.btnChooseDir, 50, SpringLayout.EAST, self.treeScrollPane)
        springLayout.putConstraint(SpringLayout.EAST, self.btnChooseDir, 200, SpringLayout.EAST, self.treeScrollPane)
        self.getContentPane().add(self.btnChooseDir)
        
        self.btnStart = JButton("Start")
        self.btnStart.addActionListener(self.startFileConversion)
        springLayout.putConstraint(SpringLayout.NORTH, self.btnStart, 54, SpringLayout.SOUTH, self.btnChooseDir)
        springLayout.putConstraint(SpringLayout.WEST, self.btnStart, 0, SpringLayout.WEST, self.btnChooseDir)
        springLayout.putConstraint(SpringLayout.EAST, self.btnStart, 0, SpringLayout.EAST, self.btnChooseDir)
        self.getContentPane().add(self.btnStart)
        
        self.btnExitCancel = JButton("Exit")
        self.btnExitCancel.addActionListener(self.exitOrCancel)
        springLayout.putConstraint(SpringLayout.NORTH, self.btnExitCancel, 54, SpringLayout.SOUTH, self.btnStart)
        springLayout.putConstraint(SpringLayout.WEST, self.btnExitCancel, 0, SpringLayout.WEST, self.btnChooseDir)
        springLayout.putConstraint(SpringLayout.EAST, self.btnExitCancel, 0, SpringLayout.EAST, self.btnChooseDir)
        self.getContentPane().add(self.btnExitCancel)
        
        self.treeScrollPane.updateUI()

    def log(self, message) :
        with self.logLock :
            prefix1 = str(datetime.datetime.now())[:19]
            prefix2 = 19 * " "
            lines = message.rstrip().split("\n")
            with open(self.log_file_name, "a") as log_file :
                for i in range(len(lines)) :
                    line = "{0} : {1}\n".format(prefix1 if i == 0 else prefix2, lines[i])
                    self.taLog.append(line)
                    log_file.write(line)
            self.taLog.setCaretPosition(self.taLog.getDocument().getLength())

    def addDssFiles(self, dss_files) :
        self.dss_files = dss_files[:]
        Heclib.zset("MLVL", "", 0)
        ifltab = array.array('i', 800*[0])
        status = [0]
        for dss_file in dss_files :
            Heclib.zopen(ifltab, dss_file, status)
            dss_version = ifltab[0]
            Heclib.zclose(ifltab)
            self.file_versions[dss_file] = dss_version
            if dss_version == 6 :
                self.files_to_convert += 1
            self.log("Added v{0} DSS file {1}".format(dss_version, dss_file))
            node = self.root
            parts = dss_file.split(os.sep)
            for i in range(len(parts)+1) :
                path = os.sep + os.sep.join(parts[:i])
                if path not in self.nodes :
                    new_node = DefaultMutableTreeNode(parts[i-1])
                    node.add(new_node)
                    self.nodes[path] = new_node
                    self.paths[new_node] = path
                    node = new_node
                else :
                    node = self.nodes[path]
        self.tree.updateUI()
        self.expandAllTreeRows()
        for row in range(self.tree.getRowCount()) :
            path = self.tree.getPathForRow(row).getPath()
            file_path = os.sep.join(map(str, path[1:]))
            if file_path.endswith(".dss") :
                self.rows[file_path] = row
                size = os.stat(file_path).st_size
                self.file_sizes[file_path] = size
                size_str = formatByteCount(size)
                node = self.nodes[os.sep+file_path]
                node.setUserObject("{0} ({1})".format(str(node.getUserObject()), size_str))
                self.tree_cell_renderer.setRowVersion(self.rows[file_path], self.file_versions[file_path])
                if self.file_versions[file_path] == 6 :
                    self.bytes_to_convert += size
        self.total_bytes_to_convert = self.bytes_to_convert
        self.tree.updateUI()
        self.log("{0} files added from {1}".format(len(dss_files), self.top_level_dir))
        self.log("{0} in {1} v6 HEC-DSS files to convert".format(formatByteCount(self.bytes_to_convert), self.files_to_convert))
        self.lblFilesCount.setText("0 / {}".format(self.files_to_convert))
        self.lblBytesCount.setText("0 B / {}".format(formatByteCount(self.bytes_to_convert)))
        self.pbFiles.setMinimum(0)
        self.pbFiles.setMaximum(self.files_to_convert)
        self.pbFiles.setValue(0)
        self.pbBytes.setMinimum(0)
        self.pbBytes.setMaximum(100)
        self.pbBytes.setValue(0)
        self.btnStart.setEnabled(self.bytes_to_convert > 0)

    def setDssFileVersionInTree(self, dss_file, version, update_view=True) :
        row = self.rows[dss_file]
        self.tree_cell_renderer.setRowVersion(row, version)
        if update_view :
            self.tree.scrollRowToVisible(row)
            self.tree.setSelectionRow(row)

    def expandAllTreeRows(self) :
        last_row_count = self.tree.getRowCount()
        row_count = last_row_count
        while True :
            for i in range(row_count) :
                self.tree.expandRow(i)
            row_count = self.tree.getRowCount()
            if row_count == last_row_count :
                break
            last_row_count = row_count
        self.tree.updateUI()

    def chooseTopLevelDir(self, e):
        self.setCursor(Cursor(Cursor.WAIT_CURSOR))
        self.btnChooseDir.setEnabled(False)
        self.btnStart.setEnabled(False)
        self.btnExitCancel.setEnabled(False)
        chooser = DirectoryChooser(self.top_level_dir)
        self.top_level_dir = chooser.chooseDirectory(self)
        chooser.dispose()
        del(chooser)
        if self.top_level_dir :
            self.log("Selected top level directory {}".format(self.top_level_dir))
            if os.path.isdir(self.top_level_dir) :
                self.dss_files = []
                self.root = DefaultMutableTreeNode(os.sep)
                self.nodes = {os.sep : self.root}
                self.paths = {self.root : os.sep}
                self.rows = {}
                self.file_versions = {}
                self.file_sizes = {}
                self.files_to_convert = 0
                self.bytes_to_convert = 0
                self.tree.setModel(DefaultTreeModel(self.root))
                self.tree_cell_renderer.resetRowVersions()
                self.tfTopLevelDir.setText(self.top_level_dir)
                self.addDssFiles(find_dss_files(self.top_level_dir))
            else :
                self.log("ERROR - no such directory : {}".format(self.top_level_dir))
                self.top_level_dir = None
        self.btnChooseDir.setEnabled(True)
        self.btnExitCancel.setEnabled(True)
        self.setCursor(Cursor(Cursor.DEFAULT_CURSOR))

    def exitOrCancel(self, e):
        if self.btnExitCancel.getText() == "Cancel" :
            self.cancelConversion = True
            self.log("Canceling conversion...")
            self.btnExitCancel.setText("Waiting...")
            self.btnExitCancel.setEnabled(False)
            self.lblEtaValue.setText("")
        else :
            do_exit = True
            for frame in Frame.getFrames() :
                if frame.__class__.__name__ not in ("DirectoryChooser",) :
                    do_exit = False
                    break
            if do_exit :
                System.exit(0)
            self.dispose()
            
    def isCanceled(self) :
        return self.cancelConversion
        
    def getFilesToConvert(self) :
        return self.files_to_convert
        
    def getBytesToConvert(self) :
        return self.bytes_to_convert
        
    def getDssFiles(self) :
        return self.dss_files[:]
        
    def getFileSizes(self) :
        return copy.deepcopy(self.file_sizes);
        
    def getFileVersions(self) :
        return copy.deepcopy(self.file_versions)
        
    def getDssMessageFile(self) :
        return self.dss_message_file

    def startFileConversion(self, e):
        self.conversion_done = False
        self.btnChooseDir.setEnabled(False)
        self.btnStart.setEnabled(False)
        self.btnExitCancel.setText("Cancel")
        self.cancelConversion = False
        self.log("Starting conversion")
        self.timer.start()
        self.converter = BackgroundFileConverter(self)
        self.converter.execute()
        
    def conversionDone(self, start_time) :
        del self.converter
        self.converter = None
        self.conversion_done = True
        self.timer.stop()
        self.btnChooseDir.setEnabled(True)
        self.btnExitCancel.setText("Exit")
        self.btnExitCancel.setEnabled(True)
        self.lblEtaValue.setText("")
        elapsed = secsToHms((datetime.datetime.now() - start_time).total_seconds())
        if self.isCanceled() :
            self.log("Convesrion canceled after {}".format(elapsed))
        else :
            self.log("Convesrion completed: {0} in {1}".format(formatByteCount(self.total_bytes_to_convert), elapsed))

    def updateEta(self, e):
        secs = hmsToSecs(self.lblEtaValue.getText())
        if secs :
            self.updateEtaLabel(secs - 1)
        else :
            self.updateEtaLabel(None)
            
    def updateEtaLabel(self, secs) :
        if self.conversion_done :
            self.lblEtaValue.setText("")
        elif secs :
            self.lblEtaValue.setText(secsToHms(secs))
        else :
            self.lblEtaValue.setText("Calculating {}".format("." * (int(time.time()) % 4)))
            
    def updateStatus(self, start_time, dss_file, files_converted, bytes_converted) :
        try :
            elapsed = (datetime.datetime.now() - start_time).total_seconds()
            fraction = (float(bytes_converted) / self.bytes_to_convert)
            percent_complete = 100 * fraction
            self.setDssFileVersionInTree(dss_file, 7)
            self.file_versions[dss_file] = 7
            self.pbFiles.setValue(files_converted)
            self.lblFilesCount.setText("{0} / {1}".format(files_converted, self.files_to_convert))
            self.pbBytes.setValue(int(percent_complete))
            self.lblBytesCount.setText("{0} / {1}".format(formatByteCount(bytes_converted), formatByteCount(self.bytes_to_convert)))
            self.setTitle("{0} - {1}%".format(self._title, int(percent_complete)))
            if percent_complete >= 2.0 :
                estimated_total_secs = elapsed / (fraction ** 2.0) # try to prevent optimistic early estimates
                estimated_remaining_secs = estimated_total_secs - elapsed
                self.updateEtaLabel(estimated_remaining_secs)
            else :
                self.updateEtaLabel(None)
        except :
            traceback.print_exc()

class BackgroundFileConverter(SwingWorker) :
    '''
    SwingWorker to do conversion in background
    '''
    def __init__(self, converterFrame) :
        try :
            self.converter = converterFrame
            self.files_converted = 0
            self.files_to_convert = self.converter.getFilesToConvert()
            self.bytes_converted = 0
            self.bytes_to_convert = self.converter.getBytesToConvert()
            self.dss_files = self.converter.getDssFiles()
            self.file_sizes = self.converter.getFileSizes()
            self.file_versions = self.converter.getFileVersions()
            self.percent_complete = 0
            self.v6_ext1 = ".v6.dss"
            self.v6_ext2 = ".dss_v6"
            self.dss_message_file = self.converter.getDssMessageFile()
            self.util = HecDSSUtilities()
            Files.deleteIfExists(Paths.get(self.dss_message_file))
        except :
            traceback.print_exc()

    def publish(self, chunk) :
        super(BackgroundFileConverter, self).publish(chunk)

    def setProgress(self, percent) :
        super(BackgroundFileConverter, self).setProgress(percent)

    def doInBackground(self) :
        self.start_time = datetime.datetime.now()
        for dss_file in self.dss_files :
            if self.converter.isCanceled() : 
                super(BackgroundFileConverter, self).setProgress(100)
                break
            if self.file_versions[dss_file] == 6 :
                try :
                    dir_name = os.path.split(dss_file)[0]
                    v6_file = dss_file.replace(".dss", self.v6_ext1)
                    self.publish("\t".join(["START", str(time.time()), dss_file, v6_file]))
                    Files.move(
                        Paths.get(dss_file),
                        Paths.get(v6_file),
                        StandardCopyOption.REPLACE_EXISTING)
                    self.util.setMessageFile(self.dss_message_file)
                    self.util.setDSSFileName(v6_file)
                    self.util.convertVersion(dss_file)
                    self.util.close()
                    self.files_converted += 1
                    self.bytes_converted += self.file_sizes[dss_file]
                    self.publish("\t".join(["END", str(time.time()), dss_file, v6_file]))
                    self.setProgress(100 * self.bytes_converted // self.bytes_to_convert)
                    Files.move(
                        Paths.get(v6_file),
                        Paths.get(v6_file.replace(self.v6_ext1, self.v6_ext2)),
                        StandardCopyOption.REPLACE_EXISTING)
                except :
                    traceback.print_exc()

    def process(self, chunks) :
        for chunk in chunks :
            status, time_val, dss_file, v6_file = chunk.split("\t")
            try :
                if status == "START" :
                    self.start_secs = float(time_val)
                    self.converter.setDssFileVersionInTree(dss_file, 6)
                    self.converter.log("Starting conversion of {}".format(dss_file))
                    self.converter.log("    renaming original file to {}".format(os.path.split(v6_file)[1]))
                    self.converter.log("    converting into {}".format(os.path.split(dss_file)[1]))
                elif status == "END" :
                    self.converter.log("    renaming {} to {}".format(
                        os.path.split(v6_file)[1],
                        os.path.split(v6_file.replace(self.v6_ext1, self.v6_ext2))[1]))
                    self.converter.log("    {0} converted in {1}".format(
                        formatByteCount(self.file_sizes[dss_file]),
                        secsToHms(float(time_val) - self.start_secs)))
                    self.converter.updateStatus(self.start_time, dss_file, self.files_converted, self.bytes_converted)
            except :
                self.converter.log(traceback.format_exc())

    def done(self) :
        self.util.flushMessageFile()
        self.util.closeMessageFile()
        del self.util
        self.converter.conversionDone(self.start_time)

class DirectoryChooser(JFrame):
    '''
    A simple Swing-based UI to select a top-level directory.
    '''
    def __init__(self, initial_directory=None):
        '''
        Init the directory chooser dialog
        '''
        super(DirectoryChooser, self).__init__()
        if initial_directory :
            self.fileChooser = JFileChooser(initial_directory)
        else :
            self.fileChooser = JFileChooser()
        self.fileChooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY)

    def chooseDirectory(self, parent) :
        '''
        Choose and return a top level directory
        '''
        selectedDirectory = None
        ret = self.fileChooser.showDialog(parent, "Select Top Level Directory")
        if ret == JFileChooser.APPROVE_OPTION:
            selectedDirectory = self.fileChooser.getSelectedFile().getAbsolutePath()
        return selectedDirectory

class CustomTreeWillExpandListener(TreeWillExpandListener) :
    '''
    Class to prevent user from collapsing tree nodes
    '''
    def treeWillExpand(selv, event) :
        pass

    def treeWillCollapse(self, event) :
        raise ExpandVetoException(event)

class CustomTreeCellRenderer(DefaultTreeCellRenderer):
    '''
    Custom renderer for the tree pane
    '''
    def __init__(self) :
        self.resetRowVersions()

    def resetRowVersions(self) :
        self.v6_files = set()
        self.v7_files = set()
        
    def setRowVersion(self, row, version) :
        if version == 6 :
            if row in self.v7_files : self.v7_files.remove(row)
            self.v6_files.add(row)
        elif version == 7 :
            if row in self.v6_files : self.v6_files.remove(row)
            self.v7_files.add(row)

    def getPreferredSize(self):
        preferredSize = super(CustomTreeCellRenderer, self).getPreferredSize()
        preferredSize.width += 100  # Add additional width to prevent truncation
        return preferredSize

    def getTreeCellRendererComponent(self, tree, value, selected, expanded, leaf, row, hasFocus):
        c = super(CustomTreeCellRenderer, self).getTreeCellRendererComponent(tree, value, selected, expanded, leaf, row, hasFocus)

        if row in self.v6_files :
            c.setForeground(Color.RED)
        elif row in self.v7_files :
            c.setForeground(Color.BLUE)
        else:
            c.setForeground(Color.BLACK)
        return c

def secsToHms(secs) :
    secs = int(secs)
    hrs  = int(secs / 3600)
    mins = int((secs - 3600 * hrs) / 60)
    secs = secs - 3600 * hrs - 60 * mins
    return "{0} hr {1:02d} min {2:02d} sec".format(hrs, mins, secs)

def hmsToSecs(hms) :
    m = hms_pattern.match(hms)
    if m :
        secs = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
        return secs
    else :
        return None

def formatByteCount(size) :
    if size >= 1e9 :
        size_str = "{0:.2f} GB".format(size / 1.0e9)
    elif size >= 1e6 :
        size_str = "{0:.2f} MB".format(size / 1.0e6)
    elif size >= 1e3 :
        size_str = "{0:.2f} KB".format(size / 1.0e3)
    else :
        size_str = "{0} B".format(size)
    return size_str

def find_dss_files(directory):
    '''
    Find all *.dss files in the given directory
    '''
    dss_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".dss"):
                pathname = os.path.join(root, file)
                dss_files.append(pathname)
    return dss_files

def main() :
    global center_on_x, center_on_y
    UIManager.setLookAndFeel("com.sun.java.swing.plaf.windows.WindowsLookAndFeel")
    for frame in Frame.getFrames() :
        if frame.__class__.__name__ in("ListSelection", "CwmsListSelection") :
            loc = frame.getLocationOnScreen()
            siz = frame.getSize()
            center_on_x = loc.x + siz.width / 2
            center_on_y = loc.y + siz.height / 2
            break;
    window = DssConverterFrame()
    window.pack()
    window.setVisible(True)
    window.chooseTopLevelDir(None)

if __name__ == "__main__":
    threading.Thread(target=main).start()