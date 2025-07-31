import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
from nomenclature import get_nomenclature
from init import clean

def lancer_traitement(url, nom_fichier):
    """
    Lance le traitement principal à partir d'une URL d'assemblage.

    Args:
        url (str): URL de l'assemblage.
        nom_fichier (str): Nom du fichier de sortie (sans extension).

    Affiche une boîte de dialogue en cas de succès ou d'erreur.
    """
    try:
        get_nomenclature(nom_fichier, 0, url)
        QMessageBox.information(None, "Succès", f"Traitement lancé pour :\n{url}\n→ {nom_fichier}.csv")
    except Exception as e:
        QMessageBox.critical(None, "Erreur", f"Erreur lors de l'execution :\n{str(e)}")

def lancer_clean(nom_fichier):
    """
    Lance le nettoyage du fichier CSV en supprimant les accents
    et en générant deux fichiers : export_bom.csv et prio.csv.

    Args:
        nom_fichier (str): Nom du fichier source sans extension.
    """
    try:
        clean(nom_fichier)
        QMessageBox.information(None, "Nettoyage terminé", f"Fichiers export_bom.csv et prio.csv générés depuis : {nom_fichier}.csv")
    except Exception as e:
        QMessageBox.critical(None, "Erreur", f"Erreur lors du nettoyage :\n{str(e)}")
        
def lancer_source(nom_fichier, nom_source):
    """
    Lance le traitement de nomenclature à partir d'un fichier source.

    Args:
        nom_fichier (str): Nom du fichier de sortie.
        nom_source (str): Nom du fichier source (CSV).
    """
    try:
        get_nomenclature(nom_fichier, 1, nom_source)
        QMessageBox.information(None, "Succès", f"Traitement (avec source) lancé pour :\n{nom_source}\n→ {nom_fichier}.csv")
    except Exception as e:
        QMessageBox.critical(None, "Erreur", f"Erreur lors de l'execution :\n{str(e)}")

class MonInterface(QWidget):
    """
    Interface utilisateur principale pour lancer les traitements
    d'export BOM et de nettoyage de fichiers CSV.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Export BOM vers CSV")
        self.init_ui()

    def init_ui(self):
        """
        Initialise l'interface utilisateur avec les champs de saisie et les boutons.
        """
        layout = QVBoxLayout()

        # Section nettoyage
        self.clean_label = QLabel("Nom du fichier à nettoyer :")
        self.clean_input = QLineEdit()
        layout.addWidget(self.clean_label)
        layout.addWidget(self.clean_input)

        self.clean_button = QPushButton("Nettoyer le fichier CSV")
        self.clean_button.clicked.connect(self.lancer_clean_depuis_ui)
        layout.addWidget(self.clean_button)

        # Section traitement via URL
        self.url_label = QLabel("URL de l'assemblage (configuration par défaut uniquement):")
        self.url_input = QLineEdit()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)

        self.fichier_label = QLabel("Nom du fichier CSV de sortie :")
        self.fichier_input = QLineEdit()
        layout.addWidget(self.fichier_label)
        layout.addWidget(self.fichier_input)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.valider)
        layout.addWidget(self.ok_button)

        # Section traitement avec fichier source
        self.source_label = QLabel("Nom du fichier CSV source :")
        self.source_input = QLineEdit()
        layout.addWidget(self.source_label)
        layout.addWidget(self.source_input)
        
        self.fichier2_label = QLabel("Nom du fichier CSV de sortie :")
        self.fichier2_input = QLineEdit()
        layout.addWidget(self.fichier2_label)
        layout.addWidget(self.fichier2_input)

        self.source_button = QPushButton("Ok")
        self.source_button.clicked.connect(self.lancer_avec_source)
        layout.addWidget(self.source_button)

        self.setLayout(layout)

    def valider(self):
        """
        Vérifie les champs pour le traitement via URL et le lance si tout est rempli.
        """
        url = self.url_input.text()
        nom_fichier = self.fichier_input.text()

        if not url or not nom_fichier:
            QMessageBox.warning(self, "Champs manquants", "Merci de remplir tous les champs.")
            return

        lancer_traitement(url, nom_fichier)

    def lancer_clean_depuis_ui(self):
        """
        Vérifie le champ de nettoyage et lance la fonction associée.
        """
        nom_fichier = self.clean_input.text()

        if not nom_fichier:
            QMessageBox.warning(self, "Nom de fichier manquant", "Merci d’indiquer le nom du fichier à nettoyer.")
            return

        lancer_clean(nom_fichier)
    
    def lancer_avec_source(self):
        """
        Vérifie les champs pour le traitement avec fichier source et lance la fonction.
        """
        nom_fichier = self.fichier2_input.text()
        nom_source = self.source_input.text()

        if not nom_fichier or not nom_source:
            QMessageBox.warning(self, "Champs manquants", "Merci de remplir tous les champs pour le traitement avec source.")
            return

        lancer_source(nom_fichier, nom_source)

if __name__ == "__main__":
    # Démarrage de l'application PyQt
    app = QApplication(sys.argv)
    fenetre = MonInterface()
    fenetre.show()
    sys.exit(app.exec_())
