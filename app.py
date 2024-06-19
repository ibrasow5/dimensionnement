import sys
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

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

    def calculer(self):
        try:
            Pt = float(self.inputs["Puissance de Transmission (dBm) :"].text())
            d = float(self.inputs["Distance de Transmission (km) :"].text())
            f = float(self.inputs["Fréquence (MHz) :"].text())
            Le = float(self.inputs["Pertes d'Équipements (dB) :"].text())
            Gt = float(self.inputs["Gain de l'Antenne de Transmission (dB) :"].text())
            Gr = float(self.inputs["Gain de l'Antenne de Réception (dB) :"].text())

            Lp = 20 * (math.log10(d) + math.log10(f)) + 32.44
            Pr = Pt + Gt + Gr - Lp - Le

            self.result_label.setText(f"Puissance reçue: {Pr:.2f} dBm")
        except ValueError:
            self.result_label.setText("Veuillez entrer des valeurs numériques valides.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
