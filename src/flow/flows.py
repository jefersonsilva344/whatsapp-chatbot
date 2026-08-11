from state.states import States


FLOWS = {


    States.INICIO: {

        "acao": "inicio",

        "proximo_estado":
            States.AGUARDANDO_NOME

    },


    States.AGUARDANDO_NOME: {

        "acao": "capturar_nome",

        "proximo_estado":
            States.AGUARDANDO_SERVICO

    },


    States.AGUARDANDO_SERVICO: {

        "acao": "capturar_servico",

        "proximo_estado":
            States.ORCAMENTO

    },


    States.ORCAMENTO: {

        "acao": "gerar_orcamento",

        "proximo_estado":
            States.CONFIRMACAO

    },


    States.CONFIRMACAO: {

        "acao": "confirmar",

        "proximo_estado":
            States.FINALIZADO

    }

}