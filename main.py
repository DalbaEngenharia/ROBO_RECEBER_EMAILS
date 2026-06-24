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

caminho_base = r"C:\Users\DALBAPY\Desktop\Scripts"
caminho_local = r"C:\Users\gustavo.elicker\Documents\PROGRAMAS"

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
                                caminho_base+r"local_do_script_p7",
                            case "Iniciar_relatorio_K":
                                caminho_base+r"local_do_script_k",
                            case "Alterar_horario_de_acesso_ao_sistema":
                                dados = pegar_corpo_email(msg)
                                print(dados)
                                import json
                                try:
                                    caminho_script = r"C:\Users\gustavo.elicker\Documents\PROGRAMAS\Ajuste-de-horarios-base\main.py"

                                    result = subprocess.run(
                                        [sys.executable, caminho_script, json.dumps(dados)],
                                        text=True,
                                        capture_output=True
                                    )

                                    print("STDOUT:", result.stdout)
                                    print("STDERR:", result.stderr)

                                    # 🔴 ERRO REAL DO SCRIPT (não cai no except)
                                    if result.returncode != 0:
                                        erro = f"""
                                Erro ao executar script de horários

                                STDOUT:
                                {result.stdout}

                                STDERR:
                                {result.stderr}
                                """
                                        enviar_email_erro("Erro na liberação de horários", erro)

                                except Exception as e:
                                    # 🔴 ERRO DO SUBPROCESS (falha ao iniciar execução)
                                    enviar_email_erro(
                                        "Erro crítico ao chamar subprocess",
                                        str(e)
                                    )
                                    print("ERRO AO MUDAR HORARIOS:", e)
                                #def enviar_email_com_zip(destinatario,assunto,corpo,caminho_zip,usuario,senha,smtp="smtp.gmail.com",porta=465):
                                # enviar_email(remetente,"RE-"+assunto, "Segue o anexo solicitado: ",caminho_arquivo,usuario,senha )
                                # os.remove(caminho_arquivo)
                            case _:
                                destinatario = remetente
                                responder_email_erro(msg, destinatario, assunto)
                       

except KeyboardInterrupt:
    print("Encerrando...")

finally:
    mail.logout()