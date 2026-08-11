from bot import WhatsAppBot

from chat.chat_manager import ChatManager
from conversation.conversation_manager import ConversationManager
from flow.flow_manager import FlowManager
from message.message_processor import MessageProcessor
from monitor import Monitor
from responder.responder import Responder
from session.session_manager import SessionManager
from state.state_manager import StateManager

from database import (
    DatabaseConnection,
    Migration,
    MessageRepository,
    ConversationRepository
)

from logger import logger


class Container:
    """
    Composition Root da aplicação.

    Responsável por criar todas as dependências
    e conectá-las entre si.
    """

    def __init__(self):

        # Recursos principais
        self.db = None
        self.bot = None

        # Managers
        self.chat_manager = None
        self.conversation_manager = None
        self.session_manager = None
        self.state_manager = None

        # Serviços
        self.responder = None
        self.flow_manager = None
        self.message_processor = None

        # Monitor principal
        self.monitor = None

    def iniciar(self):

        logger.info(
            "Inicializando container..."
        )

        # ==================================================
        # BANCO DE DADOS
        # ==================================================

        self.db = DatabaseConnection()

        Migration(
            self.db
        ).run()

        # ==================================================
        # BOT
        # ==================================================

        self.bot = WhatsAppBot()
        self.bot.iniciar()

        # ==================================================
        # REPOSITORIES
        # ==================================================

        message_repository = MessageRepository(
            self.db
        )

        conversation_repository = (
            ConversationRepository(
                self.db
            )
        )

        # ==================================================
        # MANAGERS
        # ==================================================

        self.chat_manager = ChatManager(
            self.bot.driver
        )

        self.conversation_manager = (
            ConversationManager(
                conversation_repository
            )
        )

        self.session_manager = (
            SessionManager()
        )

        self.state_manager = (
            StateManager(
                self.session_manager
            )
        )

        # ==================================================
        # IA / RESPOSTAS
        # ==================================================

        self.responder = Responder(
            message_repository
        )

        # ==================================================
        # FLUXO
        # ==================================================

        self.flow_manager = FlowManager(
            self.session_manager,
            self.state_manager,
            self.responder
        )

        # ==================================================
        # PROCESSADOR DE MENSAGENS
        # ==================================================

        self.message_processor = (
            MessageProcessor(
                self.bot,
                message_repository,
                self.conversation_manager,
                self.flow_manager
            )
        )

        # ==================================================
        # MONITOR
        # ==================================================

        self.monitor = Monitor(
            self.bot,
            self.chat_manager,
            self.conversation_manager,
            self.message_processor
        )

        logger.info(
            "Container inicializado."
        )

        return self

    def executar(self):

        if self.monitor is None:

            raise RuntimeError(
                "Container não foi iniciado."
            )

        logger.info(
            "Iniciando monitor..."
        )

        self.monitor.iniciar()

    def fechar(self):

        logger.info(
            "Encerrando aplicação."
        )

        if self.bot:
            self.bot.fechar()

        if self.db:
            self.db.close()