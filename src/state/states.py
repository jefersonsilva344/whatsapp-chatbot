from enum import Enum



class States(Enum):

    INICIO = "inicio"

    AGUARDANDO_NOME = (
        "aguardando_nome"
    )

    AGUARDANDO_SERVICO = (
        "aguardando_servico"
    )

    ORCAMENTO = (
        "orcamento"
    )

    CONFIRMACAO = (
        "confirmacao"
    )

    FINALIZADO = (
        "finalizado"
    )