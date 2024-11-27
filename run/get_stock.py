import os, random
import pandas as pd
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request

TOKEN = os.getcwd() + "/json/token_sf.json"
CREDENTIALS = os.getcwd() + "/json/credentials_sf.json"

# Scope and spreadsheet ID configuration
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1ulAoStGq7pI5pTSA1H1WKVGcf5vjVhf_CUPsJHBKuNM"  # Replace with your sheet ID
LINK = "https://docs.google.com/spreadsheets/d/1ulAoStGq7pI5pTSA1H1WKVGcf5vjVhf_CUPsJHBKuNM/edit?gid=1840576660#gid=1840576660"

# Load credentials
credentials = None
if os.path.exists(TOKEN):
    credentials = Credentials.from_authorized_user_file(TOKEN, SCOPES)

# Refresh or obtain new credentials if necessary
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS, SCOPES)
        credentials = flow.run_local_server(port=0)
    with open(TOKEN, "w") as token:
        token.write(credentials.to_json())

# Access the Google Sheets API and retrieve data
try:
    service = build("sheets", "v4", credentials=credentials)
    sheets = service.spreadsheets()
    result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range="bot_20!A:F").execute()
    values = result.get("values", [])
    if values:
        print("Data retrieved successfully.")
    else:
        print("No data found.")
except HttpError as error:
    print("An error occurred:", error)

# Convert the data to a DataFrame
if values:
    headers = values[0]
    data = values[1:]
    df = pd.DataFrame(data, columns=headers)
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
else:
    df = pd.DataFrame()

# Change 'promo' column with random values
# sales = ['No promo', '4x3', '3x2', '2x1', '50%', '30%', '20%', '10%']
# weights = [0.1] + (len(sales)-1) * [0.9 / (len(sales)-1)]
# df['promo'] = random.choices(sales, weights=weights, k=len(df))

# Remove rows with 'stock' column equal to 0
df = df[df.iloc[:, 2] > 0]

# Rename columns
df.columns = ["codigo", "ean", "stock", "precio", "promo", "descripcion"]

# Save the DataFrame to a CSV file
file_path = os.getcwd() + "/database/stock.csv"
df.to_csv(file_path, index=False)