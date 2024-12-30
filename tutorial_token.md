# Tutorial: Manipulación de Google Spreadsheets con Python y Pandas

Este tutorial describe cómo acceder a un archivo CSV almacenado en Google Drive, procesarlo con Pandas y cargarlo de nuevo a Google Sheets. Incluye los detalles para la configuración de los requisitos previos (instalación de paquetes, configuración de archivos extras, etc.).

---

## Requisitos previos

Antes de comenzar, asegúrate de tener:

1. **Python instalado** (preferiblemente >= 3.7). Sería ideal si se trabaja con la versión 3.10, por lo tanto si puede elegir esta versión asegúrese de que sea dicha versión. Se hace hincapié en la versión 3.10 ya que hemos estado utilizando esta versión y no ha proporcionado problemas de compatibilidad con el resto de los requerimientos.
2. Las siguientes librerías instaladas:
   - `pandas`: Para la manipulación de datos en formato DataFrame.
   - `google-auth`: Para gestionar la autenticación con las APIs de Google.
   - `google-auth-oauthlib`: Para el flujo de autenticación OAuth 2.0.
   - `google-api-python-client`: Para interactuar con la API de Google Sheets.
3. Una cuenta de Google activa. Este paso ya se realizó con éxito, por lo que se le proporcionará los links correspondientes para acceder a los archivos csv en el Google Drive.
4. Credenciales JSON generadas desde la consola de Google Cloud Platform (GCP), que deberás descargar y guardar localmente. Este paso ya fue realizado con éxito, se le proporcionará el archivo JSON con las credenciales.
5. Un archivo de Google Spreadsheet existente donde realizarás las operaciones. Dicho archivo ya existe, se le proveerá el correspondinete link.

Instala las librerías necesarias usando pip:

```bash
pip install pandas google-auth google-auth-oauthlib google-api-python-client
```
Si no cuenta con la herramienta pip puede visitar el siguiente link para su instalación: https://pip.pypa.io/en/stable/installation/

---

## Paso 1: Configuración inicial

### Importación de librerías
Primero, importamos todas las librerías necesarias:

```python
import os
import time
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
```

### Configuración de rutas de archivos
Debemos especificar las rutas donde se almacenarán los archivos de credenciales y el token generado. Esto es importante para que el script pueda reutilizar el token y evitar solicitudes repetidas de autenticación. Se le proporcionará un archivo con el token. Sin embargo, dado que su validación caduca luego de un período de tiempo, es necesario crearlo manualmente, proceso que se explicará en el **Paso 2**:

```python
TOKEN = "token_sf.json"  # Ruta del archivo token
CREDENTIALS = "credentials_sf.json"  # Ruta del archivo de credenciales
```
En TOKEN se almacena la ruta para el archivo JSON con el token y en CREDENTIALS la ruta para el archivo JSON con las credenciales. Se deben completar/modificar para que coincidan con la ruta de los archivos en la carpeta de su proyecto.

### Configuración de alcance (scopes) e identificadores
Definimos el alcance de los permisos necesarios y configuramos el identificador de la hoja de cálculo que deseamos manipular:

```python
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]  # Permiso de lectura y escritura
SPREADSHEET_ID = "<TU_SPREADSHEET_ID>"  # Reemplaza con el ID de tu hoja
LINK = "<TU_ENLACE_A_GOOGLE_SHEET>"  # URL de la hoja de cálculo
```

> **Nota:** El `SPREADSHEET_ID` es la parte de la URL entre `/d/` y `/edit`.

Se realizó una copia de la planilla de stock de la sede de San Fernando. El archivo se denominó *bot_20_test.csv*. A continuación se proveen el LINK y el SPREADSHEET_ID, así puede completar los campos solicitados anteriormente.

```python
SPREADSHEET_ID = "1t3Lp0MdTQV06P1oqKpk5WDhSuxkSAosZ0gFPgZnHpcA"
LINK = "(https://docs.google.com/spreadsheets/d/1t3Lp0MdTQV06P1oqKpk5WDhSuxkSAosZ0gFPgZnHpcA/edit?usp=share_link)"
```

---

## Paso 2: Autenticación

La autenticación es necesaria para interactuar con la API de Google Sheets. Este paso utiliza OAuth 2.0 para garantizar acceso seguro.

### Verificación de credenciales existentes
El script verifica si ya existe un token generado previamente. Si existe y es válido, lo reutiliza:

```python
credentials = None
if os.path.exists(TOKEN):
    credentials = Credentials.from_authorized_user_file(TOKEN, SCOPES)
```

### Manejo de tokens caducados o inexistentes
Si no hay un token existente, o si este ha caducado, el script realiza el flujo de autenticación OAuth 2.0 para generar uno nuevo:

