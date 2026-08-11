import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from logger import logger
from selector_manager import SelectorManager

from whatsapp_selectors import (
    SEARCH_BOX,
    CONTACT
)


class SearchManager:

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(
            driver,
            10
        )

    def abrir(self, nome):

        try:

            pesquisa = SelectorManager.encontrar(
                self.driver,
                SEARCH_BOX
            )

            pesquisa.click()

            pesquisa.send_keys(Keys.CONTROL,"a")

            pesquisa.send_keys(Keys.DELETE)

            time.sleep(.3)

            WebDriverWait(self.driver,10).until(EC.element_to_be_clickable(CONTACT(nome)))

            conversa = self.wait.until(

                EC.element_to_be_clickable(

                    CONTACT(nome)

                )

            )

            conversa.click()

            return True

        except TimeoutException:

            return False

        except Exception as erro:

            logger.error(f"Erro ao abrir conversa:{erro}")

            return False