kirish = """
    QMainWindow {
        background-color: #f2f7fc; /* Yengil ko'k */
    }
    QLineEdit {
        border: 2px solid #a8d0db; /* Yashil-kulrang */
        border-radius: 10px;
        padding: 8px;
        font-size: 14px;
        background: #ffffff; /* Oq */
        color: #333333; /* To'q kulrang */
    }
    QLineEdit:focus {
        border: 2px solid #6cb4b8; /* Faol element uchun to'q yashil */
    }
    QPushButton {
        background-color: #6cb4b8; /* To'q yashil */
        border: none;
        color: white;
        padding: 10px 20px;
        border-radius: 10px;
        font-size: 14px;
    }
    QPushButton:hover {
        background-color: #4a8a8f; /* Qorong'i yashil */
    }
    QPushButton:pressed {
        background-color: #356d71; /* Eng qorong'i yashil */
    }
    QMessageBox {
        background-color: #fefefe; /* Yengil oq */
        color: #333333; /* Matn uchun to'q kulrang */
    }
    """

admin = """
    QMainWindow {
        background-color: #eef5fa; /* Yengil ko'k */
    }
    QPushButton {
        background-color: #5aa897; /* Yashil */
        border: 2px solid #4d907e; /* Tugma chegarasi */
        color: #ffffff; /* Matn rangi - oq (doim ko'rinadi) */
        padding: 12px 24px;
        border-radius: 10px;
        font-size: 14px;
        font-weight: bold;
        margin: 10px;
    }
    QPushButton:hover {
        background-color: #4d907e; /* Qorong'i yashil */
        color: #ffffff; /* Hover holatda matn rangi o'zgarishsiz qoladi */
    }
    QPushButton:pressed {
        background-color: #40766d; /* Eng qorong'i yashil */
        color: #ffffff; /* Tugma bosilganda matn rangi o'zgarishsiz qoladi */
    }
    """

ishchilar_panel_css = """
    QMainWindow {
        background-color: #f7f9fc; /* Yengil oqish-ko'k rang */
    }

    QLineEdit {
        border: 2px solid #a8d0db; /* Yengil ko'k chegara */
        border-radius: 8px;
        padding: 10px;
        font-size: 14px;
        background: #ffffff; /* Oq */
        color: #333333; /* To'q kulrang matn */
    }
    QLineEdit:focus {
        border: 2px solid #5aa897; /* Faol holatda yashil */
    }

    QPushButton {
        background-color: #5aa897; /* Yashil */
        color: white; /* Oq matn */
        padding: 12px 15px;
        font-size: 14px;
        font-weight: bold;
        border-radius: 10px;
        border: 1px solid #4d907e; /* Tugma chegarasi */
    }
    QPushButton:hover {
        background-color: #4d907e; /* Qorong'i yashil */
    }
    QPushButton:pressed {
        background-color: #356d71; /* Eng qorong'i yashil */
    }

    QLabel {
        font-size: 16px;
        font-weight: bold;
        color: #333333; /* To'q kulrang matn */
    }

    QComboBox {
        background-color: #ffffff;
        border: 2px solid #a8d0db; /* Ko'k chegara */
        border-radius: 8px;
        padding: 6px;
        font-size: 14px;
        color: #333333; /* To'q kulrang matn */
    }
    QComboBox:focus {
        border: 2px solid #5aa897; /* Faol holatda yashil */
    }

    QTableWidget {
                background-color: #f7f9fc;  /* Jadval foni */
                border: 2px solid #a8d0db;
                gridline-color: #a8d0db;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 8px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #008B8B;  /* To'q kulrang fon */
                color: #ffffff;  /* Oq matn */
            }
            QHeaderView::section {
                background-color: #2d3748;  /* Sarlavha foni */
                color: #ffffff;  /* Sarlavha matni */
                font-size: 14px;
                padding: 5px;
                border: 1px solid #a8d0db;
            }
    QHeaderView::section {
        background-color: #5aa897; /* Yashil fon */
        color: white; /* Oq matn */
        font-size: 14px;
        font-weight: bold;
        border: 1px solid #4d907e;
        padding: 5px;
    }

    QMessageBox {
        background-color: #f7f9fc; /* Yengil oqish-ko'k fon */
        border: 2px solid #a8d0db; /* Ko'k chegara */
        border-radius: 8px;
        color: #333333; /* Matn rangi */
    }
"""

edit_oyna = """
            QDialog {
                background-color: #f7f9fc;  /* Yengil ko'k fon */
                border-radius: 10px;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333333;  /* To'q kulrang matn */
            }
            QLineEdit {
                border: 2px solid #a8d0db;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                background-color: #ffffff;
                color: #333333;
            }
            QLineEdit:focus {
                border: 2px solid #5aa897;  /* Yashil rang */
            }
            QComboBox {
                border: 2px solid #a8d0db;
                border-radius: 8px;
                padding: 6px;
                font-size: 14px;
                background-color: #ffffff;
                color: #333333;
            }
            QComboBox:focus {
                border: 2px solid #5aa897;
            }
            QPushButton {
                background-color: #5aa897;  /* Yashil rang */
                color: white;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4d907e;  /* Qorong'i yashil */
            }
            QPushButton:pressed {
                background-color: #356d71;  /* Eng qorong'i yashil */
            }
        """
qlistwidget_css = """
    QListWidget {
        background-color: #f7f9fc;  /* Yengil oqish-ko'k fon */
        border: 2px solid #a8d0db;  /* Yengil ko'k chegara */
        border-radius: 8px;
        padding: 8px;
        font-size: 14px;
        color: #333333;  /* To'q kulrang matn */
    }
    QListWidget::item {
        padding: 10px;
        margin: 4px;
        border: 1px solid transparent;  /* Standart holatda chegara ko'rinmaydi */
        border-radius: 6px;
        background-color: #ffffff;  /* Oq element foni */
    }
    QListWidget::item:hover {
        background-color: #d0f0ed;  /* Yengil yashil fon */
        border: 1px solid #5aa897;  /* Ko'k-yashil chegara */
    }
    QListWidget::item:selected {
        background-color: #5aa897;  /* Yashil fon */
        color: white;  /* Oq matn */
        border: 1px solid #4d907e;  /* Qorong'i yashil chegara */
    }
    QListWidget::item:selected:active {
        background-color: #356d71;  /* Eng qorong'i yashil fon */
    }
    QScrollBar:vertical {
        background: #eef5fa;  /* Yengil ko'k fon */
        width: 10px;
        margin: 2px;
        border-radius: 5px;
    }
    QScrollBar::handle:vertical {
        background: #5aa897;  /* Yashil tutqich */
        min-height: 20px;
        border-radius: 5px;
    }
    QScrollBar::handle:vertical:hover {
        background: #4d907e;  /* Qorong'i yashil */
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        border: none;
        background: none;
    }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
    }
"""
