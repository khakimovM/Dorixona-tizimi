from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
                             QLineEdit, QLabel, QComboBox, QApplication, QTableWidgetItem, QTableWidget,
                             QHeaderView, QDialog, QMessageBox)
from components import hspacer, spacer
from db_init import get_connection, load_tables
from design import ishchilar_panel_css, edit_oyna


class DeleteOynasi(QDialog):
    def __init__(self, ism):
        super().__init__()

        self.ism = ism

        self.setGeometry(1200, 400, 300, 200)

        self.setWindowTitle("Delete window")

        vertikal = QVBoxLayout()
        vertikal.addItem(spacer())

        btn1 = QPushButton("Ishdan bo'shatish")
        vertikal.addWidget(btn1)
        btn1.clicked.connect(self.accept)

        btn2 = QPushButton("Sotuvni 0 holatga keltirish")
        vertikal.addWidget(btn2)
        btn2.clicked.connect(self.bosildi)

        vertikal.addItem(spacer())

        btn3 = QPushButton("Ortga qaytish")
        vertikal.addWidget(btn3)
        btn3.clicked.connect(self.ortga)

        vertikal.addItem(spacer())

        self.setLayout(vertikal)
        self.setStyleSheet(edit_oyna)

    def bosildi(self):
        conn = get_connection()
        cur = conn.cursor()

        if QMessageBox.question(self, "Tasdiqlah",
                                "Hodimni barcha sotuvi 0 holatga aylanadi,Tasdiqlaysizmi?") == QMessageBox.Yes:
            cur.execute("""delete from sotilgan_dorilar where sotuvchi=%s""", (self.ism,))

        conn.commit()

        cur.close()
        conn.close()

        self.close()

    def ortga(self):
        self.close()


class EditOynasi(QDialog):
    def __init__(self, ism=None, parol=None):
        super().__init__()

        self.setWindowTitle("Edit oynasi")

        vertikal = QVBoxLayout()
        garizontal = QHBoxLayout()

        self.ismi = QLineEdit(ism)
        vertikal.addWidget(self.ismi)
        self.ismi.setPlaceholderText("Ismi")

        self.password = QLineEdit(parol)
        vertikal.addWidget(self.password)
        self.password.setPlaceholderText("Password")

        lt = ["Ishchi", "Admin"]

        self.lavozimi = QComboBox()
        self.lavozimi.addItems(lt)
        vertikal.addWidget(self.lavozimi)

        btn = QPushButton("Qo'shish/Tahrirlash")
        garizontal.addWidget(btn)
        btn.clicked.connect(self.accept)

        btn2 = QPushButton("Ortga")
        garizontal.addWidget(btn2)
        btn2.clicked.connect(self.reject)

        vertikal.addLayout(garizontal)

        self.setLayout(vertikal)
        self.setStyleSheet(edit_oyna)

    def get_values(self):
        return self.ismi.text(), self.password.text(), self.lavozimi.currentText()


