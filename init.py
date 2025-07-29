import pandas as pd
import unicodedata

def remove_accents(input_str):
    if isinstance(input_str, str):
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])
    return input_str

def clean (nom_fichier):
    df = pd.read_csv(f"{nom_fichier}.csv")  
    df_clean = df.applymap(remove_accents)
    df_clean.to_csv("export_bom.csv", index=False)
    df_3_colonnes = df_clean.iloc[:, :2].copy()
    df_3_colonnes['Priorite'] = ""
    df_3_colonnes.to_csv("prio.csv", index=False)

if __name__ == "__main__":
    clean("test")