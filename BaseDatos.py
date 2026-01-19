# -- coding: utf-8 --
from typing import List, Dict, Any, Set, Optional

class BaseDeDatos:
    """
    Representa una base de datos simple que contiene múltiples tablas.
    """
    def __init__(self, nombre: str):
        """
        Inicializa la base de datos con un nombre.

        Args:
            nombre (str): El nombre de la base de datos.
        """
        self.nombre = nombre
        self.tablas: Dict[str, 'Tabla'] = {}

    def crear_tabla(self, nombre_tabla: str, columnas: List[str]) -> bool:
        """
        Crea una nueva tabla en la base de datos.

        Args:
            nombre_tabla (str): El nombre de la tabla a crear.
            columnas (List[str]): Una lista con los nombres de las columnas.

        Returns:
            bool: True si la tabla se creó con éxito, False si ya existía.
        """
        if nombre_tabla not in self.tablas:
            self.tablas[nombre_tabla] = Tabla(nombre_tabla, columnas)
            print(f"Tabla '{nombre_tabla}' creada con éxito.")
            return True
        print(f"⚠  Advertencia: La tabla '{nombre_tabla}' ya existe.")
        return False

    def obtener_tabla(self, nombre_tabla: str) -> Optional['Tabla']:
        """
        Obtiene un objeto Tabla de la base de datos de forma segura. # <-- MEJORA: Encapsulación

        Args:
            nombre_tabla (str): El nombre de la tabla a obtener.

        Returns:
            Optional['Tabla']: El objeto Tabla si existe, de lo contrario None.
        """
        return self.tablas.get(nombre_tabla)

    def mostrar_estructura(self):
        """
        Muestra la estructura de todas las tablas en la base de datos.
        """
        print(f"\n🏛  Estructura de la base de datos '{self.nombre}':")
        if not self.tablas:
            print("   (No hay tablas en la base de datos)")
        for nombre_tabla, tabla in self.tablas.items():
            print(f"   - Tabla: {nombre_tabla} | Columnas: {', '.join(tabla.columnas)}")
        print()


