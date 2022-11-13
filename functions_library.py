import gspread_dataframe as gd
from random import randrange
import gspread as gs
from Google import *
import pandas as pd
import datetime
import string
import random


# Devuelve el id de los emails que contienen un asunto específico.
def get_email_id(message_subject):
    CLIENT_SECRET_FILE = './client_secret.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']

    service = Create_Service(
        CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    # Call the Gmail API to fetch INBOX
    results = service.users().messages().list(
        userId='me', labelIds=['INBOX'], maxResults=5).execute()

    messages = results.get('messages', [])

    for message in messages:
        messageResource = service.users().messages().get(
            userId="me", id=message['id']).execute()
        headers = messageResource["payload"]["headers"]

        subject = [j['value']
                   for j in headers if j["name"] == "Subject"]

        if subject[0] == message_subject:
            return message["id"]

# Elimina un mensaje de gmail


def delete_message(message_id):
    CLIENT_SECRET_FILE = "./client_secret.json"
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    service.users().messages().delete(userId='me', id=message_id).execute()
    return 'Message with id: %s deleted' % message_id

# Elimina la petición realizada


def delete_request(message_subject):
    try:
        delete_message(get_email_id(message_subject))
        return "success"
    except:
        return "No requests founded"


# Registra la actividad realizada por Aitana
def logger(tool):
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    with open('logs.txt', 'a') as the_file:
        the_file.write(f'{timestamp} | {tool} was activated\n')


# Convierte un df a una hoja de calculo de google sheet
def df_to_gsheet(sheet_id, sheet_name, df, columns):
    try:

        gc = gs.service_account(filename='service_account.json')
        sh = gc.open_by_url(
            f'https://docs.google.com/spreadsheets/d/{sheet_id}')

        ws = sh.worksheet(f'{sheet_name}')
        existing_df = gd.get_as_dataframe(ws)[columns].dropna(how='all')

        data = [existing_df, df]
        updated_df = pd.concat(data, axis=0)

        gd.set_with_dataframe(ws, updated_df)

        return "Success"

    except:
        return "Error"

# Devuelve el sheetId de la petición que contienen un asunto específico si procede


def get_sheet_id(message_subject):
    CLIENT_SECRET_FILE = './client_secret.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']

    service = Create_Service(
        CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    # Call the Gmail API to fetch INBOX
    results = service.users().messages().list(
        userId='me', labelIds=['INBOX'], maxResults=5).execute()

    messages = results.get('messages', [])

    for message in messages:
        messageResource = service.users().messages().get(
            userId="me", id=message['id']).execute()
        headers = messageResource["payload"]["headers"]

        subject = [j['value']
                   for j in headers if j["name"] == "Subject"]

        if subject[0] == message_subject:

            if len(str(messageResource["snippet"]).strip()) > 1:

                return str(messageResource["snippet"]).strip().split(" ")[0]

            else:
                return str(messageResource["snippet"]).strip()

        else:
            return "Not found"


# Convierte una hoja de calculo de google sheet a un df


def gsheet_to_df(id, sheet_name):
    gc = gs.service_account(filename='service_account.json')
    sh = gc.open_by_url(
        f'https://docs.google.com/spreadsheets/d/{id}')

    ws = sh.worksheet(f'{sheet_name}')
    df = pd.DataFrame(ws.get_all_records())
    return df


def block_approval():

    # Handle incoming Close Block request

    # Move current block to pending approval folder

    # Writing on

    # Borrado de la petición y registro de actividad en los logs del contenedor

    delete_request("Block Closer")

    logger()


def move_drive_file(source_folder_id, target_folder_id, name):
    CLIENT_SECRET_FILE = './client_secret.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ["https://www.googleapis.com/auth/drive"]

    service = Create_Service(
        CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    query = f"parents = '{source_folder_id}'"

    response = service.files().list(q=query).execute()
    files = response.get('files')

    for file in files:
        if file["name"] == name:
            service.files().update(
                fileId=file.get("id"),
                addParents=target_folder_id,
                removeParents=source_folder_id
            ).execute()


