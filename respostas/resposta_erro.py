import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def responder_email_erro(msg_original, destinatario, assunto_original):
    remetente = "robo.dalba@gmail.com"
    senha =  "jxrt cohu soik efhm"

    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = "Re: " + assunto_original

    # 🔥 ESSENCIAL para virar resposta real
    if msg_original.get("Message-ID"):
        msg["In-Reply-To"] = msg_original["Message-ID"]
        msg["References"] = msg_original["Message-ID"]

    corpo = f"""
Olá,

Não foi possível processar seu e-mail.

Assunto recebido: {assunto_original}

Por favor, envie um assunto válido.

Verifique se a ortografia está correta.  
O assunto deve ser escrito exatamente como foi proposto.

Atenciosamente,  
Robô Dalba
"""

    msg.attach(MIMEText(corpo, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(remetente, senha)
        server.send_message(msg)
        server.quit()

        print("Resposta enviada como reply real!")

    except Exception as e:
        print("Erro ao enviar resposta:", e)