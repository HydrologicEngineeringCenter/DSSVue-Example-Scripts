'''
A script to convert all HEC-DSS v6 files in a directory tree to HEC-DSS v7.

* Uses UI to select top-level directory and monitor operation
* Logs operations to log file
* Only HEC-DSS v6 files are altered
* HEC-DSS v6 files are renamed from *.dss to *.dss_v6
* The HEC-DSS v7 files are named the same as the original v6 files

Version history:
1.0     2024-03-13  MDP     Original version
1.1     2024-07-05  MDP     Improved interaction with CAVI
                            Move v6 files to archive directory
                            Allow closing via "X" window
                            Change log file naming
                            Use application-specific log directory
                            Put log files on menu
                              - CAVI: Tools->Logs
                              - CWMS-VUE, DSSVue: Advanced->Output

Developers
MDP     Mike Perryman, USACE Hydrologic Engineering Center
'''
from hec.heclib.dss    import HecDSSUtilities
from hec.heclib.util   import Heclib
from hec.io            import Identifier
from hec.io            import SimpleFile
from java.awt          import Color
from java.awt          import Cursor
from java.awt          import Dimension
from java.awt          import Frame
from java.awt          import Toolkit
from java.awt.event    import ActionListener
from java.awt.event    import WindowAdapter
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
from javax.swing       import JMenuItem
from javax.swing       import JOptionPane
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
import array, copy, datetime, os, re, threading, time, traceback

try :
    from com.rma.editors import TextEditorDialog
    use_TextEditorDialog = True
except ImportError :
    from hec.util import TextDialog
    use_TextEditorDialog = False

hms_pattern = re.compile(r"\s*(\d+)\s*hr\s*(\d+)\s*min\s*(\d+)\s*sec\s*", re.I)
var_pattern = re.compile(r"(%(\w+)%|\$(\w+)|\$\((\w+)\))")
center_on_x = None
center_on_y = None

