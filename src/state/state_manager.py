from state.states import States

from logger import logger


class StateManager:


    def __init__(
        self,
        session_manager
    ):

        self.session_manager = (
            session_manager
        )


        self.transitions = {

            States.INICIO: [

                States.AGUARDANDO_NOME

            ],


            States.AGUARDANDO_NOME: [

                States.AGUARDANDO_SERVICO

            ],


            States.AGUARDANDO_SERVICO: [

                States.ORCAMENTO

            ],


            States.ORCAMENTO: [

                States.CONFIRMACAO

            ],


            States.CONFIRMACAO: [

                States.FINALIZADO

            ]

        }



    def obter_estado(
        self,
        conversation_id
    ):

        session = (
            self.session_manager.obter(
                conversation_id
            )
        )

        return session.estado



    def mudar_estado(
        self,
        conversation_id,
        novo_estado
    ):

        estado_atual = (
            self.obter_estado(
                conversation_id
            )
        )


        if not self.pode_transicionar(
            estado_atual,
            novo_estado
        ):

            logger.warning(

                f"Transição inválida "
                f"{estado_atual} -> {novo_estado}"

            )

            return False


        self.session_manager.atualizar_estado(

            conversation_id,

            novo_estado

        )


        logger.info(

            f"Estado alterado "
            f"{estado_atual} -> {novo_estado}"

        )


        return True



    def pode_transicionar(
        self,
        atual,
        novo
    ):

        estados_permitidos = (

            self.transitions.get(
                atual,
                []
            )

        )

        return novo in estados_permitidos



    def reiniciar(
        self,
        conversation_id
    ):

        session = (
            self.session_manager.reiniciar(
                conversation_id
            )
        )


        logger.info(
            f"Estado reiniciado: "
            f"{conversation_id} -> "
            f"{States.INICIO}"
        )


        return session