class IshchilarPanel(QMainWindow):
    def __init__(self, parent):
        super().__init__()

        self.bosh = parent

        load_tables()

        self.edit_oyna = None
        self.hodim_oyna = None
        self.delete_oyna = None

        self.setWindowTitle("Ishchilar bo'yicha hisobot")

        vertikal = QVBoxLayout()
        garizontal = QHBoxLayout()
        garizontal1 = QHBoxLayout()

        self.qidiruv = QLineEdit()
        self.qidiruv.setPlaceholderText("Hodim ismi bo'yicha qidiruv")
        garizontal1.addWidget(self.qidiruv)
        self.qidiruv.returnPressed.connect(self.filter_bosildi)

        btn_qidiruv = QPushButton("Qidiruv")
        garizontal1.addWidget(btn_qidiruv)
        btn_qidiruv.clicked.connect(self.filter_bosildi)

        btn_qoshish = QPushButton("Hodim qo'shish")
        garizontal1.addWidget(btn_qoshish)
        btn_qoshish.clicked.connect(self.hodim_qoshish)

        vertikal.addLayout(garizontal1)

        lt = ['Tanlov', 'Joriy oy', 'Oxirgi oy', 'Yillik']

        label = QLabel("Filter")
        garizontal2 = QHBoxLayout()
        garizontal2.addWidget(label)

        self.filter = QComboBox()
        self.filter.addItems(lt)
        garizontal2.addWidget(self.filter)
        self.filter.activated.connect(self.filter_bosildi)

        garizontal2.addItem(hspacer())

        vertikal.addLayout(garizontal2)

        self.table = QTableWidget()
        vertikal.addWidget(self.table)

        self.jadval_yangilash()

        btn_ortga = QPushButton("Ortga qaytish")
        vertikal.addWidget(btn_ortga)
        btn_ortga.clicked.connect(self.ortga_bosildi)

        widget = QWidget()
        widget.setLayout(vertikal)
        self.setCentralWidget(widget)

        self.setStyleSheet(ishchilar_panel_css)

    def jadval_yangilash(self, data1=None):
        conn = get_connection()
        cur = conn.cursor()

        if data1 is None:
            cur.execute("""select ismi,password,qabul_qilingan_sana, lavozimi from users""")
            hodim = cur.fetchall()
        else:
            hodim = data1

        data = []

        for malumot in hodim:
            miqdor = 0
            if malumot[-1] == 'Ishchi':
                cur.execute("""SELECT sotilgan_summa FROM sotilgan_dorilar WHERE sotuvchi = %s""", (malumot[0],))
                summa = cur.fetchall()

                if summa is None:
                    miqdor = 0
                else:
                    for i in summa:
                        miqdor += float(i[0])

                temp = list(malumot[:3]) + [f"{miqdor:.1f}"]
                data.append(temp)
            else:
                temp = list(malumot[:3]) + ['Admin']
                data.append(temp)

        self.table.setRowCount(len(data))
        self.table.setColumnCount(5)

        header_list = ['Hodim ismi', 'password', 'Ishga qabul qilingan sana', 'Sotgan summasi', 'Bosharuv']

        self.table.setHorizontalHeaderLabels(header_list)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for i, malumot in enumerate(data):
            for j, curr in enumerate(malumot):
                item = QTableWidgetItem(str(curr))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Tahrirlanmas qilish
                self.table.setItem(i, j, item)
            garizontal = QHBoxLayout()
            widget = QWidget()
            edit = QPushButton("Edit")
            edit.clicked.connect(lambda checked, ism=malumot[0]: self.edit_bosildi(ism))
            delete = QPushButton("Chetlatish")
            delete.clicked.connect(lambda checked, ism=malumot[0]: self.delete_bosildi(ism))
            garizontal.addWidget(edit)
            garizontal.addWidget(delete)
            widget.setLayout(garizontal)
            widget.setMinimumHeight(80)
            self.table.setCellWidget(i, 4, widget)
            self.table.setRowHeight(i, 80)

    def edit_bosildi(self, hodim_ismi):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""select * from users where ismi=%s;""", (hodim_ismi,))

        hodim = cur.fetchone()

        self.edit_oyna = EditOynasi(hodim[1], hodim[2])

        if self.edit_oyna.exec_() == QDialog.Accepted:
            malumotlar = self.edit_oyna.get_values()

            cur.execute(f"""UPDATE users SET ismi=%s, password=%s, lavozimi=%s where id={hodim[0]};""", malumotlar)
            cur.execute("""UPDATE sotilgan_dorilar SET sotuvchi=%s where sotuvchi=%s;""", (malumotlar[0], hodim[1]))

            conn.commit()

        self.jadval_yangilash()

        cur.close()
        conn.close()

    def hodim_qoshish(self):
        con = get_connection()
        cur = con.cursor()

        self.hodim_oyna = EditOynasi()

        if self.hodim_oyna.exec_() == QDialog.Accepted:
            malumot = self.hodim_oyna.get_values()
            print(malumot[0])

            cur.execute("""select * from users where ismi=%s""", (malumot[0], ))

            temp = cur.fetchall()

            if len(temp) > 0:
                QMessageBox.warning(self, "Xatolik", "Bu ismdagi hodim mavjud\nIltimos boshqa ism bilan kirgizing")
            else:
                cur.execute("""insert into users(ismi, password, lavozimi) values
                    (%s, %s, %s)""", malumot)

                con.commit()

        cur.close()
        con.close()
        self.jadval_yangilash()

    def delete_bosildi(self, ism):
        conn = get_connection()
        cur = conn.cursor()

        self.delete_oyna = DeleteOynasi(ism)

        result = self.delete_oyna.exec_()

        if result == QDialog.Accepted:
            # Foydalanuvchi "Ishdan bo'shatish" tugmasini bosgan
            if QMessageBox.question(self, "Tasdiqlash",
                                    "Hodimni ishdan bo'shatishni tasdiqlaysizmi?") == QMessageBox.Yes:
                cur.execute("""DELETE FROM users WHERE ismi=%s""", (ism,))
                conn.commit()

        cur.close()
        conn.close()
        self.jadval_yangilash()

    def filter_bosildi(self):
        data = None
        conn = get_connection()
        cur = conn.cursor()
        text = self.qidiruv.text()  # Qidiruv maydoniga kiritilgan matnni olish

        # Filtrlash uchun tanlangan qiymat
        lt = ['Tanlov', 'Joriy oy', 'Oxirgi oy', 'Yillik']
        selected_filter = self.filter.currentText()

        if selected_filter == lt[0]:  # 'Tanlov'
            # Barcha sotuvlarni olib keladi
            cur.execute("""
                SELECT u.ismi, u.password, u.qabul_qilingan_sana, u.lavozimi
                FROM users u
                LEFT JOIN sotilgan_dorilar sd ON u.ismi = sd.sotuvchi
                WHERE u.ismi LIKE %s
                GROUP BY u.ismi, u.password, u.qabul_qilingan_sana, u.lavozimi
            """, (f"%{text}%",))
            data = cur.fetchall()

        elif selected_filter == lt[1]:  # 'Joriy oy'
            # Joriy oy ichidagi sotuvlarni olib keladi
            cur.execute("""
                SELECT u.ismi, u.password, u.qabul_qilingan_sana, u.lavozimi
                FROM users u
                LEFT JOIN sotilgan_dorilar sd ON u.ismi = sd.sotuvchi
                WHERE MONTH(sd.sotilgan_vaqt) = MONTH(CURRENT_DATE())
                AND YEAR(sd.sotilgan_vaqt) = YEAR(CURRENT_DATE()) AND u.ismi LIKE %s
                GROUP BY u.ismi, u.password, u.qabul_qilingan_sana, u.lavozimi
            """, (f"%{text}%",))
            data = cur.fetchall()

        elif selected_filter == lt[2]:  # 'Oxirgi oy'
            # Oxirgi oy ichidagi sotuvlarni olib keladi
            cur.execute("""
                SELECT u.ismi, u.password, u.qabul_qilingan_sana, u.lavozimi
                FROM users u
                LEFT JOIN sotilgan_dorilar sd ON u.ismi = sd.sotuvchi
                WHERE MONTH(sd.sotilgan_vaqt) = MONTH(CURRENT_DATE() - INTERVAL 1 MONTH)
                AND YEAR(sd.sotilgan_vaqt) = YEAR(CURRENT_DATE() - INTERVAL 1 MONTH) AND u.ismi LIKE %s
                GROUP BY u.ismi, u.password, u.qabul_qilingan_sana, u.lavozimi
            """, (f"%{text}%",))
            data = cur.fetchall()

        elif selected_filter == lt[3]:  # 'Yillik'
            # Joriy yil ichidagi sotuvlarni olib keladi
            cur.execute("""
                SELECT u.ismi, u.password, u.qabul_qilingan_sana, u.lavozimi
                FROM users u
                LEFT JOIN sotilgan_dorilar sd ON u.ismi = sd.sotuvchi
                WHERE YEAR(sd.sotilgan_vaqt) = YEAR(CURRENT_DATE()) AND u.ismi LIKE %s
                GROUP BY u.ismi, u.password, u.qabul_qilingan_sana, u.lavozimi
            """, (f"%{text}%",))
            data = cur.fetchall()

        cur.close()
        conn.close()
        self.jadval_yangilash(data)

    def ortga_bosildi(self):
        self.bosh.showMaximized()
        self.close()


