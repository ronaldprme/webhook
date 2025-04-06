import pandas as pd
import re
import unicodedata

def remover_acentos(texto):
    return ''.join(c for c in unicodedata.normalize('NFKD', texto) if not unicodedata.combining(c))

def normalizar(texto):
    texto = str(texto).upper().strip()
    texto = remover_acentos(texto)
    texto = texto.replace(" ", "")
    return texto

def carregar_respostas(caminho):
    df = pd.read_csv(caminho)
    colunas = df.columns.tolist()

    col_map = {}
    for col in colunas:
        col_limpa = col.upper().strip().replace(" ", "")
        col_map[col] = col_limpa

    df.rename(columns=col_map, inplace=True)

    perguntas = []
    for col in df.columns:
        if re.match(r"\d+\.", col):
            perguntas.append(col)

    return perguntas, df

def carregar_paragrafos(caminho):
    df = pd.read_csv(caminho)
    df['TIPO'] = df['TIPO'].astype(str).apply(normalizar)

    def ajustar_resposta(row):
        tipo = str(row['TIPO']).upper()
        if tipo.startswith("R"):
            return normalizar(str(row['RESPOSTA']))
        return row['RESPOSTA']  # mantém original para S, P, INTRO

    df['RESPOSTA'] = df.apply(ajustar_resposta, axis=1)
    return df


def organizar_perguntas_por_sessao(paragrafos_df):
    sessoes = {}
    perguntas_por_sessao = {}

    for _, row in paragrafos_df.iterrows():
        tipo = row['TIPO']
        if isinstance(tipo, str) and tipo.startswith("S") and tipo[1:].isdigit():
            sessoes[tipo] = []

    for _, row in paragrafos_df.iterrows():
        tipo = row['TIPO']
        if tipo.startswith("P") and tipo[1:].isdigit():
            pergunta_id = tipo[1:]
            for sessao in sessoes:
                if pergunta_id not in sessoes[sessao]:
                    sessoes[sessao].append(pergunta_id)
                    break

    return sessoes
