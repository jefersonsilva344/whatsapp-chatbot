from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

from config import (
    PROFILE_DIR,
    WHATSAPP_URL
)

from whatsapp_selectors import SIDEBAR
from logger import logger

from bot.profile_manager import ProfileManager
from bot.search_manager import SearchManager
from bot.message_reader import MessageReader
from bot.message_sender import MessageSender


class WhatsAppBot:

    def __init__(self):
        # Objetos principais do Selenium
        self.driver = None
        self.wait = None

        # Nome da conta logada no WhatsApp
        self.meu_nome = None

        # Componentes do bot
        self.profile = None
        self.search = None
        self.reader = None
        self.sender = None

    def iniciar(self):
        """
        Inicializa o navegador, abre o WhatsApp Web e
        prepara todos os componentes do bot.
        """

        # ConfiguraÃ§Ãµes do Chrome
        options = Options()

        # MantÃ©m a sessÃ£o salva (evita ler QR Code toda vez)
        options.add_argument(
            f"--user-data-dir={PROFILE_DIR}"
        )

        # Cria o navegador
        self.driver = webdriver.Chrome(
            service=Service(
                ChromeDriverManager().install()
            ),
            options=options
        )

        # Maximiza a janela
        self.driver.maximize_window()

        # Objeto responsÃ¡vel pelas esperas explÃ­citas
        self.wait = WebDriverWait(
            self.driver,
            20
        )

        # Abre o WhatsApp Web
        self.driver.get(
            WHATSAPP_URL
        )

        logger.info(
            "Carregando WhatsApp..."
        )

        # Aguarda a barra lateral aparecer
        self.wait.until(
            EC.presence_of_element_located(
                SIDEBAR
            )
        )

        logger.info(
            "WhatsApp carregado com sucesso."
        )

        # Inicializa todos os componentes do bot
        self._inicializar_componentes()

    def _inicializar_componentes(self):
        """
        Cria todos os gerenciadores utilizados pelo bot.
        Esse mÃ©todo Ã© chamado apenas uma vez apÃ³s o
        WhatsApp estar totalmente carregado.
        """

        # Gerenciador do perfil
        self.profile = ProfileManager(
            self.driver
        )

        # Descobre o nome do usuÃ¡rio logado
        self.meu_nome = self.profile.obter_nome()

        logger.info(
            f"UsuÃ¡rio identificado: {self.meu_nome}"
        )

        # Gerenciador de busca por conversas
        self.search = SearchManager(
            self.driver
        )

        # ResponsÃ¡vel por enviar mensagens
        self.sender = MessageSender(
            self.driver
        )

        # ResponsÃ¡vel por ler mensagens
        self.reader = MessageReader(
            self.driver,
            self.meu_nome
        )

        logger.info(
            "Componentes do bot inicializados."
        )

    def abrir_conversa(self, nome):
        """
        Abre uma conversa pelo nome do contato.
        """
        return self.search.abrir(
            nome
        )

    def enviar_mensagem(self, mensagem):
        """
        Envia uma mensagem para a conversa aberta.
        """
        return self.sender.enviar(
            mensagem
        )

    def ler_ultimas_mensagens(
            self, 
            conversation_id,
            limite=15
        ):
        """
        LÃª as Ãºltimas mensagens da conversa atual.
        """
        return self.reader.ler(
            conversation_id,
            limite
        )

    def fechar(self):
        """
        Fecha o navegador.
        """
        if self.driver:

            logger.info(
                "Fechando navegador..."
            )

            self.driver.quit()