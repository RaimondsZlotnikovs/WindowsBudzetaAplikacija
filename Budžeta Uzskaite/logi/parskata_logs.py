from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QCheckBox, QScrollArea
from dati.datubaze import Ienakumi, Izdevumi, Kategorija, sesija
from PyQt5.QtCore import Qt
from dizains.stils import get_stils
from functools import partial

class ParskataLogs(QDialog):
    def __init__(self, lietotaja_id, vecais_logs):
        super().__init__()
        self.lietotaja_id = lietotaja_id
        self.vecais_logs = vecais_logs
        self.setWindowTitle("Budžeta pārskats")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)   # Noņemt jautājuma zīmi loga stūrī
        self.setGeometry(150, 150, 400, 500)
        self.setStyleSheet(get_stils())
        self.atzimetie_ieraksti = []
        self.filtrs = "visi"

        self.init_ui()
    
    def init_ui(self):
        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel("Budžeta pārskats", alignment=Qt.AlignCenter))
        
        self.filtru_rinda = QHBoxLayout()
        self.ienakumi_poga = QPushButton("Ienākumi")
        self.ienakumi_poga.clicked.connect(lambda: self.filtrēt("ienakumi"))
        self.izdevumi_poga = QPushButton("Izdevumi")
        self.izdevumi_poga.clicked.connect(lambda: self.filtrēt("izdevumi"))
        self.visi_poga = QPushButton("Visi")
        self.visi_poga.clicked.connect(lambda: self.filtrēt("visi"))
        
        self.filtru_rinda.addWidget(self.ienakumi_poga)
        self.filtru_rinda.addWidget(self.izdevumi_poga)
        self.filtru_rinda.addWidget(self.visi_poga)
        self.layout.addLayout(self.filtru_rinda)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(self.scroll_area)
        
        self.dzesanas_poga = QPushButton("Dzēst atzīmētos")
        self.dzesanas_poga.clicked.connect(self.dzest_atzimetos)
        self.layout.addWidget(self.dzesanas_poga)
        
        self.atpakal_poga = QPushButton("Atpakaļ")
        self.atpakal_poga.clicked.connect(self.atgriezties)
        self.layout.addWidget(self.atpakal_poga)

        self.setLayout(self.layout)
        self.paradit_parskatu()

    # Parāda ienākumus un izdevumus uz ekrāna
    def paradit_parskatu(self):
        ienakumi = sesija.query(Ienakumi).filter_by(lietotaja_id=self.lietotaja_id).order_by(Ienakumi.datums.desc()).all()  # Sakārto pēc datuma dilstoši
        izdevumi = sesija.query(Izdevumi).filter_by(lietotaja_id=self.lietotaja_id).order_by(Izdevumi.datums.desc()).all() 

        for i in reversed(range(self.scroll_layout.count())):
            self.scroll_layout.itemAt(i).widget().deleteLater() # Notīra visus iepriekšējos ierakstus
        
        if self.filtrs == "visi" or self.filtrs == "ienakumi":  # Parāda tikai ienākumus, ja filtrs ir ienākumi
            self.pievienot_ierakstus("IENĀKUMI:", ienakumi)
        if self.filtrs == "visi" or self.filtrs == "izdevumi":  # Parāda tikai izdevumus, ja filtrs ir izdevumi
            self.pievienot_ierakstus("IZDEVUMI:", izdevumi)

    # Pievieno ierakstus uz ekrāna
    def pievienot_ierakstus(self, virsraksts, ieraksti):    
        self.scroll_layout.addWidget(QLabel(virsraksts))
        for ieraksts in ieraksti:
            ieraksta_widget = QWidget()
            ieraksta_layout = QHBoxLayout()

            checkbox = QCheckBox()
            checkbox.stateChanged.connect(partial(self.atzimet_ierakstu, ieraksts))

            # Iegūt kategorijas nosaukumu no saistītās tabulas
            kategorija = sesija.query(Kategorija).filter_by(id=ieraksts.kategorija_id).first()
            kategorijas_nosaukums = kategorija.nosaukums if kategorija else "Nezināma kategorija"

            etikete = QLabel(f"{ieraksts.datums} - {ieraksts.summa} EUR ({kategorijas_nosaukums})")

            ieraksta_layout.addWidget(checkbox)
            ieraksta_layout.addWidget(etikete)
            ieraksta_widget.setLayout(ieraksta_layout)
            self.scroll_layout.addWidget(ieraksta_widget)

    # Filtrē ienākumus un izdevumus
    def filtrēt(self, tips):
        self.filtrs = tips
        self.paradit_parskatu()
    
    # Atzīmē ierakstu, lai to varētu dzēst
    def atzimet_ierakstu(self, ieraksts):
        if ieraksts in self.atzimetie_ieraksti:
            self.atzimetie_ieraksti.remove(ieraksts)
        else:
            self.atzimetie_ieraksti.append(ieraksts)
    
    # Dzēš atzīmētos ierakstus
    def dzest_atzimetos(self):
        for ieraksts in self.atzimetie_ieraksti:
            sesija.delete(ieraksts)
        sesija.commit()
        self.atzimetie_ieraksti.clear()  # Tīrām sarakstu
        self.paradit_parskatu()
    
    # Aizver logu un atgriežas pie galvenā loga
    def atgriezties(self):
        self.close()
        if not self.vecais_logs.isVisible():
            self.vecais_logs.show()
