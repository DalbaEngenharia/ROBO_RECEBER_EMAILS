import smtplib
import os
import zipfile
import mimetypes

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
usuario = "robo.dalba@gmail.com"
senha = "jxrt cohu soik efhm"

# =========================
# 📦 CRIAR ZIP
# =========================
def criar_zip(pasta_ou_arquivo, destino_zip):
    """
    Cria um arquivo ZIP a partir de uma pasta ou arquivo.
    Mantém estrutura de diretórios.
    """

    # garante diretório do zip
    pasta_destino = os.path.dirname(destino_zip)
    if pasta_destino:
        os.makedirs(pasta_destino, exist_ok=True)

    with zipfile.ZipFile(destino_zip, "w", zipfile.ZIP_DEFLATED) as zipf:

        if os.path.isdir(pasta_ou_arquivo):

            for raiz, dirs, arquivos in os.walk(pasta_ou_arquivo):
                for arquivo in arquivos:
                    caminho_completo = os.path.join(raiz, arquivo)

                    # mantém estrutura relativa
                    arcname = os.path.relpath(caminho_completo, pasta_ou_arquivo)

                    zipf.write(caminho_completo, arcname)

        else:
            zipf.write(pasta_ou_arquivo, os.path.basename(pasta_ou_arquivo))


# =========================
# 📎 ANEXAR ARQUIVO GENÉRICO
# =========================
def anexar_arquivo(msg, caminho_arquivo):

    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")

    tipo_mime, _ = mimetypes.guess_type(caminho_arquivo)

    if tipo_mime is None:
        tipo_mime = "application/octet-stream"

    main_type, sub_type = tipo_mime.split("/")

    with open(caminho_arquivo, "rb") as f:
        parte = MIMEBase(main_type, sub_type)
        parte.set_payload(f.read())

    encoders.encode_base64(parte)

    nome_arquivo = os.path.basename(caminho_arquivo)

    parte.add_header(
        "Content-Disposition",
        f"attachment; filename={nome_arquivo}"
    )

    msg.attach(parte)


# =========================
# 📧 ENVIAR EMAIL COM ANEXOS
# =========================
def enviar_email(destinatario,
                 assunto,
                 corpo,
                 arquivos,
                 usuario,
                 senha,
                 smtp="smtp.gmail.com",
                 porta=465):

    msg = MIMEMultipart()
    msg["From"] = usuario
    msg["To"] = destinatario
    msg["Subject"] = assunto

    # corpo do e-mail
    msg.attach(MIMEText(corpo, "plain", "utf-8"))

    # aceita 1 ou vários arquivos
    if isinstance(arquivos, str):
        arquivos = [arquivos]

    for arquivo in arquivos:
        anexar_arquivo(msg, arquivo)

    # envio SMTP seguro
    with smtplib.SMTP_SSL(smtp, porta) as server:
        server.login(usuario, senha)
        server.send_message(msg)

    print("✅ Email enviado com sucesso!")