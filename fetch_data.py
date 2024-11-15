import json
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

def fetch_data():
    """Extrai dados de uma planilha Google Sheets e formata em JSON.

    Retorna:
        dict: Um dicionário contendo os dados formatados.
    """

    # Carregar credenciais (ajuste o caminho se necessário)
    SERVICE_ACCOUNT_FILE = 'credentials.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # Conectar à API Google Sheets
    service = build('sheets', 'v4', credentials=credentials)

    # Especificar a planilha e o intervalo de dados
    spreadsheet_id = '1WTp-GNFER8H4eCe-Yyvl4U0V2MMGhUR3Iw_eb5jqU4c'
    range_ = 'A1:H'  # Ajustar o intervalo conforme necessário

    # Obter os dados da planilha
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range=range_).execute()
    values = result.get('values', [])

    # Processar os dados e formatar em JSON
    data = []
    for row in values[2:]:  # Ignorar a primeira linha (cabeçalho)
        if not row:
            continue
        if len(row) < 6: # Se o evento é o mesmo para todas as trilhas (keynotes, intervalos, etc.)
            event = {
                'inicio': row[0],
                'duracao': row[1],
                'fim': row[2],
                'palestrantes': {
                    'Capivara Coders': row[4],
                    'Engenho Ops': row[4],
                    'Mirante: Olhares do Amanhã': row[4],
                    'Piradaptavel': row[4]
                }
            }
        else:
            event = {
                'inicio': row[0],
                'duracao': row[1],
                'fim': row[2],
                'palestrantes': {
                    'Capivara Coders': row[4],
                    'Engenho Ops': row[5],
                    'Mirante: Olhares do Amanhã': row[6],
                    'Piradaptavel': row[7]
                }
            }
        data.append(event)

    return json.dumps(data)

if __name__ == '__main__':
    result = fetch_data()
    print(result)