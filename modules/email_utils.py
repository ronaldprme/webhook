import smtplib
from email.message import EmailMessage

# def enviar_email_com_anexo(destinatario, caminho_pdf):
#     try:
#         msg = EmailMessage()
#         msg["Subject"] = "Relatório de Testes de Trauma"
#         msg["From"] = "ronaldpr@me.com"
#         msg["To"] = destinatario
#         msg.set_content("Segue em anexo seu relatório do Teste de Trauma.")

#         with open(caminho_pdf, "rb") as f:
#             msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=caminho_pdf.split("/")[-1])

#         # Configuração do servidor SMTP da Apple (iCloud)
#         with smtplib.SMTP("smtp.mail.me.com", 587) as smtp:
#             smtp.starttls()
#             smtp.login("ronaldpr@me.com", "qrpe-wzhi-xney-bftb")
#             smtp.send_message(msg)
#     except Exception as e:
#         print(f"Erro ao enviar email para {destinatario}: {e}")
#         return False

from email.message import EmailMessage
import smtplib

def enviar_email_com_anexo(destinatario, caminho_pdf, nome):
    try:
        msg = EmailMessage()
        msg["Subject"] = "Relatório de Testes de Trauma"
        msg["From"] = "ronaldpr@me.com"
        msg["To"] = destinatario

        # Corpo de fallback (texto simples)
        msg.set_content(f"Olá {nome},\nSegue em anexo seu relatório do Teste de Trauma.")

        # Template HTML com dados variáveis
        html_content = f"""
        <html>
            <body>
                <p>Olá <strong>{nome}</strong>,</p>
                <p>Segue em anexo seu relatório do <strong>Teste de Trauma</strong>.</p>
                <br>
                <p>Atenciosamente,<br>Equipe do Projeto</p>
            </body>
        </html>
        """
        # <p>Data de envio: {data_envio}</p>
        # Adiciona o conteúdo HTML como alternativa ao texto simples
        msg.add_alternative(html_content, subtype="html")

        # Anexa o PDF
        with open(caminho_pdf, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="pdf",
                filename=caminho_pdf.split("/")[-1]
            )

        # Envia o e-mail usando o servidor SMTP da Apple (iCloud)
        with smtplib.SMTP("smtp.mail.me.com", 587) as smtp:
            smtp.starttls()
            smtp.login("ronaldpr@me.com", "qrpe-wzhi-xney-bftb")  # Use sua senha de app aqui
            smtp.send_message(msg)

        print(f"E-mail enviado com sucesso para {destinatario}!")
        return True

    except Exception as e:
        print(f"Erro ao enviar email para {destinatario}: {e}")
        return False
