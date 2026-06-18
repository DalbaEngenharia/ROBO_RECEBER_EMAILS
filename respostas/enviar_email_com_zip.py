import smtplib
import os
import zipfile
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
usuario = "robo.dalba@gmail.com"
senha = "jxrt cohu soik efhm"

# =========================
# 📦 CRIAR ZIP CORRETAMENTE
# =========================
def criar_zip(pasta_or_arquivo, destino_zip):
    """
    Cria um arquivo zip a partir de uma pasta ou arquivo.
    Mantém estrutura de diretórios.
    """

    # garante diretório do zip
    os.makedirs(os.path.dirname(destino_zip), exist_ok=True)

    with zipfile.ZipFile(destino_zip, "w", zipfile.ZIP_DEFLATED) as zipf:

        if os.path.isdir(pasta_or_arquivo):
            for raiz, dirs, arquivos in os.walk(pasta_or_arquivo):
                for arquivo in arquivos:
                    caminho_completo = os.path.join(raiz, arquivo)

                    # mantém estrutura relativa da pasta
                    arcname = os.path.relpath(caminho_completo, pasta_or_arquivo)

                    zipf.write(caminho_completo, arcname)

        else:
            zipf.write(pasta_or_arquivo, os.path.basename(pasta_or_arquivo))


# =========================
# 📧 ENVIAR EMAIL COM ZIP
# =========================
def enviar_email_com_zip(destinatario,assunto,corpo,caminho_zip,usuario,senha,smtp="smtp.gmail.com",porta=465):

    if not os.path.exists(caminho_zip):
        raise FileNotFoundError(f"Arquivo ZIP não encontrado: {caminho_zip}")

    msg = MIMEMultipart()
    msg["From"] = usuario
    msg["To"] = destinatario
    msg["Subject"] = assunto

    # corpo do email
    msg.attach(MIMEText(corpo, "plain", "utf-8"))

    # anexo ZIP
    with open(caminho_zip, "rb") as f:
        parte = MIMEBase("application", "octet-stream")
        parte.set_payload(f.read())

    encoders.encode_base64(parte)

    nome_arquivo = os.path.basename(caminho_zip)

    parte.add_header(
        "Content-Disposition",
        f"attachment; filename={nome_arquivo}"
    )

    msg.attach(parte)

    # envio SMTP seguro
    with smtplib.SMTP_SSL(smtp, porta) as server:
        server.login(usuario, senha)
        server.send_message(msg)

    print("✅ Email com ZIP enviado com sucesso!")

