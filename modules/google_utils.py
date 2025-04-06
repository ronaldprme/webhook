import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials

filename = os.path.join(os.path.dirname(__file__), "figueira-455418-fa0bcb3c99a0.json")
def get_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(filename, scope)
    client = gspread.authorize(creds)
    sheet = client.open("TESTE DE TRAUMA 2025").sheet1
    try:
       print("Autenticação bem-sucedida!")
    except Exception as e:
       print(f"Erro na autenticação: {e}")
    # Listar todas as planilhas disponíveis
    print("Planilhas disponíveis:")
    return sheet

def ler_planilha(nome_planilha):
    sheet = get_sheet()
    dados = sheet.get_all_records()
    registros = [row for row in dados if not row.get("Status Report")]
    return registros

def atualizar_status(submission_id):
    sheet = get_sheet()
    try:
        # Certifique-se de que submission_id é uma string
        submission_id = str(submission_id).strip()
        # Procura o submission_id na planilha
        cell = sheet.find(submission_id)
        col = sheet.row_values(1).index("Status Report") + 1
        sheet.update_cell(cell.row, col, "Gerado")
        return True
    except gspread.CellNotFound:  # Exceção corrigida
        print(f"Erro: submission_id '{submission_id}' não encontrado na planilha.")
        return False

def atualizar_envio(submission_id):
    sheet = get_sheet()
    submission_id = str(submission_id).strip()
    cell = sheet.find(submission_id)
    # cell = sheet.find(str(submission_id))
    col = sheet.row_values(1).index("Envio") + 1
    sheet.update_cell(cell.row, col, "Concluido")
    return True

