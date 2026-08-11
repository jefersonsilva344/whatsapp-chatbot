from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import WebDriverWait
from logger import logger

from selector_manager import SelectorManager
from whatsapp_selectors import MESSAGE_BOX

from utils import remover_unicode_incompativel

import time


class MessageSender:

    def __init__(self, driver):

        self.driver = driver

    def enviar(self, mensagem):

        mensagem = remover_unicode_incompativel(mensagem)


        try:

            campo = SelectorManager.encontrar(
                self.driver,
                MESSAGE_BOX
            )   
    
            campo.click()
            campo.send_keys(mensagem)
            campo.send_keys(Keys.ENTER)

        except Exception as erro:

            logger.error(
                f"Erro ao enviar mensagem:{erro}"
            )