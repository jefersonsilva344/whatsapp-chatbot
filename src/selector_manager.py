from dataclasses import dataclass

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@dataclass
class ElementoEcontrado:
    """
    Encapsula o elemento encontrado e o seletor utilizado.

    Graças ao __getattr__, ele se comporta como um WebElement.
    """

    elemento: object
    seletor: tuple
    indice: int

    def __getattr__(self, atributo):
        return getattr(self.elemento, atributo)


class SelectorManager:

    @staticmethod
    def encontrar(
        driver,
        seletores,
        timeout=5,
        clicavel=True
    ):

        ultimo_erro = None

        for indice, seletor in enumerate(seletores):

            try:

                if clicavel:

                    elemento = WebDriverWait(
                        driver,
                        timeout
                    ).until(
                        EC.element_to_be_clickable(
                            seletor
                        )
                    )

                else:

                    elemento = WebDriverWait(
                        driver,
                        timeout
                    ).until(
                        EC.presence_of_element_located(
                            seletor
                        )
                    )

                return ElementoEcontrado(
                    elemento=elemento,
                    seletor=seletor,
                    indice=indice
                )

            except TimeoutException as erro:

                ultimo_erro = erro

                continue

        raise TimeoutException(
            f"Nenhum seletor funcionou:\n{seletores}"
        ) from ultimo_erro