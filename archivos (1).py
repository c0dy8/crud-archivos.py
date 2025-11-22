# ============================================================
# archivos.py
# Funciones para guardar y cargar el inventario desde archivos CSV.
# ============================================================

import csv  # Importamos el módulo CSV para leer y escribir archivos
from servicios import added_products  # Importamos la lista global de productos

# ============================================================
# Función: guardar_csv
# Guarda todos los productos en un archivo CSV
# Parámetros: 
#   - ruta: la ubicación y nombre del archivo donde se guardará
# ============================================================
def guardar_csv(ruta):
    """Guarda el inventario en un archivo CSV."""
    
    # Primero revisamos si hay productos en la lista
    if not added_products:
        print("ERROR: No hay productos para guardar.")
        return

    try:
        # Abrimos el archivo en modo escritura (w) y codificación UTF-8
        with open(ruta, mode='w', newline='', encoding='utf-8') as file:
            # Creamos un escritor de CSV usando los nombres de columna
            writer = csv.DictWriter(file, fieldnames=['name','price','quantity'])
            writer.writeheader()  # Escribimos la primera fila con los encabezados
            writer.writerows(added_products)  # Escribimos todas las filas con los productos
        print(f"Inventario guardado correctamente en: {ruta}")
    except Exception as e:
        # Captura cualquier error al escribir el archivo
        print(f"ERROR al guardar el archivo: {e}")


# ============================================================
# Función: cargar_csv
# Lee un archivo CSV y devuelve:
#   - una lista de productos válidos
#   - la cantidad de filas inválidas que se omitieron
# Parámetros:
#   - ruta: ubicación del archivo CSV a leer
# ============================================================
def cargar_csv(ruta):
    """Carga un archivo CSV y retorna lista de productos y cantidad de filas inválidas."""
    
    productos = []  # Lista donde guardaremos los productos válidos
    errores = 0     # Contador de filas inválidas

    try:
        # Abrimos el archivo en modo lectura
        with open(ruta, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)  # Creamos un lector de CSV
            # Verificamos que el encabezado sea correcto
            if reader.fieldnames != ['name','price','quantity']:
                print("ERROR: Encabezado inválido.")
                return [], 0
            # Leemos cada fila del CSV
            for row in reader:
                try:
                    # Convertimos los valores a los tipos correctos
                    name = row['name']
                    price = float(row['price'])
                    quantity = int(row['quantity'])
                    # Validamos que los números sean positivos
                    if price < 0 or quantity < 0:
                        errores += 1
                        continue
                    # Si todo está bien, agregamos a la lista
                    productos.append({'name': name, 'price': price, 'quantity': quantity})
                except (ValueError, KeyError):
                    # Si ocurre un error al convertir o faltar alguna columna
                    errores += 1

        # Retornamos los productos válidos y la cantidad de errores
        return productos, errores

    except FileNotFoundError:
        print("ERROR: Archivo no encontrado.")
        return [], 0
    except Exception as e:
        # Captura cualquier otro error al leer el archivo
        print(f"ERROR al cargar el archivo: {e}")
        return [], 0
