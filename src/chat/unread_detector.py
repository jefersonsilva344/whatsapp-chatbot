from selenium.common.exceptions import (
    StaleElementReferenceException,
)

from logger import logger

from selectors import (
    CHAT_ITEMS,
    CHAT_NAME,
    UNREAD_BADGE,
    UNREAD_COUNT,
)

from .conversation import Conversation


class UnreadDetector:

    def __init__(self, driver):

        self.driver = driver

    def listar(self):

        conversas = []

        chats = self.driver.find_elements(
            *CHAT_ITEMS
        )

        for indice, chat in enumerate(chats):

            try:

                if not chat.find_elements(
                    *UNREAD_BADGE
                ):
                    continue

                nome = chat.find_element(
                    *CHAT_NAME
                ).get_attribute("title")

                quantidade = int(
                    chat.find_element(
                        *UNREAD_COUNT
                    ).text
                )

                conversas.append(

                    Conversation(
                        indice=indice,
                        nome=nome,
                        nao_lidas=quantidade
                    )

                )

            except StaleElementReferenceException:

                continue

            except Exception as erro:

                logger.error(
                    f"Erro lendo conversa: {erro}"
                )

        return conversas