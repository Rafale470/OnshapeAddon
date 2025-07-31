import pandas as pd 
import unicodedata
from black_list import BLACK_LIST

def import_kit():
    """
    Importe les données des kits depuis les fichiers `export_bom.csv` et `prio.csv`.

    Regroupe les données par clé composée de trois champs :
    - Nom (colonne 0)
    - Référence nettoyée sans accents (colonne 1)
    - Un identifiant (colonne 2)

    Puis filtre les entrées valides (non blacklistées, bonnes valeurs numériques) et
    trie les kits selon leur priorité définie dans `prio.csv`.

    Returns:
        list[dict]: Liste de dictionnaires représentant les kits valides, triés par priorité.
    """

    dic_kit = {}  # Dictionnaire principal des kits

    # Chargement du fichier exporté
    df = pd.read_csv("export_bom.csv", encoding="latin1")

    def clean_key(texte):
        """Supprime les accents d’un texte Unicode."""
        return ''.join(
            c for c in unicodedata.normalize('NFD', texte)
            if not unicodedata.combining(c)
        )
    
    # Parcours des lignes du fichier BOM
    for i, row in df.iterrows():
        # Création d'une clé unique (nom, ref nettoyée, identifiant)
        key_tuple = (row[0], clean_key(row[1]), row[2])
        
        # Initialisation de l’entrée si elle n’existe pas
        if key_tuple not in dic_kit:
            dic_kit[key_tuple] = {"name": key_tuple}

        # Filtrage des lignes selon la colonne unité et la blacklist
        if row[11] != 32 and row[11] != 13 and str(row[6]) not in BLACK_LIST:
            key = str(row[6])
            dic_kit[key_tuple][key] = row[9]  # Ajout d’un composant au kit

    # Lecture du fichier de priorités
    df = pd.read_csv("prio.csv", encoding="latin1")

    list_kit_prio = []
    for _, row in df.iterrows():
        key_tuple = (row[0], clean_key(row[1]), row[2])
        try:
            prio = float(row[2]) if pd.notna(row[2]) else 1000  # Si vide ou nan, priorité par défaut
        except (ValueError, TypeError):
            prio = 1000
        list_kit_prio.append((key_tuple, prio))

    # Tri des kits par priorité croissante
    list_kit_prio = sorted(list_kit_prio, key=lambda x: x[1])

    # Construction de la liste finale des kits valides (avec composants)
    list_kit_order = []
    for kit in list_kit_prio:
        if len(dic_kit.get(kit[0], {})) > 1:  # Vérifie qu’il y a bien des composants (pas juste "name")
            list_kit_order.append(dic_kit[kit[0]])

    return list_kit_order

if __name__ == "__main__":
    print(import_kit())
