from logger import logger

from selector_manager import SelectorManager

from selectors import (
    CHAT_ITEMS,
    CHAT_CONTAINER,
    MESSAGE_BOX,
)

from .unread_detector import UnreadDetector


class ChatManager:

    def __init__(self, driver):

        self.driver = driver

        self.detector = UnreadDetector(driver)

    def listar_nao_lidas(self):

        return self.detector.listar()

    def abrir(self, conversa):

        try:

            chats = self.driver.find_elements(
                *CHAT_ITEMS
            )

            chat = chats[
                conversa.indice
            ]

            container = chat.find_element(
                *CHAT_CONTAINER
            )

            self.driver.execute_script(
                """
                arguments[0].scrollIntoView({
                    block:'center'
                });
                """,
                container
            )

            container.click()

            SelectorManager.encontrar(
                self.driver,
                MESSAGE_BOX
            )

            logger.info(
                f"Conversa aberta: {conversa.nome}"
            )

            return True

        except Exception as erro:

            logger.error(
                f"Erro abrindo conversa: {erro}"
            )

            return False