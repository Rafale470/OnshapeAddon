import pandas as pd
import unicodedata
import os

def remove_accents(input_str):
    if isinstance(input_str, str):
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])
    return input_str

def clean(nom_fichier):
    df = pd.read_csv(f"{nom_fichier}.csv", encoding='utf-8-sig')
    df_clean = df.applymap(remove_accents)
    df_clean.to_csv("export_bom.csv", index=False)

    df_3_colonnes = df_clean.iloc[:, :2].drop_duplicates().copy()

    priorite_path = "prio.csv"
    if os.path.exists(priorite_path):
        try:
            df_old = pd.read_csv(priorite_path, encoding='utf-8-sig')
            df_old = df_old.applymap(remove_accents)
            df_3_colonnes = pd.merge(
                df_3_colonnes,
                df_old,
                on=[df_3_colonnes.columns[0], df_3_colonnes.columns[1]],
                how='left'
            )
            if 'Priorite_y' in df_3_colonnes.columns:
                df_3_colonnes.drop(columns=['Priorite_x'], inplace=True, errors='ignore')
                df_3_colonnes.rename(columns={'Priorite_y': 'Priorite'}, inplace=True)
        except Exception as e:
            df_3_colonnes['Priorite'] = ""
    else:
        df_3_colonnes['Priorite'] = ""

    df_3_colonnes.to_csv(priorite_path, index=False, encoding='utf-8-sig')


if __name__ == "__main__":
    clean("test")  
