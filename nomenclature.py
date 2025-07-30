import requests
import pandas as pd
from collections import defaultdict
from credential import AUTH
from white_list import WHITE_LIST
from material_list import MATERIAL_LIST, MATERIAL_LIST_LONG
from tri import couverture
from mise_en_kit import import_kit
import csv
from init import full_clean
import math

BASE_URL = "https://cad.onshape.com"
TEST = "https://cad.onshape.com/documents/eb932709e9be08be45ec0e22/w/86b2af11aafd9c9d54348cde/e/cfa95460c6a6ec5cb90ae7da"

def get_ids_from_url(url):
    parties = url.split("/")
    return parties[4],parties[5], parties[6], parties[8]

def extract_from_API (url) :
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
    wood = {}
    for idx, row in enumerate(data.get("rows", [])):
        item = row.get("itemSource", {})
        headers = row.get("headerIdToValue", {})
        number = headers.get("57f3fb8efa3416c06701d60f") or "UNKNOWN"
        id = headers.get("6881e5cdc8936b295230a632") or f"UNKNOWN_{idx}"
        display_name = (headers.get("57f3fb8efa3416c06701d615", {}).get("displayName")
                if isinstance(headers.get("57f3fb8efa3416c06701d615"), dict)
                else headers.get("57f3fb8efa3416c06701d615") or "UNKNOWN")

        if item.get("partId") and id not in WHITE_LIST and display_name in MATERIAL_LIST:
            wood[display_name] = wood.get(display_name, 0) + float(headers.get("57f3fb8efa3416c06701d626").split()[0])
        
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
            "displayName": display_name,
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

    return final_result, wood

def extract_from_csv(name):
    full_clean(name)
    df = pd.read_csv(f"{name}.csv")
    
    final_result = []
    wood = {}
    for idx , row in df.iterrows():
        if not math.isnan(row[5]):
            id = str(int(row[5]))
        else:
            id = f"UNKNOWN_{idx}"
        if not(row[6] == "Assembly" and id not in WHITE_LIST) and (row[4] not in MATERIAL_LIST or id in WHITE_LIST):
            final_result.append({
        "Nom": row[1],
        "Numero de piece": row[2],
        "Reference": id,
        "Nombre": row[3]
    })
        if row[6] != "Assembly" and row[4] in MATERIAL_LIST and id not in WHITE_LIST :
            wood[row[4]] = wood.get(row[4], 0) + float(row[7].split()[0])
    return final_result, wood

def calculer_surfaces_en_panneaux(material_weights):
    density = 7  # kg/m²/mm
    panel_area = 1.5 * 3  # m²

    result = []

    for i in range(0, len(MATERIAL_LIST_LONG), 4):
            name = MATERIAL_LIST_LONG[i]
            material_id = MATERIAL_LIST_LONG[i+1]
            reference = MATERIAL_LIST_LONG[i+2]
            thickness = MATERIAL_LIST_LONG[i+3]  # en mm

            weight = material_weights.get(name)
            if weight is not None:
                weight_with_margin = weight * 1.25
                surface = weight_with_margin / (thickness * density)  # en m²
                nb_panels = surface / panel_area

                nb_panels_rounded = math.ceil(nb_panels)

                result.append((material_id, reference, name, nb_panels_rounded))

    return result
    
    
def get_nomenclature(nom_fichier, method, source):
    if method == 0 :
        final_result, wood = extract_from_API(source)
    
    if method == 1 :
        final_result, wood = extract_from_csv(source)
    
    list_kit_order = import_kit()
    list_kit, list_piece = couverture(final_result,list_kit_order)
    
    final_wood = calculer_surfaces_en_panneaux(wood)
    
    with open(f"{nom_fichier}.csv", mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        
        writer.writerow(["Type", "Reference", "Nom", "Nombre"])
        
        for (ref, nom), quantite in list_kit.items():
            writer.writerow(["Kit", ref, nom, quantite])
        
        writer.writerow([])

        for _, piece in list_piece.items():
            writer.writerow(["Piece", piece["Reference"], piece["Nom"], piece["Nombre"]])
            
        writer.writerow([])
        
        for elt in final_wood:
            writer.writerow(["Panneau", elt[0], elt[2], elt[3]])

if __name__ == "__main__" :
    print(get_nomenclature("test3", 0, TEST))
    #print(extract_from_csv("BOM of Assembly 1(3)")[1])
    #print(extract_from_API(TEST))