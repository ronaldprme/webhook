import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Autenticação
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credenciais.json', scope)
client = gspread.authorize(creds)

# Abre a planilha
sheet = client.open("Nome da sua planilha").worksheet("Controle de Processamento")

def atualizar_status(id_submissao, campo, valor):
    cell = sheet.find(str(id_submissao))
    if cell:
        linha = cell.row
        colunas = sheet.row_values(1)
        col_index = colunas.index(campo) + 1
        sheet.update_cell(linha, col_index, valor)

# Exemplo de uso:
atualizar_status(6190736, "CSV Gerado", f"✅ {datetime.now().strftime('%Y-%m-%d %H:%M')}")
