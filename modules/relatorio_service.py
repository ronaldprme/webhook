
from modules.processador import carregar_respostas, carregar_paragrafos, organizar_perguntas_por_sessao, normalizar
from modules.gerador_pdf import gerar_relatorio
from datetime import datetime
import pandas as pd
import re

def interpretar_total(valor):
    try:
        total = int(valor)
        if 0 < total <= 74:
            return "T1", "Sinais <b>LEVES</b> de trauma"
        elif 75 < total <= 149:
            return "T2", "Sinais <b>MODERADOS</b> de trauma"
        elif 150 < total <= 224:
            return "T3", "Sinais <b>SIGNIFICATIVOS</b> de trauma"
        elif 225 < total <= 300:
            return "T4", "Sinais <b>SEVEROS</b> de trauma"
    except:
        return "T?", "SINAIS DESCONHECIDOS"
    return "T?", "SINAIS DESCONHECIDOS"

def processar_respostas(caminho_respostas, caminho_paragrafos):
    perguntas, respostas_df = carregar_respostas(caminho_respostas)
    paragrafos_df = carregar_paragrafos(caminho_paragrafos)
    sessoes = organizar_perguntas_por_sessao(paragrafos_df)

    mapa_colunas = {}
    for col in perguntas:
        if "." in col:
            pid = col.split(".")[0].strip()
            mapa_colunas[pid] = col

    for i, linha in respostas_df.iterrows():
        nome = linha.get('NOME', f"Respondente_{i+1}")
        sobrenome = linha.get('SOBRENOME', f"Respondente_Sobrenome{i+1}")
        email = linha.get('E-MAIL', "email@exemplo.com")
        # submission_id = linha.get('SUBMISSIONID', f"ID_{i+1}")
        submission_id = str(linha.get('SUBMISSIONID', f"ID_{i+1}"))[:7]  # Converte para string antes do slicing
        submission_date_raw = linha.get('SUBMISSIONDATE', "Data desconhecida")
        try:
            submission_date = datetime.strptime(submission_date_raw, '%b. %d, %Y').strftime('%d/%m/%Y')
        except:
            submission_date = submission_date_raw

        total = linha.get('TOTAL', "0")
        tn, sinais = interpretar_total(total)

        paragrafos_relatorio = []

        respostas_vazias = []
        for col in mapa_colunas.values():
            if not linha.get(col):
                respostas_vazias.append(col)

        if respostas_vazias:
            print(f"[ERRO] Respondente '{nome}' com ID '{submission_id}' tem respostas em branco: {respostas_vazias}. Relatório não gerado.")
            continue

        paragrafos_relatorio.append(f"RESULTADO: <b>{tn}</b><br/>{sinais} de trauma psicológico.<br/><br/>")
        paragrafos_relatorio.append(f"Olá {nome}!")

        intro_query = paragrafos_df[paragrafos_df['TIPO'].str.contains(r'^INTRO\d+', flags=re.IGNORECASE, regex=True)]
        for _, row in intro_query.iterrows():
            intro = row['PARAGRAFO']
            paragrafos_relatorio.append(f"<TAB>{intro}")

        paragrafos_relatorio.append("<PAGEBREAK>")

        for _, row in paragrafos_df.iterrows():
            tipo = row['TIPO']
            if tipo.startswith("S"):
                subtitulo = row['RESPOSTA']
                paragrafos_relatorio.append(f"<b>{subtitulo}</b>")
                paragrafos_relatorio.append(row['PARAGRAFO'])

            elif tipo.startswith("P"):
                pid = tipo[1:]
                coluna = mapa_colunas.get(pid)
                if not coluna:
                    continue
                resposta = normalizar(linha.get(coluna, ""))
                if not resposta:
                    continue
                paragrafos_relatorio.append(row['PARAGRAFO'])

            elif tipo.startswith("R"):
                pid = tipo[1:]
                coluna = mapa_colunas.get(pid)
                if not coluna:
                    continue
                resposta = normalizar(linha.get(coluna, ""))
                resposta_row = row['RESPOSTA']
                if resposta == resposta_row:
                    paragrafos_relatorio.append(row['PARAGRAFO'])

        paragrafos_relatorio.append("<PAGEBREAK>")
        paragrafos_relatorio.append("<b>Conclusão</b>")
        paragrafos_conclusao = paragrafos_df[paragrafos_df['TIPO'].str.contains(r'^CON\d+', regex=True, case=False)]
        for _, row in paragrafos_conclusao.iterrows():
            if row['RESPOSTA'].strip().upper() == tn:
                paragrafos_relatorio.append("<TAB>" + row['PARAGRAFO'])

        gerar_relatorio(
            f"output/relatorios/Teste_de_Trauma_{submission_id}_{nome}.pdf",
            nome,
            sobrenome,
            email,
            total,
            paragrafos_relatorio,
            submission_id=submission_id,
            submission_date=submission_date
        )
