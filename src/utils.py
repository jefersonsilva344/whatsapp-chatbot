from datetime import datetime


def agora():

    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def remover_unicode_incompativel(texto):
    return "".join(
        c for c in texto
        if ord(c) <= 0xFFFF
    )