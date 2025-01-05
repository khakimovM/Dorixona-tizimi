from PyQt5.QtWidgets import QApplication
from kirish import Kirish


app = QApplication([])

cur = Kirish()
cur.showMaximized()

app.exec_()
