import hashlib

from selenium.common.exceptions import (
    StaleElementReferenceException
)

from whatsapp_selectors import (
    MESSAGE_LIST,
    MESSAGE_TEXT
)

from models.chat_message import ChatMessage

from logger import logger


class MessageReader:


    def __init__(self, driver, meu_nome):

        self.driver = driver
        self.meu_nome = meu_nome


    def ler(self,
            conversation_id,
            limite=15
        ):

        elementos = self.driver.find_elements(
            *MESSAGE_LIST
        )

        elementos = elementos[-limite:]

        mensagens = []

        ids = set()


        for elemento in elementos:

            mensagem = self._extrair(
                elemento,
                conversation_id
                )

            if not mensagem:
                continue


            if mensagem.id in ids:
                continue


            ids.add(
                mensagem.id
            )

            mensagens.append(
                mensagem
            )


        return mensagens



    def _extrair(
            self, 
            elemento,
            conversation_id
            ):

        try:

            cabecalho = elemento.get_attribute(
                "data-pre-plain-text"
            )


            if not cabecalho:
                return None



            textos = elemento.find_elements(
                *MESSAGE_TEXT
            )


            texto = "\n".join(
                t.text.strip()
                for t in textos
                if t.text.strip()
            )


            if not texto:
                return None



            autor = (
                cabecalho
                .split("]",1)[1]
                .strip()
                .rstrip(":")
            )



            hora = (
                cabecalho
                .split("]")[0]
                .replace("[","")
                .strip()
            )


            # Verifica se a mensagem foi recebida
            recebida = self._recebida(
                autor
            )

            # Papel utilizado pela IA
            role = (
                "user"
                if self._recebida(autor)
                else "assistant"
            )

            return ChatMessage(

                id=self._gerar_id(
                    autor,
                    hora,
                    texto
                ),

                conversation_id=conversation_id,

                autor=autor,

                role=role,

                hora=hora,

                texto=texto,

                recebida=recebida
            )


        except StaleElementReferenceException:

            return None


        except Exception:

            logger.exception(
                "Erro lendo mensagem"
            )

            return None



    def _gerar_id(
        self,
        autor,
        hora,
        texto
    ):


        base = (
            f"{autor}|"
            f"{hora}|"
            f"{texto}"
        )


        return hashlib.md5(
            base.encode("utf-8")
        ).hexdigest()



    def _recebida(self, autor):

        return (
            autor.lower().strip()
            !=
            self.meu_nome.lower().strip()
        )