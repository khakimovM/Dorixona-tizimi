import mysql.connector as connector

DATABASE = "Apteka"


def get_connection():
    try:
        return connector.connect(
            host='localhost',
            user='root',
            password='aziz1707',
            database=DATABASE
        )
    except connector.Error as e:
        print("Databasaga ulanishda xatolik bor")
        print(e)


def create_db():
    try:
        conn = connector.connect(
            host='localhost',
            user='root',
            password='aziz1707'
        )
        cur = conn.cursor()

        cur.execute(f"""create database if not exists {DATABASE};""")

        conn.commit()

        cur.close()
        conn.close()

    except connector.Error as e:
        print("Databasa yaratishda xatolik bor")
        print(e)


def load_tables():
    create_db()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""create table if not exists dorilar(
        id int primary key auto_increment,
        nomi varchar(50) unique not NULL,
        xususiyati varchar(255) not NULL,
        narxi int not NULL,
        pachka int not NULL,
        dona bigint not NULL,
        bir_pochka_miqdori int not NULL,
        kelish_narx int not NULL,
        nechta_kelgan int not NULL
    );""")

    conn.commit()

    # cur.execute("""INSERT IGNORE INTO dorilar (nomi, xususiyati, narxi, pachka, dona, bir_pochka_miqdori, kelish_narx,
    #         nechta_kelgan)
    #     VALUES
    #     ('Aspirin', 'Ogriq qoldiruvchi va yalliglanishga qarshi vosita', 10000, 10, 200, 20, 6000, 15),
    #     ('Paracetamol', 'Isitma tushiruvchi va ogriq qoldiruvchi', 4000, 15, 150, 10, 1800, 20),
    #     ('Ibuprofen', 'Yalliglanishga qarshi va ogriq qoldiruvchi', 35000, 20, 500, 25, 16000, 25),
    #     ('Amoxicillin', 'Antibiotik', 8000, 5, 50, 10, 5000, 7),
    #     ('Ciprofloxacin', 'Antibiotik', 30000, 8, 80, 10, 25000, 10),
    #     ('Metformin', 'Qandli diabet dori', 18500, 12, 144, 12, 12000, 20),
    #     ('Lisinopril', 'Qon bosimi dori', 16000, 7, 210, 30, 10000, 15),
    #     ('Omeprazole', 'Qorin ogrigi va oshqozon dorisi', 20000, 9, 90, 10, 14500, 10),
    #     ('Simvastatin', 'Xolesterinni tushiruvchi dori', 34000, 6, 180, 30, 18000, 10),
    #     ('Losartan', 'Qon bosimini tushiruvchi dori', 50000, 11, 220, 20, 32000, 15),
    #     ('Azithromycin', 'Keng tasir doirasiga ega antibiotik', 65000, 4, 12, 3, 40000, 10),
    #     ('Cetirizine', 'Allergiyaga qarshi dori', 35000, 13, 520, 40, 15000, 20),
    #     ('Furosemide', 'Suv ajratib chiqaruvchi dori', 13000, 18, 180, 10, 8000, 30),
    #     ('Warfarin', 'Qon quyulishiga qarshi dori', 45000, 9, 180, 20, 32000, 25),
    #     ('Levothyroxine', 'Qalqonsimon bez dori', 17000, 10, 200, 20, 10000, 15);
    # """)
    #
    # conn.commit()

    cur.execute("""create table if not exists users(
        id int primary key auto_increment,
        ismi varchar(70) not NULL unique,
        password varchar(20) not NULL,
        lavozimi varchar(50),
        qabul_qilingan_sana datetime default now()
    );""")

    conn.commit()

    cur.execute("""insert ignore into users(ismi, password, lavozimi, qabul_qilingan_sana) values
        ('admin', '1234', 'Admin', '2020-10-01 09:15:00'),
        ('root', '1234', 'Ishchi', '2023-07-01 09:15:00'),
        ('aziz', '1234', 'Ishchi', '2024-02-01 09:15:00');
    """)

    conn.commit()

    cur.execute("""create table if not exists sotilgan_dorilar(
        id bigint primary key auto_increment,
        sotuvchi varchar(70) not NULL,
        dori_nomi varchar(70) not NULL,
        sotilgan_dona varchar(50) not NULL,
        sotilgan_summa varchar(70) not NULL,
        sotilgan_vaqt datetime default now()
    );""")

    # cur.execute("""INSERT INTO sotilgan_dorilar (sotuvchi, dori_nomi,sotilgan_dona, sotilgan_summa, sotilgan_vaqt)
    # VALUES
    # ('aziz', 'Omeprazole', '10', '150000', '2024-11-01 09:15:00'),
    # ('root', 'Metformin','7', '105000', '2024-10-02 14:30:00'),
    # ('aziz', 'Paracetamol','15', '225000', '2024-11-03 11:45:00'),
    # ('root', 'Omeprazole','20', '300000', '2024-10-04 10:20:00'),
    # ('aziz', 'Metformin','12', '180000', '2024-11-05 13:50:00'),
    # ('root', 'Paracetamol','5', '75000', '2024-10-06 08:00:00'),
    # ('aziz', 'Omeprazole','8', '120000', '2024-11-07 15:35:00'),
    # ('root', 'Metformin','6', '90000', '2024-10-08 16:10:00'),
    # ('aziz', 'Paracetamol','13', '195000', '2024-11-09 12:25:00'),
    # ('root', 'Omeprazole','9', '135000', '2024-10-10 09:50:00');
    #     """)

    conn.commit()

    cur.close()
    conn.close()
