import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import os
import json

# CONFIGURACIÓN
creds_env = os.environ.get("GOOGLE_CREDENTIALS")
if not creds_env:
    raise ValueError("No se encontró el secreto GOOGLE_CREDENTIALS en GitHub")

SERVICE_ACCOUNT_INFO = json.loads(creds_env)
SPREADSHEET_ID = "1Q_g0OI6K4yxsdtENS75XJ_LuZgSgKmmruwF-ZcZSDzM"
SHEETS = ["Google CO", "Google CL", "Google PE", "Facebook CO", "Facebook CL", "Facebook PE", "Tiktok CL", "Tiktok PE"]
OUTPUT_PATH = "expenses_combined.csv"

# AUTENTICACIÓN
scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
credentials = Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=scopes)
client = gspread.authorize(credentials)

# DESCARGA Y COMBINACIÓN
spreadsheet = client.open_by_key(SPREADSHEET_ID)
all_dataframes = []

for sheet_name in SHEETS:
    print(f"Descargando {sheet_name}...")
    worksheet = spreadsheet.worksheet(sheet_name)
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    df["Source_Sheet"] = sheet_name
    all_dataframes.append(df)

combined_df = pd.concat(all_dataframes, ignore_index=True)
combined_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

print("✅ Archivo expenses_combined.csv generado.")
