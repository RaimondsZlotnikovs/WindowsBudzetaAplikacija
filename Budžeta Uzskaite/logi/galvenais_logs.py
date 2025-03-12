import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from dizains.stils import get_stils
from logi.izdevumu_logs import IzdevumuLogs
from logi.ienakumu_logs import IenakumuLogs
from dati.bilance import generet_parskatu
from logi.parskata_logs import ParskataLogs
from logi.pieslegsanas_logs import PieslegsanasLogs

# Galvenā loga klase
class BudzetaAplikacija(QMainWindow):
    def __init__(self, lietotaja_id):                               # Konstruktors
        super().__init__()                                          # Superklases konstruktors
        self.lietotaja_id = lietotaja_id                            # Saglabā lietotāja id
        self.setWindowTitle("Budžeta aplikācija")                   # Loga nosaukums
        self.setGeometry(100, 100, 400, 600)                        # Loga izmēri
        self.setStyleSheet(get_stils())                             # Iestata dizaina stilus
        self.init_ui()                                              # Izsauc funkciju init_ui
    
    def init_ui(self):
        layout = QVBoxLayout()                                      # Izveido vertikālu izkārtojumu

        # Izveido teksta logu ar bilanci
        self.bilance_label = QLabel(self.lasi_bilanci(), self)      # Iegūst bilances vērtību un izveido teksta logu
        self.bilance_label.setAlignment(Qt.AlignCenter)             # Teksta loga centralizēšana
        self.bilance_label.setFont(QFont("Arial", 12))              # Teksta loga fonta izmērs
        self.bilance_label.setStyleSheet("font-size: 35px;")        # Teksta loga fonta izmērs
        layout.addWidget(self.bilance_label)                        # Pievieno teksta logu izkārtojumam

        # Poga ienākumu pievienošanai
        self.ienakumi_poga = QPushButton("Pievienot ienākumus", self)       # Izveido pogu
        self.ienakumi_poga.clicked.connect(self.atvert_ienakumu_logu)       # Pievieno pogai funkciju

        # Poga izdevumu pievienošanai     
        self.izdevumi_poga = QPushButton("Pievienot izdevumus", self)       # Izveido pogu
        self.izdevumi_poga.clicked.connect(self.atvert_izdevumu_logu)       # Pievieno pogai funkciju


        # Poga budžeta pārskata apskatei
        self.parskats_poga = QPushButton("Apskatīt pārskatu", self)     # Izveido pogu
        self.parskats_poga.clicked.connect(self.paradi_parskatu)        # Pievieno pogai funkciju

        # Poga iziešanai no konta
        self.iziet_poga = QPushButton("Iziet", self)                # Izveido pogu
        self.iziet_poga.clicked.connect(self.iziet_no_konta)        # Pievieno pogai funkciju
        
        # Pievieno visas pogas izkārtojumam
        for poga in [self.ienakumi_poga, self.izdevumi_poga, self.parskats_poga, self.iziet_poga]:  # Pārbauda visas pogas
            poga.setFont(QFont("Arial", 12))                                                        # Pogas fonta izmērs
            layout.addWidget(poga)                                                                  # Pievieno pogu izkārtojumam
        
        # Izveido centrālo konteineru un piešķir tam izkārtojumu
        konteineris = QWidget()                                         # Izveido konteineru
        konteineris.setLayout(layout)                                   # Piešķir konteineram izkārtojumu
        self.setCentralWidget(konteineris)                              # Izveido centrālo konteineru

    # Atver ienākumu logu
    def atvert_ienakumu_logu(self):
        self.ienakumu_logs = IenakumuLogs(self.lietotaja_id)     # Izveido ienākumu logu
        self.ienakumu_logs.exec_()                               # Atver logu
        self.bilance_label.setText(self.lasi_bilanci())          # Atjauno bilances tekstu

    # Atver izdevumu logu   
    def atvert_izdevumu_logu(self):                             # Izveido funkciju atvert_izdevumu_logu
        self.izdevumu_logs = IzdevumuLogs(self.lietotaja_id)    # Izveido izdevumu logu
        self.izdevumu_logs.exec_()                              # Atver logu
        self.bilance_label.setText(self.lasi_bilanci())         # Atjauno bilances tekstu

    # Atgriež bilances vērtību
    def lasi_bilanci(self):                                # Izveido funkciju lasi_bilanci
        dati_bilance = generet_parskatu(self.lietotaja_id) # Iegūst bilances datus pēc pieslēgušos lietotāja
        return f"{dati_bilance.split(", ")[-1]} €"         # Atgriež tikai bilances vērtību
    
    # Atver budžeta pārskata logu
    def paradi_parskatu(self):                                      # Izveido funkciju paradi_parskatu
        self.hide()                                                 # Paslēpj galveno logu
        self.parskata_logs = ParskataLogs(self.lietotaja_id, self)  # Izveido pārskata logu
        self.parskata_logs.exec_()                                  # Atver logu
        self.bilance_label.setText(self.lasi_bilanci())             # Atjauno bilances tekstu

    def iziet_no_konta(self):       # Izveido funkciju iziet_no_konta
        self.close()                # Aizver pašreizējo galveno logu

        pieslegsanas_logs = PieslegsanasLogs()             # Izveido pieslēgšanās logu
        if pieslegsanas_logs.exec_() == QDialog.Accepted:  # Ja lietotājs veiksmīgi pieslēdzas
            self.__init__(pieslegsanas_logs.lietotaja_id)  # Restartē galveno logu ar jaunu lietotāju
            self.show()                                    # Parāda jauno galveno logu


if __name__ == "__main__":                                  # Pārbauda vai fails tiek izpildīts tieši     
    app = QApplication(sys.argv)                            # Izveido aplikācijas instanci
    pieslegsanas_logs = PieslegsanasLogs()                  # Izveido pieslēgšanās logu
    
    if pieslegsanas_logs.exec_() == QDialog.Accepted:                           # Ja lietotājs veiksmīgi pieslēdzas
        lietotaja_id = pieslegsanas_logs.lietotaja_id                           # Saglabā lietotāja id
        galvenais_logs = BudzetaAplikacija(lietotaja_id, pieslegsanas_logs)     # Izveido galveno logu
        galvenais_logs.show()                                                   # Parāda galveno logu
    
    sys.exit(app.exec_())      # Iziet no aplikācijas
