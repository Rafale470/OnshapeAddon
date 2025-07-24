def convert(l):
    res = {}
    for elt in l:
        res[elt["Reference"]] = int(elt["Nombre"])
    return res

def couverture(nomenclature, under_nomen):
    remaining = convert(nomenclature)
    added = {}
    enrichi = {}
    n = len(under_nomen)
    
    while len(remaining) != 0 :
        
        def select(remaining):
            for i in range(n) :
                under_nomen_2 = under_nomen[i]
                working = True
                for piece in under_nomen_2:
                    if piece == "name" :
                        continue
                    elif piece not in remaining :
                        working = False
                    elif int(under_nomen_2[piece]) > remaining[piece]:
                        working = False
                if working :
                    return i
        
        round = select(remaining)
        if round == None :
            break
        else :
            added[under_nomen[round]["name"]] = added.get(under_nomen[round]["name"], 0) + 1
            for piece, number in under_nomen[round].items() :
                if piece == "name":
                    continue
                restant = remaining[piece] - int(number)
                if restant == 0 :
                    del remaining[piece]
                else : 
                    remaining[piece] = restant
    
        enrichi = {}
    info_pieces = {elt["Reference"]: elt for elt in nomenclature}
    
    for piece, quantite in remaining.items():
        enrichi[piece] = {
            "Nom": info_pieces[piece]["Nom"],
            "Reference": info_pieces[piece]["Reference"],
            "Nombre": quantite
        }

    return added, enrichi

if __name__ == "__main__":
    NOMENCLATURE = [{'Nom': 'CABINEO 8 MM - NOIR', 'Numero de piece': 'QU-CABINEO_8_NOIR', 'Reference': '4972', 'Nombre': 104},
                    {'Nom': 'ACCOUPLEMENT TANDEM DROIT', 'Numero de piece': 'QU-ACCOUPL-DROIT', 'Reference': '1627', 'Nombre': 2},
                    {'Nom': 'ACCOUPLEMENT TANDEM GAUCHE', 'Numero de piece': 'QU-ACCOUPL-GAUCHE', 'Reference': '1626', 'Nombre': 2}]

    UNDER_NOMENT = [
        {"A":1,"B":1,"C":1, "name":("BOM-A","Kit A")},
        {"C":1, "name":("BOM-B","Kit B")},
        {"A":2,"B":1,"name":("BOM-C","Kit C")},
        {'name': ('BOMTEST', 'KitTest'), "4972": 4.0, "1627": 2.0, "1626": 1.0}]

    print(couverture(NOMENCLATURE, UNDER_NOMENT))