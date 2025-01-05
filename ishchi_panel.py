from decimal import Decimal

from PyQt5.QtWidgets import (QMessageBox, QMainWindow, QPushButton, QWidget, QLineEdit,
                             QVBoxLayout, QHBoxLayout, QTableWidget, QHeaderView, QApplication,
                             QTableWidgetItem, QListWidgetItem, QListWidget, QLabel, QDialog, QComboBox, QSizePolicy)
from db_init import get_connection
from components import hspacer, spacer
from PyQt5.QtCore import Qt, QSize
from design import ishchilar_panel_css, qlistwidget_css, edit_oyna


class SavatgaOlish(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Savatga qo'shish")

        self.setGeometry(1200, 350, 300, 200)

        vertikal = QVBoxLayout()
        garizontal = QHBoxLayout()

        vertikal.addItem(spacer())

        self.soni = QLineEdit()
        self.soni.setPlaceholderText("Sonini kiriting")
        vertikal.addWidget(self.soni)

        lt = ['Pachka', 'Dona']

        self.tanlov = QComboBox()
        self.tanlov.addItems(lt)
        vertikal.addWidget(self.tanlov)

        self.btn = QPushButton("Savatga Qo'shish")
        self.btn.setEnabled(False)  # Boshlanishida tugmani o'chirib qo'yamiz
        garizontal.addWidget(self.btn)
        self.btn.clicked.connect(self.check_input)

        btn2 = QPushButton("Ortga")
        garizontal.addWidget(btn2)
        btn2.clicked.connect(self.reject)

        vertikal.addItem(spacer())

        vertikal.addLayout(garizontal)

        self.soni.textChanged.connect(self.check_text)  # Matn o'zgarganda tugmani yoqish/o'chirish

        self.setLayout(vertikal)
        self.setStyleSheet(edit_oyna)

    def check_text(self):
        """Matn kiritilsa va integer bo'lsa, tugmani yoqish."""
        text = self.soni.text().strip()
        if text and text.isdigit():  # faqat raqam bo'lsa, tugmani yoqamiz
            self.btn.setEnabled(True)
        else:
            self.btn.setEnabled(False)

    def check_input(self):
        """Sonini tekshirish: bo'sh yoki raqam bo'lmasa, xatolik chiqarish."""
        text = self.soni.text().strip()
        if not text:
            QMessageBox.warning(self, "Xato", "Iltimos, sonini kiriting!")
        elif not text.isdigit():
            QMessageBox.warning(self, "Xato", "Son faqat butun raqam bo'lishi kerak!")
        else:
            self.accept()

    def get_values(self):
        return self.soni.text(), self.tanlov.currentText()


class IshchiPanel(QMainWindow):
    def __init__(self, sotuvchi):
        super().__init__()

        self.sotuvchi = sotuvchi

        self.data = None
        self.setWindowTitle("Ishchi panel")
        self.savatga_oyna = None
        self.editga_oyna = False

        vertikal = QVBoxLayout()
        garizontal = QHBoxLayout()

        self.nomi = QLineEdit()
        self.nomi.setPlaceholderText("Dori nomi")
        self.nomi.returnPressed.connect(self.qidiruv_bosildi)
        garizontal.addWidget(self.nomi)

        btn = QPushButton("Qidiruv")
        btn.clicked.connect(self.qidiruv_bosildi)
        btn.setMinimumWidth(600)
        garizontal.addWidget(btn)

        vertikal.addLayout(garizontal)

        self.table = QTableWidget()

        vertikal.addWidget(self.table)

        self.yangilash()

        self.list_widget = QListWidget()
        self.list_widget.setMaximumHeight(300)
        self.list_widget.setStyleSheet(qlistwidget_css)

        self.sotilayotganlar = []

        vertikal.addWidget(self.list_widget)

        self.umumiy = QLabel("Umumiy summa: 00.00 so'm")
        self.umumiy.setMinimumHeight(65)
        vertikal.addWidget(self.umumiy)

        btn2 = QPushButton("Sotish")
        vertikal.addWidget(btn2)
        btn2.clicked.connect(self.sotildi)

        widget = QWidget()
        widget.setLayout(vertikal)
        self.setCentralWidget(widget)

        self.setStyleSheet(ishchilar_panel_css)

    def yangilash(self, data=None):
        if data is None:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute("""select id, nomi, xususiyati, narxi,pachka, dona, bir_pochka_miqdori from dorilar;""")

            self.data = cur.fetchall()

            cur.close()
            conn.close()
        else:
            self.data = data

        self.table.setRowCount(len(self.data))
        self.table.setColumnCount(7)

        header_list = ['Dori nomi', 'Xususiyati', 'Narxi', 'Pachkasi', 'Dona', '1 pachkadagi miqdori', 'Savatga']

        self.table.setHorizontalHeaderLabels(header_list)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for i, malumot in enumerate(self.data):
            for j, curr in enumerate(malumot[1:]):
                item = QTableWidgetItem(str(curr))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Tahrirlanmas qilish
                self.table.setItem(i, j, item)
            btn = QPushButton("Savatga")
            btn.setMinimumWidth(40)
            btn.clicked.connect(lambda checked, dori_id=malumot[0]: self.savatga_otish(dori_id))
            self.table.setCellWidget(i, 6, btn)
            self.table.setRowHeight(i, 60)

    def savatga_otish(self, dori_id):
        self.savatga_oyna = None
        self.savatga_oyna = SavatgaOlish()
        result = self.savatga_oyna.exec_()
        if result == QDialog.Accepted:
            malumotlar = self.savatga_oyna.get_values()
            conn = get_connection()
            cur = conn.cursor()

            cur.execute("""select * from dorilar where id=%s""", (dori_id,))

            dori = cur.fetchone()

            soni = 0
            tekshirish = False

            if malumotlar[1] == 'Dona':
                soni = int(dori[5]) - int(malumotlar[0])
            else:
                soni = int(dori[4]) - int(malumotlar[0])
                tekshirish = True

            cur.close()
            conn.close()

            if soni >= 0:

                label1 = QLabel(f"Dori nomi: {dori[1]}")
                label2 = None
                label3 = None

                if malumotlar[1] == 'Dona':
                    bir_dona = dori[3] / dori[6]
                    label2 = QLabel(f"Summa: {bir_dona * int(malumotlar[0])}")
                    label3 = QLabel(f"Soni: {malumotlar[0]} dona")
                else:
                    label2 = QLabel(f"Summa: {dori[3] * int(malumotlar[0])}")
                    label3 = QLabel(f"Soni: {malumotlar[0]} pachka")

                lt = [label1, label2, label3]
                if self.editga_oyna is True:
                    self.editga_oyna = False
                    return lt
                else:
                    conn = get_connection()
                    cur = conn.cursor()

                    if tekshirish is False:
                        temp1 = soni // int(dori[6])
                        cur.execute("""UPDATE dorilar SET dona=%s, pachka=%s where id=%s""", (soni, temp1,dori_id))
                    else:
                        temp1 = int(dori[5]) - int(dori[6]) * int(malumotlar[0])
                        cur.execute("""UPDATE dorilar SET pachka=%s, dona=%s where id=%s""", (soni, temp1, dori_id))

                    conn.commit()

                    cur.close()
                    conn.close()
                    self.sotilayotganlar.append(lt)
                    self.listni_yangilash()
                    self.yangilash()
            else:
                QMessageBox.warning(self, "Ogohlantirish", "Dorixonada ko'rsatilgan miqdorda dori mavjud emas")

    def listni_yangilash(self):
        self.list_widget.clear()
        for index, qator in enumerate(self.sotilayotganlar):
            item = QListWidgetItem()
            widget = QWidget()
            vertikal = QVBoxLayout()
            garizontal = QHBoxLayout()

            vertikal.addWidget(qator[0])
            vertikal.addWidget(qator[1])
            vertikal.addWidget(qator[2])

            garizontal.addLayout(vertikal)
            garizontal.addItem(hspacer())

            edit = QPushButton("Edit")
            garizontal.addWidget(edit)
            edit.setMinimumSize(100, 60)
            edit.clicked.connect(lambda checked, idx=index: self.edit_bosildi(idx))

            delete = QPushButton("Delete")
            delete.setMinimumSize(100, 60)
            delete.clicked.connect(lambda checked, idx=index: self.delete_bosildi(idx))
            garizontal.addWidget(delete)

            widget.setLayout(garizontal)
            widget.setMinimumHeight(70)
            item.setSizeHint(QSize(200, 130))

            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, widget)

        self.summani_xisoblash()

    def sotildi(self):
        temp1 = self.umumiy.text().split()
        if QMessageBox.question(self, "Tasdiqlash",
                                f"Umumiy summa: {temp1[-2]} so'm\nTasdiqlaysizmi?") == QMessageBox.Yes:
            self.list_widget.clear()

            conn = get_connection()
            cur = conn.cursor()

            for item in self.sotilayotganlar:
                nomi = item[0].text().split()
                summa = item[1].text().split()
                soni = item[2].text().split()

                dori_nomi = nomi[-1]
                sotilgan_summa = summa[-1]

                dona = None

                if soni[-1] == "dona":
                    dona = soni[-2]
                else:
                    cur.execute("""select bir_pochka_miqdori from dorilar where nomi=%s""", (dori_nomi,))

                    temp = cur.fetchone()

                    dona = int(soni[-2]) * int(temp[0])

                cur.execute("""INSERT INTO sotilgan_dorilar 
                (sotuvchi, dori_nomi,sotilgan_dona, sotilgan_summa)
                VALUES (%s,%s,%s,%s)                 
                 """, (self.sotuvchi, dori_nomi, dona, sotilgan_summa))

                conn.commit()

            cur.close()
            conn.close()

            self.sotilayotganlar.clear()
            self.summani_xisoblash()

    def summani_xisoblash(self):
        narx = 0
        if self.sotilayotganlar is not None:
            for curr in self.sotilayotganlar:
                item = curr[1].text()
                curr2 = item.split()[-1]
                narx += float(curr2)

        self.umumiy.setText(f"Umumiy summa: {round(narx, 2)} so'm")

    def delete_bosildi(self, idx):
        if QMessageBox.question(self, "Ogohlantirish", "Rostdan ham o'chirmoqchimisiz?") == QMessageBox.Yes:
            if 0 <= idx < len(self.sotilayotganlar):
                malumot = self.sotilayotganlar.pop(idx)
                nomi = malumot[0].text().split()
                temp1 = malumot[-1].text().split()

                conn = get_connection()
                cur = conn.cursor()

                cur.execute("""select * from dorilar where nomi=%s""", (nomi[-1],))

                dori = cur.fetchone()

                if temp1[-1] == 'pachka':
                    dona = int(dori[5]) + int(temp1[1]) * int(dori[6])
                    pachka = dona // int(dori[6])

                    cur.execute("""UPDATE dorilar SET pachka=%s, dona=%s where id=%s""", (pachka, dona, dori[0]))
                else:
                    dona = int(dori[5]) + int(temp1[1])
                    pachka = dona // int(dori[6])

                    cur.execute("""UPDATE dorilar SET pachka=%s, dona=%s where id=%s""", (pachka, dona, dori[0]))

                conn.commit()

                cur.close()
                conn.close()
            self.summani_xisoblash()
            self.listni_yangilash()
            self.yangilash()

    def edit_bosildi(self, idx):
        temp1 = self.sotilayotganlar[idx][0].text().split()
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""select * from dorilar where nomi=%s""", (temp1[-1],))

        dori = cur.fetchone()

        temp2 = self.sotilayotganlar[idx][-1].text().split()

        self.editga_oyna = True

        malumot = self.savatga_otish(dori[0])
        if malumot is not None:
            yangi = malumot[-1].text().split()

            if yangi[-1] == 'pachka':
                if temp2[-1] == 'pachka':
                    farqi = int(temp2[1]) - int(yangi[1])
                    curr = int(dori[4]) + farqi
                    dona = int(dori[5]) + int(dori[6]) * farqi

                    cur.execute("""UPDATE dorilar SET pachka=%s, dona=%s where id=%s""", (curr, dona, dori[0]))
                else:
                    dona = int(temp2[1]) + int(dori[5])
                    yangi_dona = dona - int(yangi[1]) * int(dori[6])
                    pachka = yangi_dona // int(dori[6])

                    cur.execute("""UPDATE dorilar SET pachka=%s, dona=%s where id=%s""", (pachka, yangi_dona, dori[0]))
            else:
                if temp2[-1] == 'pachka':
                    dona = int(dori[5]) + int(temp2[1]) * int(dori[6])
                    yangi_dona = dona - int(yangi[1])
                    pachka = yangi_dona // int(dori[6])

                    cur.execute("""UPDATE dorilar SET pachka=%s, dona=%s where id=%s""", (pachka, yangi_dona, dori[0]))
                else:
                    dona = int(dori[5]) + int(temp2[1])
                    yangi_dona = dona - int(yangi[1])
                    pachka = yangi_dona // int(dori[6])

                    cur.execute("""UPDATE dorilar SET pachka=%s, dona=%s where id=%s""", (pachka, yangi_dona, dori[0]))

            conn.commit()
            self.sotilayotganlar[idx] = malumot

        cur.close()
        conn.close()

        self.listni_yangilash()
        self.summani_xisoblash()
        self.yangilash()

    def qidiruv_bosildi(self):
        nomi = self.nomi.text()

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""SELECT * FROM dorilar WHERE nomi LIKE %s""", (f"%{nomi}%",))

        data = cur.fetchall()

        cur.close()
        conn.close()

        self.yangilash(data)

