import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon, QFont, QPixmap
import BaseDatos



class MainWindow(QMainWindow):
    def __init__(self, title: str):
        super().__init__()
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon('meme.webp'))
        self.setGeometry(200, 200, 800, 800)

        # Etiqueta principal
        self.label = QLabel('Hello', self)
        self.label.setFont(QFont('Arial', 30))
        self.label.setGeometry(20, 20, 460, 60)
        self.label.setStyleSheet('color: white; background-color: #4CE4B3; font-weight: bold; font-style: italic;')

        # Campo de texto
        self.textbox = QLineEdit(self)
        self.textbox.setGeometry(20, 100, 300, 30)
        self.textbox.setPlaceholderText('Ingresa un nombre para esta base de datos.')

        # Botón que cambia el texto y muestra mensaje
        self.button = QPushButton('Mostrar mensaje', self)
        self.button.setGeometry(340, 100, 130, 30)
        self.button.clicked.connect(self.on_button_click)

        # Imagen
        self.image_label = QLabel(self)
        pixmap = QPixmap('meme.webp')
        self.image_label.setPixmap(pixmap.scaled(500, 500))
        self.image_label.setGeometry(150, 150, 500, 500)

    def on_button_click(self):
        texto = self.textbox.text()
        if texto:
            self.label.setText(texto)
            QMessageBox.information(self, 'Mensaje', f'¡Has escrito: {texto}!')
        else:
            QMessageBox.warning(self, 'Advertencia', 'Por favor, escribe algo en el campo de texto.')




def main():
    title = 'Base de datos'
    app = QApplication(sys.argv)
    window = MainWindow(title)
    window.show()


    sys.exit(app.exec_())


if __name__ == '__main__':
    main()