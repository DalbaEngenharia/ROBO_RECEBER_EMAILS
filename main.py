import imaplib
import email
from email.header import decode_header
import time
from respostas.enviar_email_com_zip import *
from respostas.resposta_erro import *
import subprocess
import sys
from enviar_email_erro import enviar_email_erro
from usuario import *
from enviar_email_sucesso import *
import os

mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(usuario, senha)
print("=====Servidor Iniciado=====")
def pegar_corpo_email(msg):
    corpo = ""

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if content_type in ["text/plain", "text/html"] and "attachment" not in content_disposition:
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or "utf-8"
                    corpo = payload.decode(charset, errors="replace")
                    break
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or "utf-8"
            corpo = payload.decode(charset, errors="replace")

    return corpo.strip()


try:
    while True:
        mail.select("INBOX")

        # Buscar apenas e-mails não lidos
        status, mensagens = mail.search(None, "UNSEEN")

        if status == "OK":
            ids = mensagens[0].split()

            for email_id in ids:
                status, dados = mail.fetch(email_id, "(RFC822)")

                for resposta in dados:
                    if isinstance(resposta, tuple):
                        msg = email.message_from_bytes(resposta[1])

                        assunto, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(assunto, bytes):
                            assunto = assunto.decode(
                                encoding or "utf-8",
                                errors="ignore"
                            )

                        remetente = msg.get("From")

                        print("=" * 50)
                        print("Novo e-mail recebido")
                        print("De:", remetente)
                        print("Assunto:", assunto)

                        match assunto: 
                            case "Iniciar_Relatorio_P7":
                                pass
                            case "Iniciar_relatorio_K":
                                pass
                           
                            case "Alterar_horario_de_acesso_ao_sistema":
                                import logging

                                # logging.basicConfig(
                                #     filename="automacao.log",
                                #     level=logging.DEBUG,
                                #     format="%(asctime)s %(levelname)s %(message)s",
                                #     encoding="utf-8"
                                #     )
                                os.system("taskkill /f /im chrome.exe")
                                os.system("taskkill /f /im chromedriver.exe")
                                dados = pegar_corpo_email(msg)

                                print("Dados recebidos:")
                                print(dados)
                                try:

                                    caminho_script = r"C:\Users\DALBAPY\Desktop\Scripts\Ajuste-de-horarios-base-requisicao\main.py"

                                 #   logging.info(f"Executando: {caminho_script}")

                                    result = subprocess.run(
                                        [sys.executable, caminho_script, dados],
                                        text=True,
                                        capture_output=True
                                    )
                                    if result.returncode == 0:
                                        enviar_email_sucesso(
                                            "Horários alterados com sucesso",
                                            f"Os horários do usuario foram alterados com sucesso.\n\nDados:\n{dados}"
                                        )
                                    if result.returncode != 0:
                                        enviar_email_erro("Erro lançamento de horarios",f"Houve um erro ao alterar os horarios {dados}")

                                except Exception as e:
                                    logging.exception(e)
                                    enviar_email_erro(
                                        "Erro lançamento de horarios",
                                        f"Houve um erro ao alterar os horarios\n\n{dados}\n\nErro: {e}"
    )
                            case _:
                                destinatario = remetente
                                responder_email_erro(msg, destinatario, assunto)
                       

except KeyboardInterrupt:
    print("Encerrando...")

finally:
    mail.logout()