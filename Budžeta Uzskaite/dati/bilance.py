from dati.datubaze import Ienakumi, Izdevumi, sesija

def generet_parskatu(lietotaja_id):
    ienakumi = sesija.query(Ienakumi).filter_by(lietotaja_id=lietotaja_id).all() # Iegūst visus ienākumus konkrētajam lietotājam no datubāzes
    izdevumi = sesija.query(Izdevumi).filter_by(lietotaja_id=lietotaja_id).all() # Iegūst visus izdevumus konkrētajam lietotājam no datubāzes

    ienakumu_summa = sum(i.summa for i in ienakumi) # Aprēķina kopējo ienākumu summu
    izdevumu_summa = sum(i.summa for i in izdevumi) # Aprēķina kopējo izdevumu summu
    bilance = ienakumu_summa - izdevumu_summa # Aprēķina bilanci (ienākumi - izdevumi)

    return f"Ienākumi: {ienakumu_summa:.2f}, Izdevumi: {izdevumu_summa:.2f}, Bilance: {bilance:.2f}" # Atgriež vērtības ar diviem cipariem aiz komata