```python
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS, SCOPES)
        credentials = flow.run_local_server(port=0)

    with open(TOKEN, "w") as token:
        token.write(credentials.to_json())
```

Si el token expiró, al itentar generar uno nuevo abrirá una pestaña en su navegador y le requerirá iniciar sesión. Para ello debe utilizar los datos de la cuenta de gmail asociada al proyecto:

EMAIL: orienopenfarma1@gmail.com
CONTRASEÑA: B$mWFnh7

---

## Paso 3: Leer los datos de la hoja de cálculo

En este paso, conectamos con la API de Google Sheets para obtener los datos de un rango específico en nuestra hoja de cálculo.

### Construcción del servicio de Google Sheets
Creamos un objeto de servicio para interactuar con la API:

```python
service = build("sheets", "v4", credentials=credentials)
sheets = service.spreadsheets()
```

### Obtención de valores del rango especificado
Se especifica el rango de celdas de las que deseamos obtener los datos. La respuesta se procesa para extraer los valores:

```python
try:
    result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range="bot_20_test!A:F").execute()
    values = result.get("values", [])
except HttpError as error:
    print(error)
```

Si el rango especificado está vacío, `values` será una lista vacía. En la variable *range* se especifica el nombre del archivo y las columnas, es decir `<nombre_archivo>!<columna_inicio>:<columna_final>`, como por ejemplo en este caso `bot_20_test!A:F`.

---

## Paso 4: Convertir los datos a un DataFrame de Pandas

Una vez obtenidos los datos, los convertimos en un DataFrame de Pandas para facilitar su manipulación.

### Creación del DataFrame
Si se encontraron datos en la hoja de cálculo, los dividimos en encabezados y filas, y creamos un DataFrame:

```python
if values:
    headers = values[0]  # Primera fila como encabezados
    data = values[1:]    # Resto de las filas como datos
    df = pd.DataFrame(data, columns=headers)
else:
    df = pd.DataFrame()  # DataFrame vacío si no hay datos
```

### Modificaciones al DataFrame
1. **Renombrar columnas:** Cambiamos los nombres de las columnas para facilitar el trabajo con ellas.
2. **Transformaciones de datos:** Convertimos los datos a tipos apropiados (por ejemplo, de texto a números) y aplicamos un descuento.

```python
# Renombrar columnas
original_names = df.columns.tolist()
df.columns = ["codigo", "ean", "stock", "precio", "promo", "descripcion"]

# Limpiar y transformar datos
df['precio'] = df['precio'].astype('float') 
df['stock'] = df['stock'].astype(str).apply(lambda x: x.replace('.', ''))
df['stock'] = df['stock'].astype(int)

# Aplicar descuento
df['precio'] = df['precio'] * 0.9

# Restaurar nombres originales
df.columns = original_names
```

Cabe aclarar que la modificación que se aplicó, en este caso un descuento del 10%, es a modo de ejemplo. Aquí el usuario debe modificar a gusto y/o necesidad las celdas que sean necesarias, incluso si desea modificar, disminuir o aumentar la totalidad de la información. 

---

## Paso 5: Actualizar la hoja de cálculo

Finalmente, cargamos el DataFrame actualizado de vuelta a Google Sheets.

### Preparación de los datos para carga
Convertimos el DataFrame en una lista de listas, incluyendo los encabezados:

```python
RANGE_NAME = "bot_20_test!A:F"
updated_values = [df.columns.tolist()] + df.astype(str).values.tolist()
body = {"values": updated_values}
```

### Manejo de reintentos
Para manejar errores transitorios al interactuar con la API, implementamos un mecanismo de reintentos:

```python
MAX_RETRIES = 3
RETRY_DELAY = 5

for attempt in range(1, MAX_RETRIES + 1):
    try:
        sheets.values().update(
            spreadsheetId=SPREADSHEET_ID, 
            range=RANGE_NAME, 
            valueInputOption="RAW", 
            body=body
        ).execute()
        print("Spreadsheet updated successfully.")
        break
    except HttpError as e:
        print(f"Attempt {attempt} failed with error: {e}")
        if attempt < MAX_RETRIES:
            print(f"Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)
        else:
            print("All retry attempts failed. Exiting.")
            raise
```

---

## Consideraciones finales

1. **Gestión de errores:** Implementa reintentos para manejar errores transitorios en la API de Google Sheets.
2. **Seguridad:** No compartas tus credenciales JSON o token de autenticación.
3. **Escalabilidad:** Divide lógicas complejas en funciones reutilizables.

Con este tutorial detallado, usted podrá manipular Google Sheets de forma eficiente con Python, modificar la información y actualizar el archivo en el Google Drive.