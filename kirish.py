from PyQt5.QtWidgets import (QMessageBox, QMainWindow, QPushButton, QWidget, QLineEdit,
                             QVBoxLayout, QHBoxLayout)
from components import spacer
from db_init import get_connection, load_tables
from ishchi_panel import IshchiPanel
from admin_panel import AdminPanel
from design import kirish


class Kirish(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Kirish oynasi")

        self.ishchi_oyna = None
        self.admin_oyna = None

        load_tables()

        vertikal = QVBoxLayout()
        garizontal = QHBoxLayout()

        vertikal.addItem(spacer())

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        vertikal.addWidget(self.username)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        vertikal.addWidget(self.password)
        self.password.returnPressed.connect(self.kirish_bosildi)

        btn = QPushButton("Kirish")
        btn.clicked.connect(self.kirish_bosildi)
        vertikal.addWidget(btn)

        vertikal.addItem(spacer())

        garizontal.addItem(spacer())
        garizontal.addLayout(vertikal)
        garizontal.addItem(spacer())

        widget = QWidget()
        widget.setLayout(garizontal)
        self.setCentralWidget(widget)

        self.setStyleSheet(kirish)

    def kirish_bosildi(self):
        ismi = self.username.text()
        password = self.password.text()

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""select * from users where ismi=%s and password=%s;""", (ismi, password))

        malumot = cur.fetchone()

        cur.close()
        conn.close()

        if malumot is None:
            QMessageBox.warning(self, "Ogohlantirish", "Siz noto'g'ri ma'lumot kiritdingiz")
            self.username.clear()
            self.password.clear()
        else:
            if malumot[3] == 'Ishchi':
                self.ishchi_oyna = IshchiPanel(self.username.text())
                self.ishchi_oyna.showMaximized()
                self.close()
                QMessageBox.information(self, "Muvaffaqiyatli", "Siz tizimga muvaffaqiyatli kirdingiz")
            else:
                self.admin_oyna = AdminPanel(self)
                self.admin_oyna.showMaximized()
                self.close()
                self.username.clear()
                self.password.clear()
