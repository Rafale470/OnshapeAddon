def convert(l):
    res = {}
    for elt in l:
        res[elt["Numéro de pièce"]] = int(elt["Nombre"])
    return res

def couverture(nomenclature, under_nomen):
    remaining = convert(nomenclature)
    added = {}
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
            added[under_nomen[round]["name"]] = added.get(str(round), 0) + 1
            for piece, number in under_nomen[round].items() :
                if piece == "name":
                    continue
                restant = remaining[piece] - int(number)
                if restant == 0 :
                    del remaining[piece]
                else : 
                    remaining[piece] = restant
    
        enrichi = {}
    info_pieces = {elt["Numéro de pièce"]: elt for elt in nomenclature}
    
    for piece, quantite in remaining.items():
        enrichi[piece] = {
            "Nom": info_pieces[piece]["Nom"],
            "Référence": info_pieces[piece]["Référence"],
            "Nombre": quantite
        }

    return added, enrichi

if __name__ == "__main__":
    NOMENCLATURE = [
    {"Nom": "pièceAAA","Numéro de pièce": "A","Référence": "qqa","Nombre": "9"},
    {"Nom": "pièceBBB","Numéro de pièce": "B","Référence": "qqb","Nombre": "2"},
    {"Nom": "pièceCCC","Numéro de pièce": "C","Référence": "qqc","Nombre": "9"},]

    UNDER_NOMENT = [
        {"A":1,"B":1,"C":1, "name":("BOM-A","Kit A")},
        {"C":1, "name":("BOM-B","Kit B")},
        {"A":2,"B":1,"name":("BOM-C","Kit C")}]

    print(couverture(NOMENCLATURE, UNDER_NOMENT))