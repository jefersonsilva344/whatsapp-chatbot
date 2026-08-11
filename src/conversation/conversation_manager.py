from uuid import uuid4

from logger import logger
from models import Conversation


class ConversationManager:

    def __init__(
        self,
        conversation_repository
    ):

        self.repository = (
            conversation_repository
        )

    def obter_conversa(
        self,
        contato
    ):

        conversation = (
            self.repository.buscar_por_contato(
                contato
            )
        )

        # ==========================================
        # CONVERSA EXISTENTE
        # ==========================================

        if conversation is not None:

            logger.info(
                f"Conversa encontrada: "
                f"{conversation.contato} | "
                f"ID: {conversation.id}"
            )

            # --------------------------------------
            # CORRIGE REGISTRO ANTIGO SEM ID
            # --------------------------------------

            if not conversation.id:

                logger.warning(
                    f"Conversa sem ID encontrada: "
                    f"{contato}"
                )

                conversation.id = str(
                    uuid4()
                )

                self.repository.atualizar_id(
                    conversation
                )

                logger.info(
                    f"ID recuperado: "
                    f"{conversation.contato} | "
                    f"ID: {conversation.id}"
                )

            return conversation

        # ==========================================
        # NOVA CONVERSA
        # ==========================================

        conversation = Conversation(

            id=str(uuid4()),

            contato=contato,

            ativa=True
        )

        self.repository.salvar(
            conversation
        )

        logger.info(
            f"Nova conversa criada: "
            f"{conversation.contato} | "
            f"ID: {conversation.id}"
        )

        return conversation

    def atualizar(
        self,
        conversa,
        mensagem
    ):

        conversa.atualizar(
            mensagem
        )

        self.repository.salvar(
            conversa
        )

        logger.info(
            f"Conversa atualizada: "
                f"{conversa.contato} | "
            f"última mensagem="
            f"{conversa.ultima_mensagem}"
        )

        return conversa