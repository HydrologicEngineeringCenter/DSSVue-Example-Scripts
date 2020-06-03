
from javax.swing import JOptionPane

# presents dialog with Yes or No question
opt = JOptionPane.showConfirmDialog(None,"choose one", "choose one Title", JOptionPane.YES_NO_OPTION)

if opt == None:
    print("closed without answer")
elif opt == JOptionPane.NO_OPTION :
    print(" User selected No")
elif opt == JOptionPane.YES_OPTION :
    print(" User selected Yes")

