import sys
from PyQt5.QtWidgets import QApplication
from logi.galvenais_logs import BudzetaAplikacija
from logi.pieslegsanas_logs import PieslegsanasLogs
from PyQt5.QtWidgets import QDialog

if __name__ == "__main__":                                          # Ja šis fails tiek palaists kā galvenais
    app = QApplication(sys.argv)                                    # Izveido aplikācijas instanci

    pieslegsanas_logs = PieslegsanasLogs()                          # Izveido pieslēgšanās loga instanci
    if pieslegsanas_logs.exec_() == QDialog.Accepted:               # Ja lietotājs pieslēdzās
        logs = BudzetaAplikacija(pieslegsanas_logs.lietotaja_id)    # Izveido galvenā loga instanci
        logs.show()                                                 # Parāda galveno logu
        sys.exit(app.exec_())                                       # Palaiž aplikāciju
