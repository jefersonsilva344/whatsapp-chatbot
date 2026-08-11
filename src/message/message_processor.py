from uuid import uuid4

from database.mapper import chat_to_message
from models import Message

from logger import logger


class MessageProcessor:
    """
    Responsável pelo ciclo de vida da mensagem:

    1 - Validar mensagem
    2 - Evitar duplicidade
    3 - Salvar histórico
    4 - Atualizar conversa
    5 - Delegar processamento do fluxo
    6 - Enviar resposta
    7 - Salvar resposta
    """

    def __init__(
        self,
        bot,
        repository,
        conversation_manager,
        flow_manager
    ):

        self.bot = bot

        self.repository = repository

        self.conversation_manager = (
            conversation_manager
        )

        self.flow_manager = flow_manager


    def processar(
        self,
        dados,
        conversation
    ):
        """
        Processa uma mensagem recebida.
        """

        # ==================================================
        # 1 - IGNORA MENSAGENS DO BOT
        # ==================================================

        if not dados.recebida:

            logger.debug(
                "Mensagem enviada pelo bot ignorada."
            )

            return


        # ==================================================
        # 2 - EVITA DUPLICIDADE
        # ==================================================

        if self.repository.exists_by_id(
            dados.id
        ):

            logger.info(
                f"Mensagem duplicada: {dados.id}"
            )

            return


        # ==================================================
        # 3 - CONVERTE PARA MODELO
        # ==================================================

        mensagem = chat_to_message(
            dados,
            conversation.id
        )


        # ==================================================
        # 4 - SALVA MENSAGEM RECEBIDA
        # ==================================================

        if not self.repository.save(
            mensagem
        ):

            logger.warning(
                "Mensagem não salva."
            )

            return


        logger.info(
            f"Nova mensagem: "
            f"{mensagem.texto}"
        )


        # ==================================================
        # 5 - ATUALIZA CONVERSA
        # ==================================================

        self.conversation_manager.atualizar(
            conversation,
            mensagem
        )


        # ==================================================
        # 6 - PROCESSA FLUXO
        # ==================================================

        resposta = (
            self.flow_manager.processar(
                conversation.id,
                mensagem.texto
            )
        )


        if not resposta:

            logger.info(
                "Fluxo não retornou resposta."
            )

            return


        # ==================================================
        # 7 - ENVIA RESPOSTA
        # ==================================================

        self._enviar_resposta(
            mensagem,
            resposta
        )


    def _enviar_resposta(
        self,
        mensagem,
        texto
    ):
        """
        Envia resposta e salva histórico.
        """

        logger.info(
            f"Respondendo: {texto}"
        )


        try:

            self.bot.enviar_mensagem(
                texto
            )


        except Exception as erro:

            logger.error(
                f"Erro enviando mensagem: {erro}"
            )

            return


        # ==================================================
        # SALVA RESPOSTA DO ASSISTENTE
        # ==================================================

        resposta = Message(

            id=str(uuid4()),

            conversation_id=(
                mensagem.conversation_id
            ),

            autor=self.bot.meu_nome,

            texto=texto,

            recebida=False,

            role="assistant"

        )


        self.repository.save(
            resposta
        )


        # ==================================================
        # MARCA ORIGINAL COMO RESPONDIDA
        # ==================================================

        self.repository.mark_answered(
            mensagem.id
        )


        logger.info(
            "Mensagem finalizada."
        )