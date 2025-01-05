from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
                             QLineEdit, QLabel, QComboBox, QApplication, QTableWidgetItem, QTableWidget,
                             QHeaderView, QDialog, QMessageBox)
from PyQt5.QtCore import Qt
from components import hspacer, spacer
from db_init import get_connection, load_tables
from design import ishchilar_panel_css, edit_oyna


class DoriQoshish(QDialog):
    def __init__(self, nomi=None, xusus=None, kelish=None, sotil=None, pachka=None, miqdor=None, kelgan=None):
        super().__init__()

        self.setWindowTitle("Dori qo'shish/tahrirlash")

        self.setGeometry(1000, 300, 400, 250)

        vertikal = QVBoxLayout()
        garizontal = QHBoxLayout()

        vertikal.addItem(spacer())

        self.nomi = QLineEdit(nomi)
        self.nomi.setPlaceholderText("Dori nomi")
        vertikal.addWidget(self.nomi)

        self.xususiyati = QLineEdit(xusus)
        self.xususiyati.setPlaceholderText("Xususiyati")
        vertikal.addWidget(self.xususiyati)

        self.kelishnarx = QLineEdit(kelish)
        self.kelishnarx.setPlaceholderText("Kelish narxi(1 pachka uchun)")
        vertikal.addWidget(self.kelishnarx)

        self.sotilishnarx = QLineEdit(sotil)
        self.sotilishnarx.setPlaceholderText("Sotilish narxi(1 pachka uchun)")
        vertikal.addWidget(self.sotilishnarx)

        self.pachka = QLineEdit(pachka)
        self.pachka.setPlaceholderText("Nechta pachka mavjud")
        vertikal.addWidget(self.pachka)

        self.pachkamiqdor = QLineEdit(miqdor)
        self.pachkamiqdor.setPlaceholderText("1 pachkadagi miqdori(donada)")
        vertikal.addWidget(self.pachkamiqdor)

        self.kelgan = QLineEdit(kelgan)
        self.kelgan.setPlaceholderText("Nechta pachka kelgan")
        vertikal.addWidget(self.kelgan)

        btn = QPushButton("Qo'shish/Tahrirlash")
        garizontal.addWidget(btn)
        btn.clicked.connect(self.accept)

        btn1 = QPushButton("Ortga")
        garizontal.addWidget(btn1)
        btn1.clicked.connect(self.reject)

        vertikal.addItem(spacer())

        vertikal.addLayout(garizontal)

        self.setLayout(vertikal)
        self.setStyleSheet(edit_oyna)

    def get_values(self):
        nomi = self.nomi.text()
        xususiyati = self.xususiyati.text()
        kelishnarx = self.kelishnarx.text()
        sotilishnarx = self.sotilishnarx.text()
        pachka = self.pachka.text()
        pachkamiqdor = self.pachkamiqdor.text()
        kelgan = self.kelgan.text()

        dona = int(pachka) * int(pachkamiqdor)

        lt = [nomi, xususiyati, sotilishnarx, pachka, dona, pachkamiqdor, kelishnarx, kelgan]

        return lt


