import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
from nomenclature import get_nomenclature

def lancer_traitement(url, nom_fichier):
    get_nomenclature(url, nom_fichier)
    QMessageBox.information(None, "Succès", f"Traitement lancé pour :\n{url}\n→ {nom_fichier}.csv")

class MonInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Export BOM vers CSV")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = MonInterface()
    fenetre.show()
    sys.exit(app.exec_())
