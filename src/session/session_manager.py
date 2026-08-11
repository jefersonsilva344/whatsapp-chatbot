from datetime import datetime

from models import Session
from state.states import States

from logger import logger



class SessionManager:


    def __init__(self):

        # Sessões temporárias em memória
        #
        # {
        #   conversation_id: Session()
        # }
        #
        self.sessions = {}



    def criar(
        self,
        conversation_id
    ):

        session = Session(

            conversation_id=
                conversation_id,

            estado=
                States.INICIO,

            dados={},

            ultima_interacao=
                datetime.now()

        )


        self.sessions[
            conversation_id
        ] = session


        logger.info(
            f"Nova sessão criada: {conversation_id}"
        )


        return session



    def obter(
        self,
        conversation_id
    ):


        session = (
            self.sessions.get(
                conversation_id
            )
        )


        if session is None:
            session = self.criar(
                conversation_id
            )


        self.atualizar_interacao(
            conversation_id
        )


        return session



    def atualizar_interacao(
        self,
        conversation_id
    ):


        session = (
            self.sessions.get(
                conversation_id
            )
        )


        if session:

            session.ultima_interacao = (
                datetime.now()
            )



    def atualizar_estado(
        self,
        conversation_id,
        novo_estado
    ):


        session = self.obter(
            conversation_id
        )


        session.estado = (
            novo_estado
        )


        self.atualizar_interacao(
            conversation_id
        )


        logger.info(
            f"Sessão {conversation_id} "
            f"mudou para {novo_estado.value}"
        )


        return session



    def obter_estado(
        self,
        conversation_id
    ):


        session = self.obter(
            conversation_id
        )


        return session.estado



    def salvar_dado(
        self,
        conversation_id,
        chave,
        valor
    ):


        session = self.obter(
            conversation_id
        )


        session.dados[
            chave
        ] = valor


        self.atualizar_interacao(
            conversation_id
        )


        logger.info(
            f"Dado salvo: {chave}"
        )



    def obter_dado(
        self,
        conversation_id,
        chave
    ):


        session = self.obter(
            conversation_id
        )


        return session.dados.get(
            chave
        )



    def obter_dados(
        self,
        conversation_id
    ):


        session = self.obter(
            conversation_id
        )


        return session.dados



    def finalizar(
        self,
        conversation_id
    ):


        if conversation_id in self.sessions:


            del self.sessions[
                conversation_id
            ]


            logger.info(
                f"Sessão finalizada: {conversation_id}"
            )


    def reiniciar(
        self,
        conversation_id
    ):

        session = self.obter(
            conversation_id
        )


        session.estado = (
            States.INICIO
        )


        session.dados = {}


        session.ultima_interacao = (
            datetime.now()
        )


        logger.info(
            f"Sessão reiniciada: "
            f"{conversation_id}"
        )


        return session



    def existe(
        self,
        conversation_id
    ):


        return (
            conversation_id
            in self.sessions
        )