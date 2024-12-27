import os, gspread
import pandas as pd
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials

SPREADSHEET_ID = "1ulAoStGq7pI5pTSA1H1WKVGcf5vjVhf_CUPsJHBKuNM"
LINK = "https://docs.google.com/spreadsheets/d/1ulAoStGq7pI5pTSA1H1WKVGcf5vjVhf_CUPsJHBKuNM/edit?gid=1840576660#gid=1840576660"
SERVICE_ACCOUNT_FILE = os.getcwd() + "/json/credentials.json"
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets"
]

# Autenticación con la cuenta de servicio
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Crear cliente de gspread con las credenciales
gc = gspread.authorize(credentials)

# Access the Google Sheets API and retrieve data
try:
    spreadsheet = gc.open_by_key(SPREADSHEET_ID)    # Abrir el archivo de Google Spreadsheet usando su ID
    worksheet = spreadsheet.sheet1                  # O usa .worksheet("Nombre de la hoja")
    data = worksheet.get_all_values()               # leer datos actuales
    if data:
        print(f"Data retrieved successfully. {len(data)-1} products.")
    else:
        print("No data found.")

except HttpError as error:
    print("An error occurred:", error)


# Convertir los datos a un DataFrame de pandas
df = pd.DataFrame(data[1:], columns=data[0])
# Columns:
# "codigo_fcia" -> código de farmacia (sede)
# "ean" -> identificador del producto
# "stock" -> cantidad de unidades en existencia
# "precio_vta" -> precio de venta
# "promocion" -> promoción del producto
# "descrip" -> descripción del producto

# Adjust stock value
df.iloc[:, 2] = df.iloc[:, 2].astype(str).apply(lambda x: x.replace('.', ''))
df.iloc[:, 2] = df.iloc[:, 2].astype(int)
# Adjust price format
df.iloc[:, 3] = df.iloc[:, 3].astype('float')

# Remove rows with 'stock' column equal to 0
df = df[df.iloc[:, 2] > 0]

# Rename columns
df.columns = ["codigo", "ean", "stock", "precio", "promo", "descripcion"]

# Save the DataFrame to a CSV file
file_path = os.getcwd() + "/database/stock.csv"
df.to_csv(file_path, index=False)