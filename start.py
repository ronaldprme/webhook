"""
start.py
- Lê dados do Google Sheets
- Gera respostas.csv
- Chama main.py para gerar relatórios
- Atualiza Google Sheets com status e envio
"""
from modules.google_utils import ler_planilha, atualizar_status, atualizar_envio
from modules.relatorio_service import processar_respostas
from modules.email_utils import enviar_email_com_anexo

import subprocess
import csv

def iniciar_processo(dados):
    print("🚀 Iniciando todo o processo com os dados:")
    print(dados)
    
	# converter dados lidos jsom em respostas.csv ou alterar a leitura dos dados no codigo

    # 1. Ler planilha e salvar dados em respostas.csv
    registros = ler_planilha("TESTE DE TRAUMA 2025")
    # respostas_path = "data/respostas.csv"
    
    if not registros:
        print("[AVISO] Nenhum registro encontrado com status em branco.")
        exit(0)  # ou continue, ou return, dependendo do contexto
    # with open(respostas_path, "w", newline='', encoding="utf-8") as f:
    with open(dados, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=registros[0].keys())
        writer.writeheader()
        writer.writerows(registros)

    # 2. Rodar geração de relatórios
    processar_respostas("data/respostas.csv", "data/paragrafos.csv")
    # subprocess.run(["python3", "main.py"])

    # 3. Atualizar status e envio
    for r in registros:
        email = r.get("E-mail")
        submission_id = str(r.get("ID Submission"))
        id = submission_id[:7]  # Obtém os primeiros 7 caracteres de submission_id
        print(submission_id)
        nome = r.get("Nome") # + " " + r.get("Sobrenome")
        arquivo_pdf = f"output/relatorios/Teste_de_Trauma_{id}_{nome}.pdf"
        status_atualizado = atualizar_status(submission_id)
        if status_atualizado:
            if enviar_email_com_anexo(email, arquivo_pdf, nome):
                atualizar_envio(submission_id)

if __name__ == '__main__':
    iniciar_processo({})