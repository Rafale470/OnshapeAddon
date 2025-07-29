import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
from nomenclature import get_nomenclature
from init import clean

def lancer_traitement(url, nom_fichier):
    get_nomenclature(url, nom_fichier)
    QMessageBox.information(None, "Succès", f"Traitement lancé pour :\n{url}\n→ {nom_fichier}.csv")

def lancer_clean(nom_fichier):
    try:
        clean(nom_fichier)
        QMessageBox.information(None, "Nettoyage terminé", f"Fichiers export_bom.csv et prio.csv générés depuis : {nom_fichier}.csv")
    except Exception as e:
        QMessageBox.critical(None, "Erreur", f"Erreur lors du nettoyage :\n{str(e)}")

class MonInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Export BOM vers CSV")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        self.clean_label = QLabel("Nom du fichier à nettoyer :")
        self.clean_input = QLineEdit()
        layout.addWidget(self.clean_label)
        layout.addWidget(self.clean_input)

        self.clean_button = QPushButton("Nettoyer le fichier CSV")
        self.clean_button.clicked.connect(self.lancer_clean_depuis_ui)
        layout.addWidget(self.clean_button)

        self.url_label = QLabel("URL de l'assemblage :")
        self.url_input = QLineEdit()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)

        self.fichier_label = QLabel("Nom du fichier CSV :")
        self.fichier_input = QLineEdit()
        layout.addWidget(self.fichier_label)
        layout.addWidget(self.fichier_input)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.valider)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def valider(self):
        url = self.url_input.text()
        nom_fichier = self.fichier_input.text()

        if not url or not nom_fichier:
            QMessageBox.warning(self, "Champs manquants", "Merci de remplir tous les champs.")
            return

        lancer_traitement(url, nom_fichier)

    def lancer_clean_depuis_ui(self):
        nom_fichier = self.clean_input.text()

        if not nom_fichier:
            QMessageBox.warning(self, "Nom de fichier manquant", "Merci d’indiquer le nom du fichier à nettoyer.")
            return

        lancer_clean(nom_fichier)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = MonInterface()
    fenetre.show()
    sys.exit(app.exec_())
