import imaplib
import email
from email.header import decode_header
import time
# from relatorio_p7 import Iniciar_Relatorio_P7
# from resposta_erro import responder_email
import subprocess
from lista_de_scripts import caminho_de_scripts
from usuario import *


mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(usuario, senha)

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
                        if assunto == "relatorio_teste": 
                            from respostas.enviar_email_com_zip import enviar_email_com_zip
                            enviar_email_com_zip(remetente,"RE-"+assunto,"Segue o arquivo compactado em anexo.", r"C:\Users\gustavo.elicker\Desktop\teste.zip",usuario,senha )
                        elif assunto in caminho_de_scripts:
                            subprocess.Popen([sys.executable, scripts[acao]])
                            #responde ao email com erro 
                        else:
                            destinatario = remetente
                            print("TESTE==========")
                            print(msg)
                            print("TESTE==========")
                            responder_email_erro(msg, destinatario, assunto)
                       

except KeyboardInterrupt:
    print("Encerrando...")

finally:
    mail.logout()