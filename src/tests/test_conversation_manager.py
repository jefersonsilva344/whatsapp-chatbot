from datetime import datetime
from types import SimpleNamespace

from conversation.conversation_manager import (
    ConversationManager
)
from models import Conversation


# ==========================================================
# FAKE REPOSITORY
# ==========================================================

class FakeConversationRepository:

    def __init__(self):

        self.conversas = {}

        self.atualizacoes_id = []

        self.salvamentos = []


    def buscar_por_contato(
        self,
        contato
    ):

        return self.conversas.get(
            contato
        )


    def salvar(
        self,
        conversa
    ):

        self.conversas[
            conversa.contato
        ] = conversa

        self.salvamentos.append(
            conversa
        )

        return conversa


    def atualizar_id(
        self,
        conversa
    ):

        self.atualizacoes_id.append(
            conversa
        )

        self.conversas[
            conversa.contato
        ] = conversa


# ==========================================================
# FIXTURE MANUAL
# ==========================================================

def criar_manager():

    repository = (
        FakeConversationRepository()
    )

    manager = ConversationManager(
        repository
    )

    return (
        manager,
        repository
    )


# ==========================================================
# NOVA CONVERSA
# ==========================================================

def test_cria_nova_conversa():

    manager, repository = (
        criar_manager()
    )


    conversa = (
        manager.obter_conversa(
            "Jeferson"
        )
    )


    assert conversa is not None

    assert conversa.contato == (
        "Jeferson"
    )

    assert conversa.id is not None

    assert conversa.id != ""

    assert conversa.ativa is True


    assert (
        repository.conversas["Jeferson"]
        is conversa
    )


# ==========================================================
# CONVERSA EXISTENTE
# ==========================================================

def test_obtem_conversa_existente():

    manager, repository = (
        criar_manager()
    )


    conversa_original = Conversation(

        id="conversation-001",

        contato="Jeferson",

        ativa=True

    )


    repository.conversas[
        "Jeferson"
    ] = conversa_original


    conversa = (
        manager.obter_conversa(
            "Jeferson"
        )
    )


    assert conversa is conversa_original

    assert conversa.id == (
        "conversation-001"
    )


# ==========================================================
# MESMO CONTATO
# ==========================================================

def test_mesmo_contato_retorna_mesma_conversa():

    manager, repository = (
        criar_manager()
    )


    primeira = (
        manager.obter_conversa(
            "Jeferson"
        )
    )


    segunda = (
        manager.obter_conversa(
            "Jeferson"
        )
    )


    assert primeira.id == segunda.id

    assert primeira is segunda

    assert len(
        repository.salvamentos
    ) == 1


# ==========================================================
# NOVO CONTATO CRIA NOVA CONVERSA
# ==========================================================

def test_contatos_diferentes_criam_conversas_diferentes():

    manager, repository = (
        criar_manager()
    )


    conversa_1 = (
        manager.obter_conversa(
            "Jeferson"
        )
    )


    conversa_2 = (
        manager.obter_conversa(
            "Maria"
        )
    )


    assert conversa_1.id != (
        conversa_2.id
    )

    assert conversa_1.contato == (
        "Jeferson"
    )

    assert conversa_2.contato == (
        "Maria"
    )

    assert len(
        repository.conversas
    ) == 2


# ==========================================================
# ATUALIZA ÚLTIMA MENSAGEM
# ==========================================================

def test_atualiza_ultima_mensagem():

    manager, repository = (
        criar_manager()
    )


    conversa = (
        manager.obter_conversa(
            "Jeferson"
        )
    )


    mensagem = SimpleNamespace(

        texto="Olá, preciso de orçamento."

    )


    manager.atualizar(
        conversa,
        mensagem
    )


    assert conversa.ultima_mensagem == (
        "Olá, preciso de orçamento."
    )


# ==========================================================
# ATUALIZA DATA DA CONVERSA
# ==========================================================

def test_atualiza_data_da_conversa():

    manager, repository = (
        criar_manager()
    )


    conversa = (
        manager.obter_conversa(
            "Jeferson"
        )
    )


    assert conversa.atualizada_em is None


    mensagem = SimpleNamespace(

        texto="Bom dia"

    )


    manager.atualizar(
        conversa,
        mensagem
    )


    assert isinstance(
        conversa.atualizada_em,
        datetime
    )


# ==========================================================
# SALVA CONVERSA ATUALIZADA
# ==========================================================

def test_atualiza_conversa_no_repositorio():

    manager, repository = (
        criar_manager()
    )


    conversa = (
        manager.obter_conversa(
            "Jeferson"
        )
    )


    quantidade_salvamentos_antes = (
        len(repository.salvamentos)
    )


    mensagem = SimpleNamespace(

        texto="Quero instalar LED."

    )


    resultado = manager.atualizar(
        conversa,
        mensagem
    )


    assert resultado is conversa


    assert len(
        repository.salvamentos
    ) == (
        quantidade_salvamentos_antes + 1
    )


    assert (
        repository.salvamentos[-1]
        is conversa
    )


# ==========================================================
# RECUPERA CONVERSA SEM ID
# ==========================================================

def test_recupera_conversa_sem_id():

    manager, repository = (
        criar_manager()
    )


    conversa = Conversation(

        id="",

        contato="Jeferson",

        ativa=True

    )


    repository.conversas[
        "Jeferson"
    ] = conversa


    resultado = (
        manager.obter_conversa(
            "Jeferson"
        )
    )


    assert resultado is conversa

    assert resultado.id is not None

    assert resultado.id != ""

    assert len(
        repository.atualizacoes_id
    ) == 1


    assert (
        repository.atualizacoes_id[0]
        is conversa
    )