class DorilarHisobot(QMainWindow):
    def __init__(self, admin):
        super().__init__()
        self.admin = admin
        load_tables()

        self.dori_qoshish_oyna = None
        self.edit_oyna = None

        self.setWindowTitle("Dorilar hisoboti")

        vertikal = QVBoxLayout()
        garizontal1 = QHBoxLayout()
        garizontal2 = QHBoxLayout()

        self.qidiruv = QLineEdit()
        garizontal1.addWidget(self.qidiruv)
        self.qidiruv.setPlaceholderText("Qidiruv")
        self.qidiruv.returnPressed.connect(self.filter_bosildi)

        btn1 = QPushButton("Qidiruv")
        garizontal1.addWidget(btn1)
        btn1.clicked.connect(self.filter_bosildi)

        btn2 = QPushButton("Dori qo'shish")
        garizontal1.addWidget(btn2)
        btn2.clicked.connect(self.dori_qoshish_bosildi)

        vertikal.addLayout(garizontal1)

        label = QLabel("Filter")
        garizontal2.addWidget(label)

        lt = ["tanlov", "joriy oy", "Oxirgi oy", "Joriy Yillik", "Oxirgi Yillik"]

        self.filter = QComboBox()
        self.filter.addItems(lt)
        self.filter.activated.connect(self.filter_bosildi)
        garizontal2.addWidget(self.filter)
        garizontal2.addItem(hspacer())

        vertikal.addLayout(garizontal2)

        self.table = QTableWidget()
        vertikal.addWidget(self.table)

        garizontal3 = QHBoxLayout()
        self.sarmoya = QLabel("Kiritilgan sarmoya: 0 so'm")
        garizontal3.addWidget(self.sarmoya)
        garizontal3.addItem(hspacer())

        garizontal4 = QHBoxLayout()
        self.savdo = QLabel("Umumiy savdo: 0 so'm")
        garizontal4.addWidget(self.savdo)
        garizontal4.addItem(hspacer())

        garizontal5 = QHBoxLayout()
        self.foyda = QLabel("Sof foyda: 0 so'm")
        garizontal5.addWidget(self.foyda)
        garizontal5.addItem(hspacer())

        vertikal.addLayout(garizontal3)
        vertikal.addLayout(garizontal4)
        vertikal.addLayout(garizontal5)

        btn3 = QPushButton("Ortga qaytish")
        vertikal.addWidget(btn3)
        btn3.clicked.connect(self.ortga_qaytish)

        self.data = []

        self.summani_hisoblash()
        self.filter_bosildi()

        widget = QWidget()
        widget.setLayout(vertikal)
        self.setCentralWidget(widget)
        self.setStyleSheet(ishchilar_panel_css)

    def dori_qoshish_bosildi(self):
        self.dori_qoshish_oyna = DoriQoshish()

        if self.dori_qoshish_oyna.exec_() == QDialog.Accepted:
            try:
                malumotlar = self.dori_qoshish_oyna.get_values()

                # Narxlarni tekshirish va to'g'ri formatga o'tkazish
                kelishnarx = float(malumotlar[6])
                sotilishnarx = float(malumotlar[2])

                # Boshqa ma'lumotlarni olish
                nomi = malumotlar[0]
                xususiyati = malumotlar[1]
                pachka = int(malumotlar[3])
                dona = int(malumotlar[4])
                pachkamiqdor = int(malumotlar[5])
                kelgan = int(malumotlar[7])

                conn = get_connection()
                if not conn:
                    QMessageBox.critical(self, "Xatolik", "Bazaga ulanishda xatolik yuz berdi.")
                    return

                cur = conn.cursor()

                cur.execute("""select * from dorilar where nomi=%s""", (nomi,))
                tekshiruv = cur.fetchone()

                if tekshiruv is None and len(nomi) > 0 and len(xususiyati) > 0:
                    cur.execute("""insert into dorilar (nomi, xususiyati, narxi, pachka, dona, bir_pochka_miqdori, 
                                    kelish_narx, nechta_kelgan) 
                                    values (%s, %s, %s, %s, %s, %s, %s, %s);""",
                                (nomi, xususiyati, sotilishnarx, pachka, dona, pachkamiqdor, kelishnarx, kelgan))
                    conn.commit()
                    QMessageBox.information(self, "Muvaffaqiyatli", "Dori muvaffaqiyatli qo'shildi")
                else:
                    QMessageBox.warning(self, "Ogohlantirish",
                                        "Bunday nomdagi dori mavjud yoki siz hech narsa kiritmadingiz, iltimos boshqa "
                                        "nom bilan kiriting")

                cur.close()
                conn.close()

                self.filter_bosildi()
                self.summani_hisoblash()

            except ValueError:
                QMessageBox.warning(self, "Xatolik", "Narxlarni to'g'ri formatda kiriting (faqat sonlar).")
            except Exception as e:
                QMessageBox.critical(self, "Xatolik", f"Kutilmagan xatolik: {e}")

    def edit_bosildi(self, kerakli):
        kerakli = [str(x) for x in kerakli]  # Decimal va boshqa turlarni stringga o'zgartirish

        # Dori nomi orqali id ni aniqlash
        try:
            dori_nomi = kerakli[0]  # kerakli[0] - dori nomi
            conn = get_connection()
            cur = conn.cursor()

            cur.execute("SELECT id FROM dorilar WHERE nomi = %s", (dori_nomi,))
            result = cur.fetchone()

            if result is None:
                QMessageBox.warning(self, "Xatolik", f"Dori uchun ID topilmadi: {dori_nomi}")
                return

            dori_id = result[0]  # ID ni aniqladik

            # Tahrirlash oynasini ochish
            self.edit_oyna = DoriQoshish(
                nomi=kerakli[0],
                xusus=kerakli[1],
                kelish=kerakli[2],
                sotil=kerakli[3],
                pachka=kerakli[5],
                miqdor=kerakli[7],
                kelgan=kerakli[4]
            )

            if self.edit_oyna.exec_() == QDialog.Accepted:
                malumotlar = self.edit_oyna.get_values()

                kelishnarx = float(malumotlar[6])
                sotilishnarx = float(malumotlar[2])
                nomi = malumotlar[0]
                xususiyati = malumotlar[1]
                pachka = int(malumotlar[3])
                dona = int(malumotlar[4])
                pachkamiqdor = int(malumotlar[5])
                kelgan = int(malumotlar[7])

                # Dori ma'lumotlarini yangilash
                cur.execute("""UPDATE dorilar SET nomi=%s, xususiyati=%s, narxi=%s, pachka=%s, dona=%s, 
                                bir_pochka_miqdori=%s, kelish_narx=%s, nechta_kelgan=%s WHERE id=%s""",
                            (nomi, xususiyati, sotilishnarx, pachka, dona, pachkamiqdor, kelishnarx, kelgan, dori_id))
                conn.commit()

                QMessageBox.information(self, "Muvaffaqiyatli", "Dori muvaffaqiyatli tahrirlandi")

                # Ma'lumotlar bazasidan oxirgi ma'lumotlarni qayta yuklash
                self.filter_bosildi()
                self.summani_hisoblash()

            cur.close()
            conn.close()

        except ValueError:
            QMessageBox.warning(self, "Xatolik", "Narxlarni to'g'ri formatda kiriting (faqat sonlar).")
        except Exception as e:
            QMessageBox.critical(self, "Xatolik", f"Kutilmagan xatolik: {e}")

    def delete_bosildi(self, kerakli):
        if QMessageBox.question(self, "Tasdiqlash", "Dorini o'chirib tashlashni tasdiqlaysizmi?") == QMessageBox.Yes:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute("""delete from dorilar where nomi=%s""", (kerakli,))

            conn.commit()

            self.filter_bosildi()
            self.summani_hisoblash()

            QMessageBox.information(self, "Muvaffaqiyatli", "Dori muvaffaqiyatli o'chirib tashlandi")

            cur.close()
            conn.close()

    def summani_hisoblash(self):

        sarmoya = 0
        umumiy = 0
        foyda = 0

        for item in self.data:
            lt = item[8].split()
            sarmoya += float(item[2]) * int(item[4])
            umumiy += int(lt[0]) * int(item[3]) + int(lt[-2]) * (float(item[3]) / float(item[7]))
            foyda += float(item[9])

        self.sarmoya.setText(f"Kiritilgan sarmoya: {round(sarmoya, 2)} so'm")
        self.savdo.setText(f"Umumiy savdo: {round(umumiy, 2)} so'm")
        self.foyda.setText(f"Sof foyda: {round(foyda, 2)} so'm")

    def filter_bosildi(self):
        conn = get_connection()
        cur = conn.cursor()

        lt = ["tanlov", "joriy oy", "Oxirgi oy", "Joriy Yillik", "Oxirgi Yillik"]
        tekshirish = self.filter.currentText()
        nomi = self.qidiruv.text()

        if tekshirish == lt[0]:
            cur.execute("""SELECT nomi, xususiyati, narxi,
                        pachka, dona, bir_pochka_miqdori, kelish_narx, nechta_kelgan
                        FROM dorilar where nomi like %s """, (f"%{nomi}%",))

        else:

            cur.execute("""SELECT DISTINCT dorilar.nomi, dorilar.xususiyati, dorilar.narxi,
                        dorilar.pachka, dorilar.dona, dorilar.bir_pochka_miqdori, dorilar.kelish_narx,
                        dorilar.nechta_kelgan
                        FROM dorilar
                        WHERE EXISTS (
                        SELECT 1
                        FROM sotilgan_dorilar
                        WHERE dorilar.nomi = sotilgan_dorilar.dori_nomi and dorilar.nomi like %s
                        );
                    """, (f"%{nomi}%",))
        dori = cur.fetchall()

        self.data = []

        for malumot in dori:

            miqdor = 0

            if tekshirish == lt[0]:
                cur.execute("""select sotilgan_dona from sotilgan_dorilar where dori_nomi=%s""", (malumot[0],))
            elif tekshirish == lt[1]:
                cur.execute("""select sotilgan_dona from sotilgan_dorilar where dori_nomi=%s 
                            and MONTH(sotilgan_vaqt)=MONTH(CURRENT_DATE()) and 
                            YEAR(sotilgan_vaqt)=YEAR(CURRENT_DATE());""", (malumot[0],))
            elif tekshirish == lt[2]:
                cur.execute("""select sotilgan_dona from sotilgan_dorilar where dori_nomi=%s 
                            and MONTH(sotilgan_vaqt)=MONTH(CURRENT_DATE() - INTERVAL 1 MONTH) and 
                            YEAR(sotilgan_vaqt)=YEAR(CURRENT_DATE());""", (malumot[0],))
            elif tekshirish == lt[3]:
                cur.execute("""select sotilgan_dona from sotilgan_dorilar where dori_nomi=%s 
                            and YEAR(sotilgan_vaqt)=YEAR(CURRENT_DATE());""", (malumot[0],))
            elif tekshirish == lt[4]:
                cur.execute("""select sotilgan_dona from sotilgan_dorilar where dori_nomi=%s 
                            and YEAR(sotilgan_vaqt)=YEAR(CURRENT_DATE() - INTERVAL 1 YEAR);""", (malumot[0],))
            temp = cur.fetchall()

            for i in temp:
                miqdor += int(i[0])

            cur.execute("""select bir_pochka_miqdori from dorilar where nomi=%s""", (malumot[0],))
            birpachka = cur.fetchone()

            pachka = miqdor // int(birpachka[0])
            dona = miqdor - pachka * int(birpachka[0])

            sotilgan = f"{pachka} pachka, {dona} dona"

            farq = float(malumot[2]) - float(malumot[6])
            foyda = pachka * farq + dona * (farq / int(malumot[6]))

            temp1 = list(malumot[:2]) + [malumot[6]] + [malumot[2]] + [malumot[7]] + list(malumot[3:6]) + [sotilgan] + [round(foyda, 2)]

            if tekshirish == lt[0]:
                self.data.append(temp1)
            elif foyda > 0:
                self.data.append(temp1)

        self.table.setRowCount(len(self.data))
        self.table.setColumnCount(11)

        header_list = ['Dori nomi', 'xususiyati', 'kelish narxi', 'sotilish narxi', 'nechta pachka kelgan', 'qolgan pachka',
                       'dona', '1 pachka miqdori', 'sotilgani', 'foyda', 'boshqaruv']

        self.table.setHorizontalHeaderLabels(header_list)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for i, malumot in enumerate(self.data):
            for j, curr in enumerate(malumot):
                item = QTableWidgetItem(str(curr))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Tahrirlanmas qilish
                self.table.setItem(i, j, item)

            garizontal = QHBoxLayout()
            widget = QWidget()
            edit = QPushButton("Edit")
            edit.clicked.connect(lambda checked, kerakli=malumot[:8]: self.edit_bosildi(kerakli))
            delete = QPushButton("Delete")
            delete.setMinimumWidth(74)
            delete.clicked.connect(lambda checked, kerakli=malumot[0]: self.delete_bosildi(kerakli))
            garizontal.addWidget(edit)
            garizontal.addWidget(delete)
            widget.setLayout(garizontal)
            widget.setMinimumHeight(80)
            self.table.setCellWidget(i, 10, widget)
            self.table.setRowHeight(i, 90)

        self.summani_hisoblash()

    def ortga_qaytish(self):
        self.admin.showMaximized()
        self.close()


