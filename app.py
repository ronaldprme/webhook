from flask import Flask, request
import os
import pandas as pd
from datetime import datetime

# 👇 Importa a função do seu start.py
from start import iniciar_processo

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])

def webhook():
    data = request.form.to_dict()

    print("📬 Dados recebidos do JotForm:")
    # Adiciona data de submissão
    data["Submission Date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Reorganiza os dados na ordem desejada (ajuste conforme suas perguntas)
    colunas = ["Submission Date"] + [str(i) for i in range(1, 51)] + [
        "nome", "sobrenome", "email", "ip", "submission_id"]

    # Cria DataFrame e salva linha nova em CSV
    df = pd.DataFrame([data], columns=colunas)
    df.to_csv("respostas.csv", mode='a', header=not pd.io.common.file_exists("respostas.csv"), index=False)

    # 👇 Chama a função que está no start.py
    iniciar_processo(data)

    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
