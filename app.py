import sys
import math
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QMessageBox, QFileDialog
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculateur de Puissance Reçue")
        self.setGeometry(100, 100, 800, 650)  # Ajustement de la hauteur à 650 pixels
        self.setStyleSheet(
            "background-color: #778899; "  # Couleur de fond principale
            "color: #ECF0F1; "  # Couleur du texte principal
        )

        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        container_widget = QWidget(self)
        container_widget.setStyleSheet(
            "background-color: #2C3E50; "  # Couleur de fond du container
            "border-radius: 8px;"
        )
        container_layout = QVBoxLayout()
        container_widget.setLayout(container_layout)
        main_layout.addWidget(container_widget, alignment=Qt.AlignCenter)

        container_widget.setMaximumWidth(600)

        title_label = QLabel("Calculateur de Puissance Reçue dans une Liaison Radio", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setStyleSheet("color: #ECF0F1;")  # Couleur du texte principal
        title_label.setWordWrap(True)
        container_layout.addWidget(title_label)

        form_layout = QVBoxLayout()

        labels = ["Puissance de Transmission (dBm) :", "Distance de Transmission (km) :", "Fréquence (MHz) :",
                  "Pertes d'Équipements (dB) :", "Gain de l'Antenne de Transmission (dB) :",
                  "Gain de l'Antenne de Réception (dB) :"]

        self.inputs = {}
        for label_text in labels:
            label = QLabel(label_text, self)
            label.setFont(QFont("Arial", 12, QFont.Bold))
            label.setStyleSheet("color: #ECF0F1;")  # Couleur du texte principal
            form_layout.addWidget(label)
            line_edit = QLineEdit(self)
            line_edit.setFont(QFont("Arial", 12))
            line_edit.setStyleSheet(
                "padding: 10px; "
                "background-color: #DCDCDC; "  # Couleur de fond des inputs
                "border: 1px solid #34495E; "  # Bordures et accents
                "border-radius: 4px; "
                "color: #000000;"  # Couleur du texte principal
            )
            form_layout.addWidget(line_edit)
            self.inputs[label_text] = line_edit

        container_layout.addLayout(form_layout)

        calculate_button = QPushButton("Calculer", self)
        calculate_button.setFont(QFont("Arial", 14, QFont.Bold))
        calculate_button.setStyleSheet(
            "background-color: #2980B9; "  # Couleur de mise en évidence du bouton
            "color: #ECF0F1; "
            "border: none; "
            "border-radius: 4px; "
            "padding: 10px;"
        )
        calculate_button.clicked.connect(self.calculer)
        container_layout.addWidget(calculate_button)

        self.result_label = QLabel("", self)
        self.result_label.setAlignment(Qt.AlignCenter)
        result_font = QFont("Arial", 16, QFont.Bold)
        self.result_label.setFont(result_font)
        self.result_label.setStyleSheet("color: #ECF0F1;")  # Couleur du texte principal
        container_layout.addWidget(self.result_label)

        # Bouton pour générer le rapport
        report_button = QPushButton("Générer Rapport PDF", self)
        report_button.setFont(QFont("Arial", 14, QFont.Bold))
        report_button.setStyleSheet(
            "background-color: #27AE60; "  # Couleur de mise en évidence du bouton
            "color: #ECF0F1; "
            "border: none; "
            "border-radius: 4px; "
            "padding: 10px;"
        )
        report_button.clicked.connect(self.generer_rapport_pdf)
        container_layout.addWidget(report_button)

    def calculer(self):
        try:
            Pt = float(self.inputs["Puissance de Transmission (dBm) :"].text())
            d = float(self.inputs["Distance de Transmission (km) :"].text())
            f = float(self.inputs["Fréquence (MHz) :"].text())
            Le = float(self.inputs["Pertes d'Équipements (dB) :"].text())
            Gt = float(self.inputs["Gain de l'Antenne de Transmission (dB) :"].text())
            Gr = float(self.inputs["Gain de l'Antenne de Réception (dB) :"].text())

            # Calcul du chemin de propagation libre en dB
            lp_db = 20 * (math.log10(d) + math.log10(f)) + 32.44
            
            # Calcul du bilan de liaison
            bilan_liaison_db = Pt + Gt + Gr - lp_db - Le

            self.result_label.setText(f"Puissance reçue: {bilan_liaison_db:.2f} dBm")

            self.afficher_graphique(d, f, Pt, Gt, Gr, Le)
        except ValueError:
            self.result_label.setText("Veuillez entrer des valeurs numériques valides.")

    def afficher_graphique(self, d, f, Pt, Gt, Gr, Le):
        distances = [i for i in range(1, int(d) + 1)]
        puissances_recues = []
        for dist in distances:
            lp_db = 20 * (math.log10(dist) + math.log10(f)) + 32.44
            Pr = Pt + Gt + Gr - lp_db - Le
            puissances_recues.append(Pr)

        plt.figure(figsize=(10, 6))
        plt.plot(distances, puissances_recues, marker='o')
        plt.title('Puissance Reçue en fonction de la Distance')
        plt.xlabel('Distance (km)')
        plt.ylabel('Puissance Reçue (dBm)')
        plt.grid(True)
        plt.show()

    def generer_rapport_pdf(self):
        try:
            Pt = float(self.inputs["Puissance de Transmission (dBm) :"].text())
            d = float(self.inputs["Distance de Transmission (km) :"].text())
            f = float(self.inputs["Fréquence (MHz) :"].text())
            Le = float(self.inputs["Pertes d'Équipements (dB) :"].text())
            Gt = float(self.inputs["Gain de l'Antenne de Transmission (dB) :"].text())
            Gr = float(self.inputs["Gain de l'Antenne de Réception (dB) :"].text())

            # Calcul du chemin de propagation libre en dB
            lp_db = 20 * (math.log10(d) + math.log10(f)) + 32.44
            
            # Calcul du bilan de liaison
            bilan_liaison_db = Pt + Gt + Gr - lp_db - Le

            # Générer le rapport en PDF
            file_dialog = QFileDialog(self)
            file_path, _ = file_dialog.getSaveFileName(self, "Enregistrer le rapport PDF", "", "PDF files (*.pdf)")

            if file_path:
                self.export_to_pdf(file_path, Pt, d, f, Le, Gt, Gr, bilan_liaison_db)

                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("Rapport PDF généré")
                msg_box.setText(f"Rapport PDF enregistré à : {file_path}")
                msg_box.setIcon(QMessageBox.Information)
                msg_box.exec_()
        except ValueError:
            self.result_label.setText("Veuillez entrer des valeurs numériques valides.")
    
    def export_to_pdf(self, file_path, Pt, d, f, Le, Gt, Gr, Pr):
        try:
            doc = SimpleDocTemplate(file_path, pagesize=letter)
            elements = []

            data = [
                ["Paramètre", "Valeur"],
                ["Puissance de Transmission (dBm)", Pt],
                ["Distance de Transmission (km)", d],
                ["Fréquence (MHz)", f],
                ["Pertes d'Équipements (dB)", Le],
                ["Gain de l'Antenne de Transmission (dB)", Gt],
                ["Gain de l'Antenne de Réception (dB)", Gr],
                ["Puissance reçue (dBm)", f"{Pr:.2f}"]
            ]

            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ])

            table = Table(data)
            table.setStyle(table_style)
            elements.append(table)

            doc.build(elements)

        except Exception as e:
            print(f"Erreur lors de la création du PDF : {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

