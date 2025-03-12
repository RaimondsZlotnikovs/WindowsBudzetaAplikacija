from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import bcrypt
import os

# Norāda kur tiks sagalbāta datubāze un ar kādu nosaukumu
datu_mape = "dati"
db_cels = os.path.join(datu_mape, "budzets.db")

# Datubāzes savienojums
engine = create_engine(f"sqlite:///{db_cels}", echo=False)
# SQLAlchemy bāzes klase modeļu definēšanai
baze = declarative_base()

# Lietotāju tabula
class Lietotajs(baze):
    __tablename__ = "lietotaji"                                 # Tabulas nosaukums
    id = Column(Integer, primary_key=True)                      # Primārā atslēga   
    lietotajvards = Column(String, unique=True, nullable=False) # Lietotājvārds
    parole_hash = Column(String, nullable=False)                # Paroles

    # Metode paroles šifrēšanai un saglabāšanai
    def uzstadit_paroli(self, parole):
        self.parole_hash = bcrypt.hashpw(parole.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    # Metode paroles pārbaudei
    def parbaud_paroli(self, parole):
        return bcrypt.checkpw(parole.encode("utf-8"), self.parole_hash.encode("utf-8"))

# Ienākumu tabula
class Ienakumi(baze):
    __tablename__ = "ienakumi"                                                      # Tabulas nosaukums
    id = Column(Integer, primary_key=True)                                          # Primārā atslēga
    lietotaja_id = Column(Integer, ForeignKey("lietotaji.id"), nullable=False)      # Ārējā atslēga
    summa = Column(Float, nullable=False)                                           # Ienākuma summa
    datums = Column(Date, nullable=False)                                           # Ienākuma datums
    kategorija_id = Column(Integer, ForeignKey("kategorijas.id"), nullable=False)   # Kategorijas atslēga

# Izdevumu tabula
class Izdevumi(baze):
    __tablename__ = "izdevumi"                                                      # Tabulas nosaukums
    id = Column(Integer, primary_key=True)                                          # Primārā atslēga
    lietotaja_id = Column(Integer, ForeignKey("lietotaji.id"), nullable=False)      # Ārējā atslēga
    summa = Column(Float, nullable=False)                                           # Izdevuma summa
    datums = Column(Date, nullable=False)                                           # Izdevuma datums
    kategorija_id = Column(Integer, ForeignKey("kategorijas.id"), nullable=False)   # Kategorijas atslēga

class Kategorija(baze):                                         # Kategoriju tabula
    __tablename__ = "kategorijas"                               # Tabulas nosaukums
    id = Column(Integer, primary_key=True)                      # Primārā atslēga
    nosaukums = Column(String, unique=True, nullable=False)     # Kategorijas nosaukums
    veids = Column(String, nullable=False)                      # Kategorijas veids (ienākumi/izdevumi)

# Izvedio tabulas, ja tādas nepastāv
baze.metadata.create_all(engine)

# Sesijas inicializācija
Sesija = sessionmaker(bind=engine)
sesija = Sesija()   