class Tabla:
    """
    Representa una tabla en la base de datos, con columnas y filas.
    """
    def __init__(self, nombre: str, columnas: List[str]):
        """
        Inicializa la tabla.

        Args:
            nombre (str): El nombre de la tabla.
            columnas (List[str]): Una lista de nombres de columnas.
        """
        self.nombre = nombre
        self.columnas: Set[str] = set(columnas) # <-- MEJORA: Usar un 'set' para búsquedas más rápidas
        self.filas: List[Dict[str, Any]] = []

    def insertar(self, datos: Dict[str, Any]) -> bool:
        """
        Inserta una nueva fila (diccionario) en la tabla.
        # <-- MEJORA: Validación estricta de columnas.
        Ahora verifica que todas las columnas requeridas estén presentes.
        """
        if self.columnas != set(datos.keys()):
            print(f"Error de inserción: Las columnas proporcionadas no coinciden con la estructura de la tabla '{self.nombre}'.")
            print(f"   Columnas requeridas: {self.columnas}")
            print(f"   Columnas dadas:      {set(datos.keys())}")
            return False

        self.filas.append(datos)
        return True

    def seleccionar(self, condiciones: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Selecciona filas que cumplen con ciertas condiciones.

        Args:
            condiciones (Optional[Dict[str, Any]]): Un diccionario de {columna: valor} para filtrar.
                                                   Si es None, devuelve todas las filas.

        Returns:
            List[Dict[str, Any]]: Una lista de filas que cumplen las condiciones.
        """
        if not condiciones:
            return self.filas

        resultados = []
        for fila in self.filas:
            # all() es una forma más concisa de verificar que todas las condiciones se cumplan
            if all(fila.get(columna) == valor for columna, valor in condiciones.items()):
                resultados.append(fila)
        return resultados

    def actualizar(self, condiciones: Dict[str, Any], actualizaciones: Dict[str, Any]) -> int:
        """
        Actualiza una o más filas que cumplan con las condiciones.

        Args:
            condiciones (Dict[str, Any]): Las condiciones que deben cumplir las filas a actualizar.
            actualizaciones (Dict[str, Any]): Los campos a actualizar con sus nuevos valores.

        Returns:
            int: El número de filas actualizadas.
        """
        contador = 0
        for fila in self.filas:
            if all(fila.get(columna) == valor for columna, valor in condiciones.items()):
                for columna, nuevo_valor in actualizaciones.items():
                    if columna in self.columnas:
                        fila[columna] = nuevo_valor
                contador += 1
        return contador

    def eliminar(self, condiciones: Dict[str, Any]) -> int:
        """
        Elimina filas que cumplan con las condiciones.

        Args:
            condiciones (Dict[str, Any]): Las condiciones que deben cumplir las filas a eliminar.

        Returns:
            int: El número de filas eliminadas.
        """
        filas_a_mantener = []
        filas_eliminadas = 0

        for fila in self.filas:
            if all(fila.get(columna) == valor for columna, valor in condiciones.items()):
                filas_eliminadas += 1
            else:
                filas_a_mantener.append(fila)

        if filas_eliminadas > 0:
            self.filas = filas_a_mantener

        return filas_eliminadas


# --- Ejemplo de Uso Mejorado ---
if __name__ == "__main__":
    # Crear base de datos
    escuela_db = BaseDeDatos("Colegio Moderno")

    # Crear tablas
    escuela_db.crear_tabla("Estudiantes", ["id", "nombre", "edad", "curso_id"])
    escuela_db.crear_tabla("Cursos", ["id_curso", "nombre_curso", "profesor"])

    # Mostrar estructura
    escuela_db.mostrar_estructura()

    # Obtener tablas de forma segura
    tabla_estudiantes = escuela_db.obtener_tabla("Estudiantes")
    tabla_cursos = escuela_db.obtener_tabla("Cursos")

    if tabla_estudiantes and tabla_cursos:
        # --- Insertar datos ---
        print("\n--- Insertando Datos ---")
        tabla_estudiantes.insertar({"id": 1, "nombre": "Ana Torres", "edad": 15, "curso_id": 101})
        tabla_estudiantes.insertar({"id": 2, "nombre": "Luis Castro", "edad": 16, "curso_id": 102})
        tabla_estudiantes.insertar({"id": 3, "nombre": "Marta Rivas", "edad": 15, "curso_id": 101})

        # Intento de inserción inválido (faltan columnas)
        print("\n-> Intentando inserción inválida...")
        tabla_estudiantes.insertar({"id": 4, "nombre": "Carlos"})

        tabla_cursos.insertar({"id_curso": 101, "nombre_curso": "Matemáticas", "profesor": "Prof. García"})
        tabla_cursos.insertar({"id_curso": 102, "nombre_curso": "Literatura", "profesor": "Prof. Pérez"})

        # --- Consultar datos ---
        print("\n--- Consultando Datos ---")
        print("Todos los estudiantes:")
        for estudiante in tabla_estudiantes.seleccionar():
            print(f"   {estudiante}")

        print("\nEstudiantes del curso 101:")
        for estudiante in tabla_estudiantes.seleccionar({"curso_id": 101}):
            print(f"   {estudiante}")

        # --- Actualizar datos ---
        print("\n--- Actualizando Datos ---")
        actualizados = tabla_estudiantes.actualizar(
            condiciones={"nombre": "Ana Torres"},
            actualizaciones={"edad": 16}
        )
        print(f"Se actualizó la edad de Ana. Filas afectadas: {actualizados}")

        # --- Eliminar datos ---
        print("\n--- Eliminando Datos ---")
        eliminados = tabla_estudiantes.eliminar({"nombre": "Luis Castro"})
        print(f"Se eliminó a Luis. Filas afectadas: {eliminados}")

        # --- Resultados finales ---
        print("\n--- Resultados Finales ---")
        print("Estudiantes después de actualizar y eliminar:")
        for estudiante in tabla_estudiantes.seleccionar():
            print(f"   {estudiante}")