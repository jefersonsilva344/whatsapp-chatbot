from flow.flows import FLOWS

from state.states import States

from logger import logger



class FlowManager:


    def __init__(
        self,
        session_manager,
        state_manager,
        responder
    ):

        self.session_manager = (
            session_manager
        )

        self.state_manager = (
            state_manager
        )

        self.responder = responder



    def processar(
        self,
        conversation_id,
        mensagem
    ):


        estado = (
            self.state_manager.obter_estado(
                conversation_id
            )
        )

        # ==========================================
        # SESSÃO FINALIZADA
        # ==========================================
        
        if estado == States.FINALIZADO:

            logger.info(
                f"Sessão finalizada. "
                f"Iniciando novo atendimento: "
                f"{conversation_id}"
            )

            self.state_manager.reiniciar(
                conversation_id,
            )

            estado = States.INICIO

        # ==========================================
        # LOCALIZA FLUXO
        # ==========================================

        fluxo = (
            FLOWS.get(
                estado
            )
        )


        if not fluxo:

            logger.warning(
                f"Fluxo não encontrado: {estado}"
            )

            return None


        # ==========================================
        # EXECUTA AÇÃO
        # ==========================================

        acao = fluxo["acao"]



        resposta = (
            self._executar_acao(
                acao,
                conversation_id,
                mensagem
            )
        )


        # ==========================================
        # ALTERA ESTADO
        # ==========================================

        self.state_manager.mudar_estado(

            conversation_id,

            fluxo["proximo_estado"]

        )


        return resposta





    def _executar_acao(
        self,
        acao,
        conversation_id,
        mensagem
    ):


        if acao == "inicio":

            return (
                "Olá! Qual seu nome?"
            )



        if acao == "capturar_nome":

            self.session_manager.salvar_dado(

                conversation_id,

                "nome",

                mensagem

            )


            return (
                f"Prazer {mensagem}! "
                "Qual serviço você precisa?"
            )



        if acao == "capturar_servico":


            self.session_manager.salvar_dado(

                conversation_id,

                "servico",

                mensagem

            )


            return (
                "Vou preparar seu orçamento."
            )



        if acao == "gerar_orcamento":

            dados = (
                self.session_manager
                .obter(conversation_id)
                .dados
            )


            return (
                f"Orçamento para "
                f"{dados.get('servico')} "
                "foi criado."
            )



        if acao == "confirmar":

            return (
                "Obrigado! Atendimento finalizado."
            )


        return None