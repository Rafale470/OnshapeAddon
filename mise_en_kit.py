import pandas as pd 
import unicodedata

def import_kit():

    dic_kit = {}

    df = pd.read_csv("export_bom.csv", encoding="latin1")

    def clean_key(texte):
        return ''.join(
            c for c in unicodedata.normalize('NFD', texte)
            if not unicodedata.combining(c)
        )

    for i , row in df.iterrows():
        if (row[0], clean_key(row[1])) not in dic_kit:
            dic_kit[(row[0], clean_key(row[1]))] = {"name":(row[0], clean_key(row[1]))}
        if row[11] != 32 and row[11] != 13:
            key = str(row[6])
            dic_kit[(row[0], clean_key(row[1]))][key] = row[9]
                
    df = pd.read_csv("prio.csv", encoding="latin1")

    list_kit_prio = []
    for i, row in df.iterrows():
        list_kit_prio.append(((row[0], clean_key(row[1])), 1000 if str(row[2]) == "nan" else row[2]))
    list_kit_prio = sorted(list_kit_prio, key=lambda x: x[1])

    list_kit_order = []
    for kit in list_kit_prio :
        if len(dic_kit[kit[0]]) != 1 :
            list_kit_order.append(dic_kit[kit[0]])

    return(list_kit_order)

if __name__ == "__main__":
    print(import_kit())