class DssConverterFrame(JFrame, ActionListener):
    '''
    GUI class to perform the work
    '''
    class MyWindowAdapter(WindowAdapter) :
        '''
        A WindowAdapter subclass to handle window closing events
        '''
        def __init__(self, dialog) :
            self.dialog = dialog

        def windowClosing(self, e) :
            self.dialog.onClose(e)

    def __init__(self, title=None, gc=None):
        '''
        Constructor
        '''
        super(DssConverterFrame, self).__init__(title, gc)
        self._title = "DSS v6 to v7 Converter"
        self._width = 830
        self._height = 830
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
        self.top_level_source_dir = None
        self.top_level_archive_dir = None
        self.conversion_done = False
        self.timer = Timer(1000, self.updateEta)
        self.exit_when_canceled = False
        self.program_name = "DssConverter"
        self.application_frame = None
        self.logs_menu = None
        self.logfiles = {}
        #-----------------------#
        # get the log directory #
        #-----------------------#
        log_dir = None
        # first try CAVI, CWMS-Vue or HEC-DSSVue log directory
        try :
            log_dir = Paths.get(System.getProperty("LOGFILE")).getParent().toString()
        except :
            # maybe CWMS_HOME?
            log_dir = System.getProperty("CWMS_HOME")
            if log_dir :
                # (almost) last chance
                log_dir = os.path.join(log_dir, "..", "HEC", "HEC-DSSVue", "scripts")
                if not os.path.exists(log_dir) or not os.path.isdir(log_dir) :
                    # give up and log to current directory
                    log_dir = "."
            else :
                # give up and log to current directory
                log_dir = "."
        #----------------------------------------------------------------------------------#
        # replace any environment variable references in the log directory with the values #
        #----------------------------------------------------------------------------------#
        while True :
            m = var_pattern.search(log_dir)
            if not m : break
            if m.group(2) :
                log_dir = log_dir.replace(m.group(1), os.getenv(m.group(2)))
            elif m.group(3) :
                log_dir = log_dir.replace(m.group(1), os.getenv(m.group(3)))
            if m.group(4) :
                log_dir = log_dir.replace(m.group(1), os.getenv(m.group(4)))
        log_file_name = "{0}_{1}.log".format(
            str(datetime.datetime.now())[:19].replace("-",'.').replace(" ","-").replace(":",""),
            self.program_name)
        self.log_file_name = File(Paths.get(log_dir, log_file_name).toAbsolutePath().toString()).getCanonicalPath()
        self.dss_message_file = self.log_file_name.replace(".log", ".dssmsg.log")
        self.initComponents()
        self.addWindowListener(self.MyWindowAdapter(self))

    def initComponents(self):
        '''
        Set up the UI
        '''
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
        
        lblTopLevelSrcDir = JLabel("Top Level Source Directory")
        springLayout.putConstraint(SpringLayout.NORTH, lblTopLevelSrcDir, 10, SpringLayout.NORTH, self.getContentPane())
        springLayout.putConstraint(SpringLayout.WEST, lblTopLevelSrcDir, 10, SpringLayout.WEST, self.getContentPane())
        self.getContentPane().add(lblTopLevelSrcDir)
        
        self.tfTopLevelSrcDir = JTextField()
        self.tfTopLevelSrcDir.setEditable(False)
        self.tfTopLevelSrcDir.setColumns(10)
        springLayout.putConstraint(SpringLayout.NORTH, self.tfTopLevelSrcDir, -4, SpringLayout.NORTH, lblTopLevelSrcDir)
        springLayout.putConstraint(SpringLayout.WEST, self.tfTopLevelSrcDir, 6, SpringLayout.EAST, lblTopLevelSrcDir)
        springLayout.putConstraint(SpringLayout.EAST, self.tfTopLevelSrcDir, 450, SpringLayout.EAST, lblTopLevelSrcDir)
        self.getContentPane().add(self.tfTopLevelSrcDir)
        
        lblTopLevelArchDir = JLabel("Top Level Archive Directory")
        springLayout.putConstraint(SpringLayout.NORTH, lblTopLevelArchDir, 10, SpringLayout.SOUTH, lblTopLevelSrcDir)
        springLayout.putConstraint(SpringLayout.WEST, lblTopLevelArchDir, 0, SpringLayout.WEST, lblTopLevelSrcDir)
        self.getContentPane().add(lblTopLevelArchDir)
        
        self.tfTopLevelArchDir = JTextField()
        self.tfTopLevelArchDir.setEditable(False)
        self.tfTopLevelArchDir.setColumns(10)
        springLayout.putConstraint(SpringLayout.NORTH, self.tfTopLevelArchDir, -4, SpringLayout.NORTH, lblTopLevelArchDir)
        springLayout.putConstraint(SpringLayout.WEST, self.tfTopLevelArchDir, 6, SpringLayout.EAST, lblTopLevelArchDir)
        springLayout.putConstraint(SpringLayout.EAST, self.tfTopLevelArchDir, 450, SpringLayout.EAST, lblTopLevelArchDir)
        self.getContentPane().add(self.tfTopLevelArchDir)
        
        springLayout.putConstraint(SpringLayout.WEST, self.tfTopLevelSrcDir, 6, SpringLayout.EAST, lblTopLevelArchDir)
        springLayout.putConstraint(SpringLayout.EAST, self.tfTopLevelSrcDir, 450, SpringLayout.EAST, lblTopLevelArchDir)

        lblV6DssFile = JLabel("Version 6 DSS file")
        lblV6DssFile.setForeground(Color.RED)
        springLayout.putConstraint(SpringLayout.NORTH, lblV6DssFile, 10, SpringLayout.SOUTH, lblTopLevelArchDir)
        springLayout.putConstraint(SpringLayout.WEST, lblV6DssFile, 0, SpringLayout.WEST, lblTopLevelArchDir)
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
        springLayout.putConstraint(SpringLayout.EAST, self.treeScrollPane, 0, SpringLayout.EAST, self.tfTopLevelSrcDir)
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
        
        self.btnChooseDirs = JButton("Choose Directories")
        self.btnChooseDirs.addActionListener(self.chooseTopLevelDirs)
        springLayout.putConstraint(SpringLayout.NORTH, self.btnChooseDirs, 180, SpringLayout.NORTH, self.getContentPane())
        springLayout.putConstraint(SpringLayout.WEST, self.btnChooseDirs, 50, SpringLayout.EAST, self.treeScrollPane)
        springLayout.putConstraint(SpringLayout.EAST, self.btnChooseDirs, 200, SpringLayout.EAST, self.treeScrollPane)
        self.getContentPane().add(self.btnChooseDirs)
        
        self.btnStart = JButton("Start")
        self.btnStart.addActionListener(self.startFileConversion)
        springLayout.putConstraint(SpringLayout.NORTH, self.btnStart, 54, SpringLayout.SOUTH, self.btnChooseDirs)
        springLayout.putConstraint(SpringLayout.WEST, self.btnStart, 0, SpringLayout.WEST, self.btnChooseDirs)
        springLayout.putConstraint(SpringLayout.EAST, self.btnStart, 0, SpringLayout.EAST, self.btnChooseDirs)
        self.getContentPane().add(self.btnStart)
        
        self.btnExitCancel = JButton("Exit")
        self.btnExitCancel.addActionListener(self.exitOrCancel)
        springLayout.putConstraint(SpringLayout.NORTH, self.btnExitCancel, 54, SpringLayout.SOUTH, self.btnStart)
        springLayout.putConstraint(SpringLayout.WEST, self.btnExitCancel, 0, SpringLayout.WEST, self.btnChooseDirs)
        springLayout.putConstraint(SpringLayout.EAST, self.btnExitCancel, 0, SpringLayout.EAST, self.btnChooseDirs)
        self.getContentPane().add(self.btnExitCancel)
        
        self.treeScrollPane.updateUI()

    def setApplicationFrame(self, frame) :
        '''
        Set the application program frame
        '''
        self.application_frame = frame

    def setLogsMenu(self, logs_menu) :
        '''
        Set the menu to attach log files to
        '''
        self.logs_menu = logs_menu
        text = ""
        try :
            text = self.logs_menu.getItem(self.logs_menu.getItemCount()-1).getText()
        except :
            pass
        if not text.endswith(".log") and not text.endswith(".dssmsg.log") :
            self.logs_menu.addSeparator()
        log_file_name = os.path.split(self.log_file_name)[1]
        dss_msg_file = os.path.split(self.dss_message_file)[1]
        self.logfiles[log_file_name] = self.log_file_name
        self.logfiles[dss_msg_file] = self.dss_message_file
        for filename in log_file_name, dss_msg_file :
            menu_item = JMenuItem(filename, UIManager.getIcon("FileView.fileIcon"))
            menu_item.addActionListener(self)
            self.logs_menu.add(menu_item)
    
    def actionPerformed(self, e) :
        '''
        Display the log file selected from the logs menu
        '''
        try :
            logfile = self.logfiles[e.getActionCommand()]
        except KeyError :
            return
        if self.application_frame :
            x = self.application_frame.getLocation().x + 100
            y = self.application_frame.getLocation().y + 100
        else :
            x = y = 100
        parent = self.application_frame if self.application_frame else self
        if use_TextEditorDialog :
            #----------------#
            # CAVI, CWMS-Vue #
            #----------------#
            id = Identifier(logfile, SimpleFile(logfile))
            dlg = TextEditorDialog(parent, False, id, False)
            dlg.fillForm(id)
        else :
            #------------#
            # HEC-DSSVue #
            #------------#
            dlg = TextDialog(parent, False)
            dlg.initialize(logfile, False)
        dlg.setLocation(x, y)
        dlg.setSize(1200, 400)
        dlg.setVisible(True)
    
    def onClose(self, event) :
        '''
        Handle the user clicking the "X"
        '''
        self.exit_when_canceled = True
        isConverting = self.btnExitCancel.getText() in ("Cancel", "Waiting")
        self.exitOrCancel(event)
        if isConverting :
            msgbox = JOptionPane(
                "The process will exit after the current file conversion is complete",
                JOptionPane.INFORMATION_MESSAGE,
                JOptionPane.DEFAULT_OPTION,
                None,
                [],
                None)
            msgbox.createDialog(self, "File Conversion In Process...").setVisible(True)

    def log(self, message) :
        '''
        Output to log file and update log text element
        '''
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
        '''
        Add all DSS files to the tree element, noting the DSS version of each
        '''
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
        self.log("{0} files added from {1}".format(len(dss_files), self.top_level_source_dir))
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
        '''
        Tell the tree element how to render a specific DSS file based on its version
        and optionally scroll the tree view so that the file is visible and selected
        '''
        row = self.rows[dss_file]
        self.tree_cell_renderer.setRowVersion(row, version)
        if update_view :
            self.tree.scrollRowToVisible(row)
            self.tree.setSelectionRow(row)

    def expandAllTreeRows(self) :
        '''
        Expand the tree view
        '''
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

    def chooseTopLevelDirs(self, e):
        '''
        Choose the source and archive directories.
        - Source dir is where we look for files to convert
        - Archive dir is where we move v6 files to for archiving
        '''
        self.setCursor(Cursor(Cursor.WAIT_CURSOR))
        self.btnChooseDirs.setEnabled(False)
        self.btnStart.setEnabled(False)
        self.btnExitCancel.setEnabled(False)
        try :
            #-------------------------#
            # Choose source directory #
            #-------------------------#
            chooser = DirectoryChooser(self.top_level_source_dir, archive=False)
            self.top_level_source_dir = chooser.chooseDirectory(self)
            chooser.dispose()
            del(chooser)
            if self.top_level_source_dir :
                self.log("Selected top level source directory {}".format(self.top_level_source_dir))
                if os.path.isdir(self.top_level_source_dir) :
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
                    self.tfTopLevelSrcDir.setText(self.top_level_source_dir)
                    self.addDssFiles(find_dss_files(self.top_level_source_dir))
                    #--------------------------#
                    # Choose archive directory #
                    #--------------------------#
                    chooser = DirectoryChooser(self.top_level_archive_dir, archive=True)
                    self.top_level_archive_dir = chooser.chooseDirectory(self)
                    chooser.dispose()
                    del(chooser)
                    self.log("Selected top level archive directory {}".format(self.top_level_archive_dir))
                    if not os.path.exists(self.top_level_archive_dir) :
                        choice = JOptionPane.showConfirmDialog(
                            self,
                            "<html>Directory <b>{}</b> does not exist.<br>Do you want to create it?</html>".format(self.top_level_archive_dir),
                            "Directory Does Not Exist",
                            JOptionPane.YES_NO_OPTION)
                        if choice == JOptionPane.YES_OPTION :
                            os.mkdir(self.top_level_archive_dir)
                            self.log("Created directory {}".format(self.top_level_archive_dir))
                        else :
                            self.log("Selected top level archive directiry does not exist and was not created")
                            self.top_level_archive_dir = None
                    if self.top_level_archive_dir :
                        if os.path.isdir(self.top_level_archive_dir) :
                            if Files.isSameFile(Paths.get(self.top_level_source_dir), Paths.get(self.top_level_archive_dir)) :
                                self.log("ERROR - top level source and archive directories may not be the same")
                                self.top_level_archive_dir = None
                            else :
                                self.tfTopLevelArchDir.setText(self.top_level_archive_dir)
                        else :
                            self.log("ERROR - no such directory : {}".format(self.top_level_archive_dir))
                            self.top_level_archive_dir = None
                else :
                    self.log("ERROR - no such directory : {}".format(self.top_level_source_dir))
                    self.top_level_source_dir = None
        except JavaException as je :
            self.log("ERROR - {}".format(je.getMessage()))
            je.printStackTrace()
        except Exception as e:
            self.log(str(e))
            traceback.print_exc()
        finally :
            self.setCursor(Cursor(Cursor.DEFAULT_CURSOR))
            self.btnChooseDirs.setEnabled(True)
            self.btnStart.setEnabled(bool(self.top_level_source_dir) and bool(self.top_level_archive_dir))
            self.btnExitCancel.setEnabled(True)

    def exitOrCancel(self, e):
        '''
        Stop conversion or exit dialog depending on state
        '''
        if self.btnExitCancel.getText() == "Cancel" :
            self.conversion_canceled = True
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
        '''
        Return whether conversion was canceled befor completion
        '''
        return self.conversion_canceled
        
    def getFilesToConvert(self) :
        '''
        Return number of files left to convert
        '''
        return self.files_to_convert
        
    def getBytesToConvert(self) :
        '''
        Return cumulative sizes of files left to convert
        '''
        return self.bytes_to_convert
        
    def getDssFiles(self) :
        '''
        Return the list of DSS files identified in the top-level source directory
        '''
        return self.dss_files[:]
        
    def getFileSizes(self) :
        '''
        Return the list of file sizes for DSS files identified in the top-level directory
        '''
        return copy.deepcopy(self.file_sizes)
        
    def getFileVersions(self) :
        '''
        Return the list of DSS versions for DSS files identified in the top-level directory
        '''
        return copy.deepcopy(self.file_versions)
        
    def getDssMessageFile(self) :
        '''
        Return the file used to hold the DSS output from the conversion activity
        '''
        return self.dss_message_file

    def startFileConversion(self, e):
        '''
        Start the conversion process
        '''
        self.conversion_done = False
        self.btnChooseDirs.setEnabled(False)
        self.btnStart.setEnabled(False)
        self.btnExitCancel.setText("Cancel")
        self.conversion_canceled = False
        self.log("Starting conversion")
        self.timer.start()
        self.converter = BackgroundFileConverter(self)
        self.converter.execute()
        
    def conversionDone(self, start_time) :
        '''
        Stop the conversion process either becuase there are no more DSS files or the conversion was canceled
        '''
        del self.converter
        self.converter = None
        self.conversion_done = True
        self.timer.stop()
        self.btnChooseDirs.setEnabled(True)
        self.btnExitCancel.setText("Exit")
        self.btnExitCancel.setEnabled(True)
        self.lblEtaValue.setText("")
        elapsed = secsToHms((datetime.datetime.now() - start_time).total_seconds())
        if self.isCanceled() :
            self.log("Convesrion canceled after {}".format(elapsed))
            if self.exit_when_canceled :
                self.exitOrCancel(None)
        else :
            self.log("Convesrion completed: {0} in {1}".format(formatByteCount(self.total_bytes_to_convert), elapsed))

    def updateEta(self, e):
        '''
        Update the estimated time to completion element from a timer event
        '''
        secs = hmsToSecs(self.lblEtaValue.getText())
        if secs :
            self.updateEtaLabel(secs - 1)
        else :
            self.updateEtaLabel(None)
            
    def updateEtaLabel(self, secs) :
        '''
        Set the estimated time to completion element
        '''
        if self.conversion_done or self.conversion_canceled :
            self.lblEtaValue.setText("")
        elif secs :
            self.lblEtaValue.setText(secsToHms(secs))
        else :
            self.lblEtaValue.setText("Calculating {}".format("." * (int(time.time()) % 4)))
            
    def updateStatus(self, start_time, dss_file, files_converted, bytes_converted) :
        '''
        Update the UI based on conversion progress
        '''
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
        '''
        Constructor
        '''
        try :
            self.converter = converterFrame
            self.files_converted = 0
            self.files_to_convert = self.converter.getFilesToConvert()
            self.bytes_converted = 0
            self.bytes_to_convert = self.converter.getBytesToConvert()
            self.dss_files = self.converter.getDssFiles()
            self.file_sizes = self.converter.getFileSizes()
            self.file_versions = self.converter.getFileVersions()
            self.source_dir = self.converter.top_level_source_dir
            self.archive_dir = self.converter.top_level_archive_dir
            self.percent_complete = 0
            self.dss_message_file = self.converter.getDssMessageFile()
            self.util = HecDSSUtilities()
            Files.deleteIfExists(Paths.get(self.dss_message_file))
        except :
            traceback.print_exc()

    def publish(self, chunk) :
        '''
        Queues a chunk of of information for the UI thread to use
        '''
        super(BackgroundFileConverter, self).publish(chunk)

    def setProgress(self, percent) :
        '''
        Sets the percent complete of the background process for the UI thread
        '''
        super(BackgroundFileConverter, self).setProgress(percent)

    def doInBackground(self) :
        '''
        The background process
        '''
        self.start_time = datetime.datetime.now()
        for dss_file in self.dss_files :
            if self.converter.isCanceled() : 
                super(BackgroundFileConverter, self).setProgress(100)
                break
            if self.file_versions[dss_file] == 6 :
                try :
                    relative_filename = dss_file[len(self.source_dir):]
                    if relative_filename[0] == os.sep :
                        relative_filename = relative_filename[1:]
                    archive_file = os.path.join(self.archive_dir, relative_filename)
                    archive_dir = os.path.split(archive_file)[0]
                    make_dir = "F"
                    if os.path.exists(archive_dir) :
                        if not os.path.isdir(archive_dir) :
                            raise Exception("Archive directory {} is not a directory".format(archive_dir))
                    else :
                        os.makedirs(archive_dir)
                        make_dir = "T"
                    self.publish("\t".join(["START", str(time.time()), dss_file, archive_file, make_dir]))
                    Files.move(
                        Paths.get(dss_file),
                        Paths.get(archive_file),
                        StandardCopyOption.REPLACE_EXISTING)
                    self.util.setMessageFile(self.dss_message_file)
                    self.util.setDSSFileName(archive_file)
                    self.util.convertVersion(dss_file)
                    self.util.close()
                    self.files_converted += 1
                    self.bytes_converted += self.file_sizes[dss_file]
                    self.publish("\t".join(["END", str(time.time()), dss_file, archive_file, make_dir]))
                    self.setProgress(100 * self.bytes_converted // self.bytes_to_convert)
                except :
                    traceback.print_exc()

    def process(self, chunks) :
        '''
        Code in the UI thread to process the information published from doInBackground()
        '''
        for chunk in chunks :
            status, time_val, dss_file, archive_file, make_dir = chunk.split("\t")
            try :
                if status == "START" :
                    self.start_secs = float(time_val)
                    self.converter.setDssFileVersionInTree(dss_file, 6)
                    dss_file_only = os.path.split(dss_file)[1]
                    archive_dir = os.path.split(archive_file)[0]
                    self.converter.log('Starting conversion of "{}"'.format(dss_file))
                    if make_dir == "T" :
                        self.converter.log('    creating directory "{}"'.format(archive_dir))
                    self.converter.log('    moving "{}" to "{}"'.format(dss_file_only, archive_dir))
                    self.converter.log('    converting into "{}"'.format(dss_file_only))
                elif status == "END" :
                    self.converter.log("    {0} converted in {1}".format(
                        formatByteCount(self.file_sizes[dss_file]),
                        secsToHms(float(time_val) - self.start_secs)))
                    self.converter.updateStatus(self.start_time, dss_file, self.files_converted, self.bytes_converted)
            except :
                self.converter.log(traceback.format_exc())

    def done(self) :
        '''
        Called when background process ends
        '''
        self.util.flushMessageFile()
        self.util.closeMessageFile()
        del self.util
        self.converter.conversionDone(self.start_time)

class DirectoryChooser(JFrame):
    '''
    A simple Swing-based UI to select a top-level directory.
    '''
    def __init__(self, initial_directory=None, archive=False):
        '''
        Init the directory chooser dialog
        '''
        super(DirectoryChooser, self).__init__()
        self.archive = archive
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
        title = "Select Top Level {} Directory".format("Archive" if self.archive else "Source")
        ret = self.fileChooser.showDialog(parent, title)
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
        '''
        Constructor
        '''
        self.resetRowVersions()

    def resetRowVersions(self) :
        '''
        Reset the renderer
        '''
        self.v6_files = set()
        self.v7_files = set()
        
    def setRowVersion(self, row, version) :
        '''
        Set the DSS version for a row in the tree
        '''
        if version == 6 :
            if row in self.v7_files : self.v7_files.remove(row)
            self.v6_files.add(row)
        elif version == 7 :
            if row in self.v6_files : self.v6_files.remove(row)
            self.v7_files.add(row)

    def getPreferredSize(self):
        '''
        Pad the preferred size of the text component
        '''
        preferredSize = super(CustomTreeCellRenderer, self).getPreferredSize()
        preferredSize.width += 100  # Add additional width to prevent truncation
        return preferredSize

    def getTreeCellRendererComponent(self, tree, value, selected, expanded, leaf, row, hasFocus):
        '''
        Render the text in the row based on whether it's a DSS file and the DSS file version
        '''
        c = super(CustomTreeCellRenderer, self).getTreeCellRendererComponent(tree, value, selected, expanded, leaf, row, hasFocus)

        if row in self.v6_files :
            c.setForeground(Color.RED)
        elif row in self.v7_files :
            c.setForeground(Color.BLUE)
        else:
            c.setForeground(Color.BLACK)
        return c

def secsToHms(secs) :
    '''
    Return the "h mm:ss" for the number of seconds
    '''
    secs = int(secs)
    hrs  = int(secs / 3600)
    mins = int((secs - 3600 * hrs) / 60)
    secs = secs - 3600 * hrs - 60 * mins
    return "{0} hr {1:02d} min {2:02d} sec".format(hrs, mins, secs)

def hmsToSecs(hms) :
    '''
    Return the number of seconds in "h mm:ss"
    '''
    m = hms_pattern.match(hms)
    if m :
        secs = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
        return secs
    else :
        return None

def formatByteCount(size) :
    '''
    Return the number of bytes using B, KB, MB, or GB
    '''
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
    '''
    Launches the UI
    '''
    global center_on_x, center_on_y
    UIManager.setLookAndFeel("com.sun.java.swing.plaf.windows.WindowsLookAndFeel")
    #---------------------------#
    # get the application frame #
    #---------------------------#
    application_frame = None
    for frame in Frame.getFrames() :
        if frame.__class__.__name__ in("ListSelection", "CwmsListSelection", "CaviFrame") and frame.isVisible() :
            application_frame = frame
            loc = frame.getLocationOnScreen()
            siz = frame.getSize()
            center_on_x = loc.x + siz.width / 2
            center_on_y = loc.y + siz.height / 2
            break
    #-------------------------------------#
    # get the menu to attach log files to #
    #-------------------------------------#
    logs_menu = None
    if frame.__class__.__name__ == "CaviFrame" :
        #------#
        # CAVI #
        #------#
        for component in frame.getComponents() :
            if component.__class__.__name__ == "RmaJFrame$4" :
                menu_bar = component.getMenuBar()
                if menu_bar is not None :
                    for i in range(menu_bar.getComponentCount()) :
                        menu = menu_bar.getComponentAtIndex(i)
                        if menu.getText() == "Tools" :
                            tool_menu = menu
                            for component in tool_menu.getMenuComponents() :
                                if component.__class__.__name__ == "EnablableJMenu" and component.getText() == "Logs" :
                                    logs_menu = component
    elif frame.__class__.__name__ in ("ListSelection", "CwmsListSelection") :
        #-------------------------#
        # CWMS-Vue and HEC-DSSVue #
        #-------------------------#
        for component in frame.getComponents() :
            if component.__class__.__name__ == "JRootPane" :
                menu_bar = component.getMenuBar()
                for i in range(menu_bar.getComponentCount()) :
                    menu = menu_bar.getComponentAtIndex(i)
                    if menu.getText() == "Advanced" :
                        advanced_menu = menu
                        for component in advanced_menu.getMenuComponents() :
                            if component.__class__.__name__ == "JMenu" and component.getText() == "Output" :
                                logs_menu = component

    window = DssConverterFrame()
    window.pack()
    window.setVisible(True)
    window.setApplicationFrame(application_frame)
    window.setLogsMenu(logs_menu)
    window.chooseTopLevelDirs(None)

if __name__ == "__main__":
    threading.Thread(target=main).start()
