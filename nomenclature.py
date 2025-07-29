import requests
import pandas as pd
from collections import defaultdict
from credential import AUTH
from white_list import WHITE_LIST
from material_list import MATERIAL_LIST
from tri import couverture
from mise_en_kit import import_kit
import csv

BASE_URL = "https://cad.onshape.com"
TEST = "https://cad.onshape.com/documents/cf77df69727a79b4260ec223/w/129fa290abf3f44098958c1c/e/8fffd41d48f03b74f39fabf0"

def get_ids_from_url(url):
    parties = url.split("/")
    return parties[4],parties[5], parties[6], parties[8]

def get_nomenclature(url, nom_fichier):
    did, wvm, wvmid, eid = get_ids_from_url(url)
    req = f"https://cad.onshape.com/api/v12/assemblies/d/{did}/{wvm}/{wvmid}/e/{eid}/bom?indented=true&multiLevel=true&generateIfAbsent=true&includeExcluded=false&ignoreSubassemblyBomBehavior=false&includeItemMicroversions=false&includeTopLevelAssemblyRow=false&thumbnail=false"
    print(req)
    head = {
    "accept": "application/json;charset=UTF-8; qs=0.09",
    "Authorization": f"Basic {AUTH}",
    }
    
    try:
        response = requests.get(req, headers=head, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(f"Request failed: {err}")
        raise
    data = response.json()
    
    full_data = []
    for row in data.get("rows", []):
        item = row.get("itemSource", {})
        headers = row.get("headerIdToValue", {})
        number = headers.get("57f3fb8efa3416c06701d60f") or "UNKNOWN"
        id = headers.get("6881e5cdc8936b295230a632") or "UNKNOWN"
    
        if not item.get("partId") and id not in WHITE_LIST:  
            print(f"Ignored: {headers.get("57f3fb8efa3416c06701d60d") or "UNKNOWN"}")
            continue

        full_data.append({
            "documentId": item.get("documentId"),
            "elementId": item.get("elementId"),
            "wvmType": item.get("wvmType"),
            "wvmId": item.get("wvmId"),
            "name": headers.get("57f3fb8efa3416c06701d60d") or "UNKNOWN",
            "number" : number,
            "id" : id,
            "displayName": (
                headers.get("57f3fb8efa3416c06701d615", {}).get("displayName")
                if isinstance(headers.get("57f3fb8efa3416c06701d615"), dict)
                else headers.get("57f3fb8efa3416c06701d615") or "UNKNOWN"
            ),
            "occurrences": len(row.get("relatedOccurrences", []))
        })

    grouped = defaultdict(lambda: defaultdict(int))
    for entry in full_data:
        key = (
            entry["documentId"],
            entry["elementId"],
            entry["wvmType"],
            entry["wvmId"],
            entry["displayName"]
        )
        grouped[key][(entry["name"], entry["number"], entry["id"])] += entry["occurrences"]

    final_result = []
    for (doc_id, elem_id, wvm_type, wvm_id, display_name), parts in grouped.items():
        for (name, number, id), count in parts.items():
            if display_name not in MATERIAL_LIST or id in WHITE_LIST:
                final_result.append({
                    "Nom": name,
                    "Numero de piece": number,
                    "Reference": id,
                    "Nombre": count
                })
    
    list_kit_order = import_kit()
    list_kit, list_piece = couverture(final_result,list_kit_order)
    
    with open(f"{nom_fichier}.csv", mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        
        writer.writerow(["Type", "Reference", "Nom", "Nombre"])
        
        for (ref, nom), quantite in list_kit.items():
            writer.writerow(["Kit", ref, nom, quantite])
        
        writer.writerow([])

        for _, piece in list_piece.items():
            writer.writerow(["Piece", piece["Reference"], piece["Nom"], piece["Nombre"]])

if __name__ == "__main__" :
    print(get_nomenclature(TEST, "test3"))