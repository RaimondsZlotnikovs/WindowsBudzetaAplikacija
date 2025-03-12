from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from dati.datubaze import Lietotajs, sesija
from dizains.stils import get_stils
from PyQt5.QtCore import Qt

class PieslegsanasLogs(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pieslēgšanās")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setGeometry(100, 100, 300, 200)
        self.setStyleSheet(get_stils()) 
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        self.lietotajvards_label = QLabel("Lietotājvārds:")
        self.lietotajvards_ievade = QLineEdit()
        
        self.parole_label = QLabel("Parole:")
        self.parole_ievade = QLineEdit()
        self.parole_ievade.setEchoMode(QLineEdit.Password)
        
        self.pieslegties_poga = QPushButton("Pieslēgties")
        self.pieslegties_poga.clicked.connect(self.pieslegties)
        
        self.registreties_poga = QPushButton("Reģistrēties")
        self.registreties_poga.clicked.connect(self.registreties)
        
        layout.addWidget(self.lietotajvards_label)
        layout.addWidget(self.lietotajvards_ievade)
        layout.addWidget(self.parole_label)
        layout.addWidget(self.parole_ievade)
        layout.addWidget(self.pieslegties_poga)
        layout.addWidget(self.registreties_poga)
        
        self.setLayout(layout)

    # Funkcija, kas tiek izsaukta, kad lietotājs nospiež "Pieslēgties" pogu
    def pieslegties(self):
        lietotajvards = self.lietotajvards_ievade.text().strip()    # Iegūstam ievadīto lietotājvārdu
        parole = self.parole_ievade.text().strip()                  # Iegūstam ievadīto paroli

        if not lietotajvards or not parole:
            QMessageBox.warning(self, "Kļūda", "Lūdzu aizpildiet visus laukus!")
            return

        lietotajs = sesija.query(Lietotajs).filter_by(lietotajvards=lietotajvards).first()  # Meklē lietotāju pēc lietotājvārda

        if lietotajs and lietotajs.parbaud_paroli(parole):  # Ja lietotājs eksistē un parole ir pareiza
            self.lietotaja_id = lietotajs.id                # Saglabājam lietotāja ID
            self.accept()                                   # Aizver pieslēgšanās logu
        else:
            QMessageBox.warning(self, "Kļūda", "Nepareizs lietotājvārds vai parole!")

    # Funkcija, kas tiek izsaukta, kad lietotājs nospiež "Reģistrēties" pogu
    def registreties(self):
        lietotajvards = self.lietotajvards_ievade.text().strip()    # Iegūstam ievadīto lietotājvārdu
        parole = self.parole_ievade.text().strip()                  # Iegūstam ievadīto paroli

        if not lietotajvards or not parole:
            QMessageBox.warning(self, "Kļūda", "Lūdzu aizpildiet visus laukus!")
            return
        
        if sesija.query(Lietotajs).filter_by(lietotajvards=lietotajvards).first():  # Pārbauda, vai lietotājvārds jau eksistē
            QMessageBox.warning(self, "Kļūda", "Lietotājvārds jau eksistē!")        # Ja eksistē, izvada kļūdu
            return
        
        jauns_lietotajs = Lietotajs(lietotajvards=lietotajvards)            # Izveido jaunu lietotāju
        jauns_lietotajs.uzstadit_paroli(parole)                             # Uzstāda lietotājam paroli
        sesija.add(jauns_lietotajs)                                         # Pievieno jauno lietotāju datubāzei
        sesija.commit()                                                     # Saglabā izmaiņas datubāzē
        self.lietotaja_id = jauns_lietotajs.id                              # Saglabā jaunā lietotāja ID
        self.accept()                                                       # Aizver pieslēgšanās logu
