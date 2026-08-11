from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selector_manager import SelectorManager

from whatsapp_selectors import (
    PROFILE_BUTTON,
    PROFILE_NAME,
    PROFILE_CLOSE
)

from logger import logger


class ProfileManager:

    def __init__(self, driver):

        self.driver = driver

    def obter_nome(self):

        logger.info(
            "Abrindo perfil..."
        )

        # Abre o perfil
        botao = SelectorManager.encontrar(
            self.driver,
            PROFILE_BUTTON
        )

        botao.click()

        # ObtÃ©m o nome do usuÃ¡rio
        nome = SelectorManager.encontrar(
            self.driver,
            PROFILE_NAME,
            clicavel=False
        ).text.strip()

        # Fecha o perfil
        fechar = SelectorManager.encontrar(
            self.driver,
            PROFILE_CLOSE
        )

        fechar.click()

        # Aguarda o painel desaparecer
        WebDriverWait(
            self.driver,
            5
        ).until(

            EC.invisibility_of_element_located(
                PROFILE_CLOSE[0]
            )

        )

        logger.info(
            "Perfil fechado."
        )

        return nome