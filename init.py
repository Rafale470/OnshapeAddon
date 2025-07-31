import pandas as pd
import unicodedata
import os

def remove_accents(input_str):
    """
    Supprime les accents d'une chaîne de caractères Unicode.

    Args:
        input_str (str): La chaîne de caractères à nettoyer.

    Returns:
        str: La chaîne sans accents si une chaîne est passée, sinon la valeur d'origine.
    """
    if isinstance(input_str, str):
        # Normalisation Unicode pour séparer les accents
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        # On garde uniquement les caractères non accentués
        return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])
    return input_str

def clean(nom_fichier):
    """
    Nettoie un fichier CSV en supprimant les accents, exporte un fichier BOM nettoyé,
    et met à jour un fichier de priorités (prio.csv) avec les premières colonnes.

    Args:
        nom_fichier (str): Nom du fichier CSV sans l'extension (.csv).
    """
    # Chargement du fichier CSV avec encodage latin1
    df = pd.read_csv(f"{nom_fichier}.csv", encoding='latin1')
    # Suppression des accents sur tout le DataFrame
    df_clean = df.applymap(remove_accents)
    # Sauvegarde du DataFrame nettoyé dans un nouveau fichier CSV
    df_clean.to_csv("export_bom.csv", index=False)

    # Extraction des 3 premières colonnes et suppression des doublons
    df_3_colonnes = df_clean.iloc[:, :3].drop_duplicates().copy()

    priorite_path = "prio.csv"
    if os.path.exists(priorite_path):
        try:
            # Lecture de l'ancien fichier de priorités
            df_old = pd.read_csv(priorite_path, encoding='latin1')
            df_old = df_old.applymap(remove_accents)
            # Fusion des priorités sur les deux premières colonnes
            df_3_colonnes = pd.merge(
                df_3_colonnes,
                df_old,
                on=[df_3_colonnes.columns[0], df_3_colonnes.columns[1]],
                how='left'
            )
            # Gestion des colonnes doublonnées de priorités
            if 'Priorite_y' in df_3_colonnes.columns:
                df_3_colonnes.drop(columns=['Priorite_x'], inplace=True, errors='ignore')
                df_3_colonnes.rename(columns={'Priorite_y': 'Priorite'}, inplace=True)
        except Exception as e:
            # En cas d'erreur lors de la fusion, on ajoute une colonne vide
            df_3_colonnes['Priorite'] = ""
    else:
        # Si le fichier priorite n'existe pas, on crée une colonne vide
        df_3_colonnes['Priorite'] = ""

    # Sauvegarde des priorités mises à jour
    df_3_colonnes.to_csv(priorite_path, index=False, encoding='utf-8-sig')

def full_clean(nom_fichier):
    """
    Nettoie un fichier CSV en supprimant les accents (écrase le fichier d'origine).

    Args:
        nom_fichier (str): Nom du fichier CSV sans l'extension (.csv).
    """
    df = pd.read_csv(f"{nom_fichier}.csv", encoding='utf-8')
    df_sans_accents = df.applymap(remove_accents)
    df_sans_accents.to_csv(f"{nom_fichier}.csv", index=False)

if __name__ == "__main__":
    # Exemple d'utilisation
    clean("test")
    full_clean("BOM of Assembly 1(3)")
