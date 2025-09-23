import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QMessageBox, QTextEdit
from PyQt5.QtGui import QIcon, QFont, QPixmap
from BaseDatos import BaseDeDatos

DB_FILE = 'basedatos.json'



class MainWindow(QMainWindow):
    def __init__(self, title: str):
        super().__init__()
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon('meme.webp'))
        self.setGeometry(200, 200, 800, 800)
        self.db = None
        self.load_database()

        # Etiqueta principal
        self.label = QLabel('Crea una base de datos', self)
        self.label.setFont(QFont('Arial', 24))
        self.label.setGeometry(20, 20, 400, 40)

        # Campo para nombre de la base de datos
        self.db_name_input = QLineEdit(self)
        self.db_name_input.setGeometry(20, 70, 300, 30)
        self.db_name_input.setPlaceholderText('Nombre de la base de datos')

        # Botón para crear base de datos
        self.create_db_btn = QPushButton('Crear Base de Datos', self)
        self.create_db_btn.setGeometry(340, 70, 180, 30)
        self.create_db_btn.clicked.connect(self.create_database)

        # Campo para nombre de la tabla
        self.table_name_input = QLineEdit(self)
        self.table_name_input.setGeometry(20, 120, 200, 30)
        self.table_name_input.setPlaceholderText('Nombre de la tabla')

        # Campo para columnas de la tabla
        self.columns_input = QLineEdit(self)
        self.columns_input.setGeometry(240, 120, 280, 30)
        self.columns_input.setPlaceholderText('Columnas separadas por coma')

        # Botón para crear tabla
        self.create_table_btn = QPushButton('Crear Tabla', self)
        self.create_table_btn.setGeometry(540, 120, 120, 30)
        self.create_table_btn.clicked.connect(self.create_table)

        # --- NUEVO: Campos para insertar datos ---
        self.insert_label = QLabel('Insertar datos en tabla', self)
        self.insert_label.setFont(QFont('Arial', 16))
        self.insert_label.setGeometry(20, 400, 300, 30)

        self.insert_table_input = QLineEdit(self)
        self.insert_table_input.setGeometry(20, 440, 200, 30)
        self.insert_table_input.setPlaceholderText('Tabla destino')

        self.insert_data_input = QLineEdit(self)
        self.insert_data_input.setGeometry(240, 440, 400, 30)
        self.insert_data_input.setPlaceholderText('Datos: columna1=valor1, columna2=valor2...')

        self.insert_btn = QPushButton('Insertar', self)
        self.insert_btn.setGeometry(660, 440, 100, 30)
        self.insert_btn.clicked.connect(self.insert_data)

        # --- NUEVO: Consulta de datos ---
        self.query_label = QLabel('Consultar datos de tabla', self)
        self.query_label.setFont(QFont('Arial', 16))
        self.query_label.setGeometry(20, 490, 300, 30)

        self.query_table_input = QLineEdit(self)
        self.query_table_input.setGeometry(20, 530, 200, 30)
        self.query_table_input.setPlaceholderText('Tabla a consultar')

        self.query_btn = QPushButton('Consultar', self)
        self.query_btn.setGeometry(240, 530, 100, 30)
        self.query_btn.clicked.connect(self.query_data)

        self.query_result_area = QTextEdit(self)
        self.query_result_area.setGeometry(20, 570, 760, 200)
        self.query_result_area.setReadOnly(True)
        self.query_result_area.setFont(QFont('Consolas', 12))

        self.structure_area = QTextEdit(self)
        self.structure_area.setGeometry(20, 180, 760, 200)
        self.structure_area.setReadOnly(True)
        self.structure_area.setFont(QFont('Consolas', 12))
        self.show_structure()

    def save_database(self):
        if self.db:
            data = {
                'nombre': self.db.nombre,
                'tablas': {}
            }
            for nombre_tabla, tabla in self.db.tablas.items():
                data['tablas'][nombre_tabla] = {
                    'columnas': list(tabla.columnas),
                    'filas': tabla.filas
                }
            with open(DB_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

    def load_database(self):
        if os.path.exists(DB_FILE):
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.db = BaseDeDatos(data['nombre'])
            for nombre_tabla, info in data['tablas'].items():
                self.db.crear_tabla(nombre_tabla, info['columnas'])
                tabla = self.db.obtener_tabla(nombre_tabla)
                for fila in info['filas']:
                    tabla.insertar(fila)

    def create_database(self):
        nombre = self.db_name_input.text().strip()
        if nombre:
            self.db = BaseDeDatos(nombre)
            self.label.setText(f"Base de datos: {nombre}")
            self.structure_area.setText("")
            self.save_database()
            QMessageBox.information(self, 'Base de datos', f"Base de datos '{nombre}' creada.")
        else:
            QMessageBox.warning(self, 'Advertencia', 'Debes ingresar un nombre para la base de datos.')

    def create_table(self):
        if not self.db:
            QMessageBox.warning(self, 'Advertencia', 'Primero crea una base de datos.')
            return
        nombre_tabla = self.table_name_input.text().strip()
        columnas = [col.strip() for col in self.columns_input.text().split(',') if col.strip()]
        if nombre_tabla and columnas:
            exito = self.db.crear_tabla(nombre_tabla, columnas)
            self.show_structure()
            self.save_database()
            if exito:
                QMessageBox.information(self, 'Tabla', f"Tabla '{nombre_tabla}' creada.")
            else:
                QMessageBox.warning(self, 'Advertencia', f"La tabla '{nombre_tabla}' ya existe.")
        else:
            QMessageBox.warning(self, 'Advertencia', 'Debes ingresar nombre y columnas para la tabla.')

    def insert_data(self):
        if not self.db:
            QMessageBox.warning(self, 'Advertencia', 'Primero crea una base de datos.')
            return
        nombre_tabla = self.insert_table_input.text().strip()
        datos_raw = self.insert_data_input.text().strip()
        if not nombre_tabla or not datos_raw:
            QMessageBox.warning(self, 'Advertencia', 'Debes ingresar tabla y datos.')
            return
        tabla = self.db.obtener_tabla(nombre_tabla)
        if not tabla:
            QMessageBox.warning(self, 'Advertencia', f"La tabla '{nombre_tabla}' no existe.")
            return
        datos = {}
        for par in datos_raw.split(','):
            if '=' in par:
                k, v = par.split('=', 1)
                datos[k.strip()] = v.strip()
        exito = tabla.insertar(datos)
        self.save_database()
        if exito:
            QMessageBox.information(self, 'Inserción', f"Datos insertados en '{nombre_tabla}'.")
        else:
            QMessageBox.warning(self, 'Error', 'Las columnas no coinciden con la estructura de la tabla.')

    def query_data(self):
        if not self.db:
            QMessageBox.warning(self, 'Advertencia', 'Primero crea una base de datos.')
            return
        nombre_tabla = self.query_table_input.text().strip()
        tabla = self.db.obtener_tabla(nombre_tabla)
        if not tabla:
            QMessageBox.warning(self, 'Advertencia', f"La tabla '{nombre_tabla}' no existe.")
            return
        filas = tabla.seleccionar()
        texto = f"Filas en '{nombre_tabla}':\n"
        for fila in filas:
            texto += str(fila) + '\n'
        self.query_result_area.setText(texto)

    def show_structure(self):
        if self.db:
            texto = f"Estructura de la base de datos '{self.db.nombre}':\n"
            if not self.db.tablas:
                texto += "(No hay tablas en la base de datos)\n"
            for nombre_tabla, tabla in self.db.tablas.items():
                texto += f"- Tabla: {nombre_tabla} | Columnas: {', '.join(tabla.columnas)}\n"
            self.structure_area.setText(texto)




def main():
    title = 'Base de datos'
    app = QApplication(sys.argv)
    window = MainWindow(title)
    window.show()


    sys.exit(app.exec_())


if __name__ == '__main__':
    main()