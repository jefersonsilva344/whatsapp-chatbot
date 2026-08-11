import time

from logger import logger


class Monitor:
    """
    Monitora o WhatsApp e encaminha mensagens
    recebidas para o MessageProcessor.
    """


    def __init__(
        self,
        bot,
        chat_manager,
        conversation_manager,
        message_processor
    ):
        """
        Recebe as dependências necessárias
        para executar o monitoramento.

        bot:
            Controla o WhatsApp via Selenium.

        chat_manager:
            Gerencia chats e conversas
            dentro do WhatsApp.

        conversation_manager:
            Gerencia as conversas
            persistidas no banco.

        message_processor:
            Processa a mensagem recebida
            e decide a ação.
        """


        self.bot = bot

        self.chat_manager = (
            chat_manager
        )

        self.conversation_manager = (
            conversation_manager
        )

        self.message_processor = (
            message_processor
        )



    def iniciar(self):
        """
        Inicia o loop principal do monitor.

        O bot fica executando continuamente,
        verificando novas mensagens.
        """


        logger.info(
            "Monitor iniciado."
        )


        while True:

            try:

                # Executa uma verificação
                # de novas mensagens
                self.monitorar()

            except Exception as erro:

                logger.exception(
                    f"Erro no monitor:{erro}"
                )


            # Aguarda 1 segundo antes
            # de verificar novamente
            time.sleep(1)




    def monitorar(self):
        """
        Executa uma varredura no WhatsApp.

        Fluxo:

        WhatsApp
             |
             ↓
        ChatManager
             |
             ↓
        ConversationManager
             |
             ↓
        MessageProcessor
        """


        # Busca conversas que possuem
        # mensagens ainda não lidas
        conversas = (
            self.chat_manager
            .listar_nao_lidas()
        )



        # Percorre cada conversa encontrada
        for chat in conversas:


            # Abre a conversa no WhatsApp
            #
            # Caso ocorra erro,
            # pula para a próxima conversa
            if not self.chat_manager.abrir(
                chat
            ):
                continue



            # Busca ou cria a conversa
            # correspondente no banco SQLite.
            #
            # Importante:
            # chat.nome é uma string.
            # O banco não recebe o objeto inteiro.
            conversation = (
                self.conversation_manager
                .obter_conversa(
                    chat.nome
                )
            )

            if not conversation:
                logger.error(
                    f"Não foi possível obter conversa:{chat.nome}"
                )
                continue

            if not conversation.id:
                logger.error(
                    f"Conversa sem ID:{chat.nome}"
                )
                continue

            logger.debug(
                f"Conversation ID:{conversation.id}"
            )



            # Recupera as últimas mensagens
            # disponíveis na conversa aberta
            mensagens = (
                self.bot
                .ler_ultimas_mensagens(
                    conversation.id
                )
            )



            # Envia cada mensagem encontrada
            # para o processador principal
            for mensagem in mensagens:


                self.message_processor.processar(
                    mensagem,
                    conversation
                )