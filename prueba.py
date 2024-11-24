import sys
from PyQt6.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)

label = QLabel("¡Hola, PyQt6!")
label.show()

sys.exit(app.exec())
