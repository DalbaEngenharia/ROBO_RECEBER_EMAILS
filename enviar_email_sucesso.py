import smtplib
from email.mime.text import MIMEText

def enviar_email_sucesso(assunto, corpo):
    if isinstance(corpo, list):
        corpo = "\n".join(map(str, corpo))
    else:
        corpo = str(corpo)

    remetente = "robo.dalba@gmail.com"
    senha = "jxrt cohu soik efhm"
    destinatario = ["gustavo.elicker@dalba.com.br","marlon.prates@dalba.com.br"]
    # destinatario = ["gustavo.elicker@dalba.com.br"]
    for x in destinatario: 
        msg = MIMEText(corpo, "plain", "utf-8")
        msg["Subject"] = assunto
        msg["From"] = remetente
        msg["To"] = x

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(remetente, senha)
            server.send_message(msg)