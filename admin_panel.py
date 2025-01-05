from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget, QHBoxLayout, QVBoxLayout
from components import spacer
from ishchilar_panel import IshchilarPanel
from dorilar_panel import DorilarHisobot
from design import admin


class AdminPanel(QMainWindow):
    def __init__(self, asosiy):
        super().__init__()

        self.asosiy_oyna = asosiy

        self.ishchilar_hisobot = None
        self.dorilar_hisobot = None

        self.setWindowTitle("Admin panel")

        vertikal = QVBoxLayout()
        garizontal = QHBoxLayout()

        vertikal.addItem(spacer())
        vertikal.addItem(spacer())

        ishchilar = QPushButton("Ishchilar bo'yicha hisobot")
        vertikal.addWidget(ishchilar)
        ishchilar.clicked.connect(self.ishchilar_bosildi)

        dorilar = QPushButton("Dorilar bo'yicha hisobot")
        vertikal.addWidget(dorilar)
        dorilar.clicked.connect(self.dorilar_bosildi)

        vertikal.addItem(spacer())

        ortga = QPushButton("Ortga qaytish")
        vertikal.addWidget(ortga)
        ortga.clicked.connect(self.ortga_bosildi)

        vertikal.addItem(spacer())
        vertikal.addItem(spacer())

        garizontal.addItem(spacer())
        garizontal.addLayout(vertikal)
        garizontal.addItem(spacer())

        widget = QWidget()
        widget.setLayout(garizontal)
        self.setCentralWidget(widget)

        self.setStyleSheet(admin)

    def ortga_bosildi(self):
        self.asosiy_oyna.showMaximized()
        self.close()

    def ishchilar_bosildi(self):
        self.ishchilar_hisobot = None
        self.ishchilar_hisobot = IshchilarPanel(self)
        self.ishchilar_hisobot.showMaximized()
        self.close()

    def dorilar_bosildi(self):
        self.dorilar_hisobot = None
        self.dorilar_hisobot = DorilarHisobot(self)
        self.dorilar_hisobot.showMaximized()
        self.close()
