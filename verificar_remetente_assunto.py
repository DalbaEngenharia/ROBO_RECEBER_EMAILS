import json

def verificar_remtente_assunto(remetente_bruto, assunto): 
    remetente = remetente_bruto.split("<")[1].split(">")[0]
    with open("lista_remetente_assunto.json", "r",encoding="utf-8") as arquivo: 
        dados = json.load(arquivo)
    print(dados)
    if remetente in dados[assunto]:
        return True
    return False
    