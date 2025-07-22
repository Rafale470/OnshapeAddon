import requests
import pandas as pd
from collections import defaultdict
from credential import ACCESS_KEY, SECRET_KEY

BASE_URL = "https://cad.onshape.com"
TEST = "https://cad.onshape.com/documents/e4b6852c1aeadb87d10fe119/w/6a95673077b4f5c97ba43d70/e/3bc37e4643c68313f8e23eed"

def get_ids_from_url(url):
    parties = url.split("/")
    return parties[4],parties[5], parties[6], parties[8]

def get_nomenclature(url, nom_fichier):
    did, wvm, wvmid, eid = get_ids_from_url(url)
    req = f"https://cad.onshape.com/api/v12/assemblies/d/{did}/{wvm}/{wvmid}/e/{eid}/bom?indented=true&multiLevel=true&generateIfAbsent=true&includeExcluded=false&ignoreSubassemblyBomBehavior=false&includeItemMicroversions=false&includeTopLevelAssemblyRow=false&thumbnail=false"

    head = {
    "accept": "application/json;charset=UTF-8; qs=0.09",
    "Authorization": "Basic Nk5HVUpmSlpQeXFxUEZKOFpjYmRvSDRiOkpiUm5mYmRhb2tpQVNwd09PZlpqdHZJOXdlMFVucGhiSXNxZGpUTGxsWU00OUsyUw==",
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

        full_data.append({
            "documentId": item.get("documentId"),
            "elementId": item.get("elementId"),
            "wvmType": item.get("wvmType"),
            "wvmId": item.get("wvmId"),
            "name": headers.get("57f3fb8efa3416c06701d60d") or "UNKNOWN",
            "number" : headers.get("57f3fb8efa3416c06701d60f") or "UNKNOWN",
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
        grouped[key][(entry["name"], entry["number"])] += entry["occurrences"]

    material = [
        "CP15 bouleau Brut",
        "CP9 bouleau Brut",
        "CP15.5 bouleau FILM",
        "CP9.5 bouleau FILM",
        "CP16.4 bouleau STRAT_1",
        "CP16.4 bouleau STRAT_2",
        "CP15 bouleau CC",
        "CP15 bouleau EB"
    ]

    final_result = []
    for (doc_id, elem_id, wvm_type, wvm_id, display_name), parts in grouped.items():
        if display_name not in material:
            for (name, number), count in parts.items():
                final_result.append({
                    "Nom": name,
                    "Numéro de pièce": number,
                    "Nombre": count
                })
    
    df = pd.DataFrame(final_result)
    df.to_csv(f"{nom_fichier}.csv", index=False)
    
    return final_result

if __name__ == "__main__" :
    print(get_nomenclature(TEST, "test"))