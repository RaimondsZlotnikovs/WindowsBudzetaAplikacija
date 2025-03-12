from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QDateEdit, QComboBox
from PyQt5.QtCore import QDate, Qt
from dati.datubaze import Izdevumi, Kategorija, sesija
from dizains.stils import get_stils

class IzdevumuLogs(QDialog):
    def __init__(self, lietotaja_id):
        super().__init__()
        self.lietotaja_id = lietotaja_id
        self.setWindowTitle("Pievienot izdevumus")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setGeometry(150, 150, 300, 250)
        self.setStyleSheet(get_stils())
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.summa_label = QLabel("Izdevumu summa:")
        self.summa_ievade = QLineEdit()

        self.datums_label = QLabel("Datums:")
        self.datums_ievade = QDateEdit()
        self.datums_ievade.setCalendarPopup(True)
        self.datums_ievade.setDate(QDate.currentDate())
        self.datums_ievade.setMaximumDate(QDate.currentDate())

        self.jauna_kategorija_label = QLabel("Jauna kategorija:")
        self.jauna_kategorija_ievade = QLineEdit()

        self.pievienot_kategoriju_poga = QPushButton("Pievienot kategoriju")
        self.pievienot_kategoriju_poga.clicked.connect(self.pievienot_kategoriju)

        layout.addWidget(self.jauna_kategorija_label)
        layout.addWidget(self.jauna_kategorija_ievade)
        layout.addWidget(self.pievienot_kategoriju_poga)

        self.kategorija_label = QLabel("Kategorija:")
        self.kategorija_ievade = QComboBox()
        self.ieladet_kategorijas()

        self.pievienot_poga = QPushButton("Saglabāt")
        self.pievienot_poga.clicked.connect(self.saglabat_izdevumu)

        layout.addWidget(self.summa_label)
        layout.addWidget(self.summa_ievade)
        layout.addWidget(self.datums_label)
        layout.addWidget(self.datums_ievade)
        layout.addWidget(self.kategorija_label)
        layout.addWidget(self.kategorija_ievade)
        layout.addWidget(self.pievienot_poga)

        self.setLayout(layout)

    def pievienot_kategoriju(self):
        jaunais_nosaukums = self.jauna_kategorija_ievade.text().strip()
    
        if not jaunais_nosaukums:
            QMessageBox.warning(self, "Kļūda", "Kategorijas nosaukums nevar būt tukšs!")
            return

        # Pārbauda, vai kategorija jau eksistē
        ekzistejosa = sesija.query(Kategorija).filter_by(nosaukums=jaunais_nosaukums, veids="izdevumi").first()
        if ekzistejosa:
            QMessageBox.warning(self, "Kļūda", "Šāda kategorija jau pastāv!")
            return

        # Izveido jaunu kategoriju un saglabāt datubāzē
        jauna_kategorija = Kategorija(nosaukums=jaunais_nosaukums, veids="izdevumi")
        sesija.add(jauna_kategorija)
        sesija.commit()

        # Atjaunina kategoriju izvēlni
        self.ieladet_kategorijas()

        # Notīra ievades lauku
        self.jauna_kategorija_ievade.clear()

    def ieladet_kategorijas(self):
        self.kategorija_ievade.clear()  # Notīra esošās opcijas
        kategorijas = sesija.query(Kategorija).filter_by(veids="izdevumi").all()
        for kat in kategorijas:
            self.kategorija_ievade.addItem(kat.nosaukums, kat.id)

    def saglabat_izdevumu(self):
        try:
            summa = float(self.summa_ievade.text())
            datums = self.datums_ievade.date().toPyDate()
            kategorija_id = self.kategorija_ievade.currentData()

            if summa <= 0:
                raise ValueError("Summai jābūt pozitīvai!")

            jauns_izdevums = Izdevumi(lietotaja_id=self.lietotaja_id, summa=summa, datums=datums, kategorija_id=kategorija_id)
            sesija.add(jauns_izdevums)
            sesija.commit()

            self.close()
        except ValueError as e:
            QMessageBox.warning(self, "Kļūda", str(e))