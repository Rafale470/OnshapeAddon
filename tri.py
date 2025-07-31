def convert(l):
    """
    Transforme une liste de dictionnaires contenant des pièces en un dictionnaire
    {reference: quantité}.

    Args:
        l (list[dict]): Liste d'éléments de nomenclature (chaque dict contient 'Reference' et 'Nombre').

    Returns:
        dict[str, int]: Dictionnaire des références et leur quantité.
    """
    res = {}
    for elt in l:
        res[elt["Reference"]] = int(elt["Nombre"])
    return res

def couverture(nomenclature, under_nomen):
    """
    Tente de couvrir une nomenclature avec des kits disponibles.

    Args:
        nomenclature (list[dict]): Liste de pièces avec Nom, Reference, Nombre, etc.
        under_nomen (list[dict]): Liste de kits disponibles avec structure {"reference": quantité, "name": (bom, nom, id)}.

    Returns:
        tuple:
            - added (dict): Nombre de fois que chaque kit a été ajouté.
            - enrichi (dict): Pièces restantes non couvertes, avec leurs infos.
    """
    remaining = convert(nomenclature)  # Pièces à couvrir
    added = {}                         # Kits ajoutés
    enrichi = {}                       # Résultat des pièces restantes
    n = len(under_nomen)

    def select(remaining):
        """
        Recherche un kit entièrement "couvrable" avec les pièces restantes.

        Args:
            remaining (dict): Références encore disponibles.

        Returns:
            int or None: Index du kit utilisable ou None si aucun.
        """
        for i in range(n):
            kit = under_nomen[i]
            working = True
            for piece in kit:
                if piece == "name":
                    continue
                if piece not in remaining or int(kit[piece]) > remaining[piece]:
                    working = False
                    break
            if working:
                return i
        return None

    while len(remaining) != 0:
        round = select(remaining)
        if round is None:
            break

        kit = under_nomen[round]
        kit_name = kit["name"]
        added[kit_name] = added.get(kit_name, 0) + 1

        for piece, qty in kit.items():
            if piece == "name":
                continue
            restant = remaining[piece] - int(qty)
            if restant == 0:
                del remaining[piece]
            else:
                remaining[piece] = restant

    # Construction enrichie avec infos détaillées
    info_pieces = {elt["Reference"]: elt for elt in nomenclature}
    for piece, quantite in remaining.items():
        enrichi[piece] = {
            "Nom": info_pieces[piece]["Nom"],
            "Reference": piece,
            "Numero": info_pieces[piece]["Numero de piece"],
            "Nombre": quantite
        }

    return added, enrichi

# Exemple d'exécution
if __name__ == "__main__":
    NOMENCLATURE = [
        {'Nom': 'CABINEO 8 MM - NOIR', 'Numero de piece': 'QU-CABINEO_8_NOIR', 'Reference': '4972', 'Nombre': 104},
        {'Nom': 'ACCOUPLEMENT TANDEM DROIT', 'Numero de piece': 'QU-ACCOUPL-DROIT', 'Reference': '1627', 'Nombre': 2},
        {'Nom': 'ACCOUPLEMENT TANDEM GAUCHE', 'Numero de piece': 'QU-ACCOUPL-GAUCHE', 'Reference': '1626', 'Nombre': 2}
    ]

    UNDER_NOMENT = [
        {"A": 1, "B": 1, "C": 1, "name": ("BOM-A", "Kit A", "12")},
        {"C": 1, "name": ("BOM-B", "Kit B", "13")},
        {"A": 2, "B": 1, "name": ("BOM-C", "Kit C", "15")},
        {'name': ('BOMTEST', 'KitTest', "16"), "4972": 4.0, "1627": 2.0, "1626": 1.0}
    ]

    print(couverture(NOMENCLATURE, UNDER_NOMENT))
