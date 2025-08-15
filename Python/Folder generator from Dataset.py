# Programa para hacer Carpetas múltiples a través de un Dataset en Excel

## Instrucciones:

1. El Dataset debe ser guardado en Excel (xls, xlsx, csv). Empezar desde la celda A1 y evita los encabezados
2. En la línea de comando de Python se solicitará "cargar el archivo". No importa la ruta, tú la puedes seleccionar manualmente
3. El código hará lo suyo y te descargará un ZIP file donde contendrá las carpetas que requieres en el Dataset.
4. Una vez teniendo el ZIP file, sólo extraes y  . . . **LISTO!!!**




import pandas as pd
import zipfile
import re
from google.colab import files

def limpiar_nombre_carpeta(nombre):
    """Limpia espacios y reemplaza caracteres inválidos para carpetas."""
    nombre = str(nombre).strip()
    # Reemplazar caracteres inválidos por guion bajo
    nombre = re.sub(r'[\\/*?:"<>|]', '_', nombre)
    return nombre

# === 1) Subir el archivo ===
print("📂 Selecciona el archivo Excel o CSV con la lista de carpetas:")
uploaded = files.upload()
archivo = next(iter(uploaded))

# === 2) Configuración: indica si tu archivo tiene encabezado ===
TIENE_ENCABEZADO = False  # Cambia a True si tu archivo tiene encabezado en la primera fila

# === 3) Leer archivo según extensión ===
if archivo.lower().endswith(('.xlsx', '.xls')):
    df = pd.read_excel(archivo, header=0 if TIENE_ENCABEZADO else None)
elif archivo.lower().endswith('.csv'):
    df = pd.read_csv(archivo, header=0 if TIENE_ENCABEZADO else None)
else:
    raise ValueError("Formato no soportado. Usa Excel (.xlsx, .xls) o CSV (.csv)")

# === 4) Tomar primera columna, limpiar y quitar duplicados ===
carpetas = df.iloc[:, 0].dropna().unique()
carpetas_limpias = [limpiar_nombre_carpeta(c) for c in carpetas if str(c).strip()]

# === 5) Crear ZIP con carpetas ===
zip_filename = "carpetas_desde_archivo.zip"
with zipfile.ZipFile(zip_filename, 'w') as zipf:
    for folder_name in carpetas_limpias:
        zipf.writestr(folder_name + '/', '')  # Crea carpeta vacía en ZIP

# === 6) Descargar ZIP ===
files.download(zip_filename)

print(f"✅ ZIP creado con {len(carpetas_limpias)} carpetas.")

