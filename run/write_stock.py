'''
Este script primero lee una hoja de calculo de google sheets. 
Trae los datos, los pone en un dataframe, modifica una columna y finaliza escribiendo esa columna en la hoja de calculo de 
google sheets de donde vinieron los datos. 
'''

import os, time
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Definir los directorios del token y las credenciales (archivos json)
TOKEN = os.getcwd() + "/json/token_sf.json"
CREDENTIALS = os.getcwd() + "/json/credentials_sf.json"


# Scope and spreadsheet ID configuration
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1ulAoStGq7pI5pTSA1H1WKVGcf5vjVhf_CUPsJHBKuNM"  # Replace with your sheet ID
LINK = "https://docs.google.com/spreadsheets/d/1ulAoStGq7pI5pTSA1H1WKVGcf5vjVhf_CUPsJHBKuNM/edit?gid=1840576660#gid=1840576660"


credentials = None
if os.path.exists(TOKEN):
    credentials = Credentials.from_authorized_user_file(TOKEN, SCOPES)
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

    else:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS, SCOPES)
        credentials = flow.run_local_server(port=0)

    with open(TOKEN, "w") as token:
        token.write(credentials.to_json())

try:
    service = build("sheets", "v4", credentials=credentials)
    sheets = service.spreadsheets()

    result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range="bot_20!A:F").execute()
    values = result.get("values", [])


except HttpError as error:
    print(error)


# convierto la importacion a dataframe

if values:
        headers = values[0]
        data = values[1:]
        df = pd.DataFrame(data, columns=headers)
else:
        df = pd.DataFrame()

# Renombro las columnas para ahcer modificaciones
original_names = df.columns.tolist()
df.columns = ["codigo", "ean", "stock", "precio", "promo", "descripcion"]

df['precio'] = df['precio'].astype('float') 
df['stock'] = df['stock'].astype(str).apply(lambda x: x.replace('.', ''))
df['stock'] = df['stock'].astype(int)

# modifico la columna de precios
df['precio'] = df['precio'] * 0.9

# Vuelvo las columnas a sus nombres originales
df.columns = original_names

# Escribo la hoja de cálculo
RANGE_NAME = "bot_20!A:F"  # Adjust this to match your spreadsheet's range
updated_values = [df.columns.tolist()] + df.astype(str).values.tolist()
body = {"values": updated_values}

# Configurar el número máximo de reintentos y el retraso entre ellos
MAX_RETRIES = 3
RETRY_DELAY = 5  # en segundos

for attempt in range(1, MAX_RETRIES + 1):
    try:
        # Intentar actualizar la hoja de cálculo
        sheets.values().update(
            spreadsheetId=SPREADSHEET_ID, 
            range=RANGE_NAME, 
            valueInputOption="RAW", 
            body=body
        ).execute()
        print("Spreadsheet updated successfully.")
        break  # Salir del bucle si se ejecuta con éxito
    except HttpError as e:
        print(f"Attempt {attempt} failed with error: {e}")
        if attempt < MAX_RETRIES:
            print(f"Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)  # Esperar antes de reintentar
        else:
            print("All retry attempts failed. Exiting.")
            raise  # Re-lanzar la excepción si se agotaron los reintentos