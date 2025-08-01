
EXPORT BOM ONSHAPE – GENERATEUR DE KITS ET PANNEAUX
==================================================

DESCRIPTION
-----------
Ce projet a été réalisé dans le cadre de mon stage au sein d'Exokit. 
Il permet d'extraire, nettoyer et transformer des nomenclatures techniques (BOM) issues de Onshape ou d’un fichier CSV local, afin de générer un fichier CSV structuré contenant :

- Des kits regroupés
- Des pièces non couvertes
- Des panneaux bois avec quantités calculées

STRUCTURE DU PROJET
-------------------
main.py                : Interface du projet permettant de lancer l'execution 
nomenclature.py        : Extraction de la nomenclature et export des données
mise_en_kit.py         : Définit les kits à partir d'un fichier CSV
tri.py                 : Optimise la couverture des pièces par des kits
init.py                : Nettoie les accents et gère la génération de fichier CSV initiaux
material_list.py       : Liste de matériaux bois
white_list.py          : Liste de référence à inclure lors du traitement
black_list.py          : Liste de référence à inclure
credential.py          : Authentification API
export_bom.csv         : Fichier CSV contenant les kits existants
prio.csv               : Fichier CSV contenant l'ordre de priorité des kits 
README.txt             : Ce fichier

INSTALLATION
------------
1. Installer Python 3.8 ou version plus récente
2. Installer les dépendances nécessaires :

    -   pandas
    -   unicode
    -   os
    -   sys
    -   PyQt5.QtWidgets
    -   requests
    -   collection
    -   csv
    -   math
    -   warnings

   commande d'installation : pip install [dépendance]
   ex : pip install pandas 

3. Créer un fichier credential.py contenant :

   AUTH = "Basic VOTRE_TOKEN_ENCODE_EN_BASE64"

UTILISATION
-----------
Importer les kits :
    Depuis dolibar, importer les kits dans un fichier CSV. Ce fichier devra contenir la référence du kit (colone A), le libellé du kit (colonne B), l'ID produit du kit (colonne C), l'id produit de la pièce (colonne G), le nombre requis de la pièce (colonne J), l'unité de la pièce (colonne L). 
    Il est possible de forcer l'exploration de certains kits en priorité, pour cela il suffit de mettre à jour la "priorité" du kit dans le fichier prio.csv . Les priorités déjà définit sont conservé même en cas de nouvel import des kits. 
    Les pièces bois considéré comme standard et apparaissant dans les nomenclatures doivent avoir une unité 37.

Extraction depuis une URL Onshape :
    Il suffit de récupérer l'URL de l'assemblage. Cette fonctionalité va récupérer la configuration par défaut de l'assemblage. Pour charger une configuration spécifique, il faut l'ajouter à la fin de l'URL séparé par ; (voir documentation onshape pour le format de l'URL).
    A moins de changer les identifiants des différentes options des configurations, il parait peu pratique de charger des configurations différents de celle par défaut.

Extraction depuis un fichier CSV local :
    Il suffit de donner le nom de l'export CSV de la nomenclature onshape. Cette dernière s'adapte à la configuration choisie et ne requiert pas l'usage de l'API. C'est cette utilisation du projet qui semble la plus utile et la plus pertinente.

Résultat :
    Un fichier nom_de_sortie.csv sera généré, contenant trois sections : Kits, Pièces, Panneaux.

FORMAT DU FICHIER GENERE
-------------------------
Colonnes : Type, ID, Reference, Nom, Nombre

Exemple :
Kit     12      KIT-A         Kit A complet         3
Piece   4972    QU-CABINEO    CABINEO 8 MM NOIR     28
Panneau 6172    PAN_CP15_FILM CP15.5 bouleau FILM   4.5

NOTE
-----------
Les pièces standards considéré comme des assemblages sur Onshape doivent être ajouté manuellement à white_list.py.

L'execution est supposé être robuste aux différents encodage de fichier utilisé par Onshape et Dolibar. Ces derniers restes suceptibles d'être problématique. En cas de soucis, un encodage au format UTF-8 est à privilégier, il est facile de changer l'encodage d'un fichier CSV notamment en utilisant un logiciel comme Notepad++.

AUTEURS
-------
Moi :)



