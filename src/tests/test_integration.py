import sqlite3
from types import SimpleNamespace

import pytest

from database.migrations import Migration
from database.message_repository import MessageRepository
from database.conversation_repository import ConversationRepository

from conversation.conversation_manager import ConversationManager

from message.message_processor import MessageProcessor

from flow.flow_manager import FlowManager
from session.session_manager import SessionManager
from state.state_manager import StateManager
from state.states import States

from models import Conversation


# ==========================================================
# FAKE BOT
# ==========================================================

class FakeBot:

    def __init__(self):
        self.meu_nome = "ilumina ai"
        self.mensagens_enviadas = []

    def enviar_mensagem(self, texto):
        self.mensagens_enviadas.append(texto)


# ==========================================================
# FAKE CONVERSATION MANAGER
# ==========================================================

class FakeConversationManager:

    def __init__(self):
        self.atualizacoes = []

    def atualizar(self, conversation, mensagem):

        conversation.atualizar(mensagem)

        self.atualizacoes.append(
            (
                conversation,
                mensagem
            )
        )


# ==========================================================
# FIXTURE — BANCO
# ==========================================================

@pytest.fixture
def db():

    connection = sqlite3.connect(":memory:")

    Migration(connection).run()

    yield connection

    connection.close()


# ==========================================================
# FIXTURE — CONVERSA
# ==========================================================

@pytest.fixture
def conversation(db):

    conversation = Conversation(
        id="conversation-integration-001",
        contato="Jeferson"
    )

    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO conversas (
            id,
            contato,
            ultima_mensagem,
            atualizada_em,
            ativa
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            conversation.id,
            conversation.contato,
            conversation.ultima_mensagem,
            conversation.atualizada_em,
            int(conversation.ativa)
        )
    )

    db.commit()

    return conversation


# ==========================================================
# FIXTURE — COMPONENTES
# ==========================================================

@pytest.fixture
def integration(db):

    bot = FakeBot()

    repository = MessageRepository(
        db
    )

    conversation_manager = (
        FakeConversationManager()
    )

    session_manager = (
        SessionManager()
    )

    state_manager = StateManager(
        session_manager
    )

    flow_manager = FlowManager(
        session_manager=session_manager,
        state_manager=state_manager,
        responder=None
    )

    processor = MessageProcessor(
        bot=bot,
        repository=repository,
        conversation_manager=conversation_manager,
        flow_manager=flow_manager
    )

    return {
        "processor": processor,
        "bot": bot,
        "repository": repository,
        "conversation_manager": conversation_manager,
        "session_manager": session_manager,
        "state_manager": state_manager,
    }


# ==========================================================
# DADOS DE TESTE
# ==========================================================

def criar_dados(
    message_id,
    texto,
    recebida=True
):

    return SimpleNamespace(
        id=message_id,
        autor="Jeferson",
        texto=texto,
        recebida=recebida,
        hora="15:00"
    )


# ==========================================================
# TESTE 1
# ==========================================================

def test_mensagem_recebida_e_salva_no_banco(
    integration,
    conversation
):
    """
    Deve receber uma mensagem pelo
    MessageProcessor e persistir a
    mensagem no SQLite.
    """

    processor = integration["processor"]

    repository = integration["repository"]

    dados = criar_dados(
        "integration-msg-001",
        "Olá"
    )

    processor.processar(
        dados,
        conversation
    )

    assert repository.exists_by_id(
        "integration-msg-001"
    ) is True

    cursor = repository.db.cursor()

    cursor.execute(
        """
        SELECT
            autor,
            texto,
            recebida,
            role,
            conversation_id
        FROM mensagens
        WHERE id = ?
        """,
        (
            "integration-msg-001",
        )
    )

    resultado = cursor.fetchone()

    assert resultado is not None

    assert resultado[0] == "Jeferson"

    assert resultado[1] == "Olá"

    assert resultado[2] == 1

    assert resultado[3] == "user"

    assert resultado[4] == conversation.id


# ==========================================================
# TESTE 2
# ==========================================================

def test_resposta_do_bot_e_enviada_e_salva(
    integration,
    conversation
):
    """
    Deve processar a mensagem, enviar a
    resposta pelo bot e salvar a resposta
    como assistant no banco.
    """

    processor = integration["processor"]

    bot = integration["bot"]

    repository = integration["repository"]

    dados = criar_dados(
        "integration-msg-002",
        "Olá"
    )

    processor.processar(
        dados,
        conversation
    )

    assert bot.mensagens_enviadas == [
        "Olá! Qual seu nome?"
    ]

    historico = repository.history(
        conversation.id,
        limite=10
    )

    assert len(historico) == 2

    assert historico[0] == {
        "role": "user",
        "content": "Olá"
    }

    assert historico[1] == {
        "role": "assistant",
        "content": "Olá! Qual seu nome?"
    }


# ==========================================================
# TESTE 3
# ==========================================================

def test_estado_da_sessao_acompanha_fluxo(
    integration,
    conversation
):
    """
    Deve atualizar corretamente o estado
    da sessão durante o atendimento.
    """

    processor = integration["processor"]

    state_manager = integration["state_manager"]

    session_manager = integration["session_manager"]

    # ------------------------------------------------------
    # PRIMEIRA MENSAGEM
    # ------------------------------------------------------

    processor.processar(
        criar_dados(
            "integration-state-001",
            "Olá"
        ),
        conversation
    )

    assert state_manager.obter_estado(
        conversation.id
    ) == States.AGUARDANDO_NOME

    # ------------------------------------------------------
    # NOME
    # ------------------------------------------------------

    processor.processar(
        criar_dados(
            "integration-state-002",
            "Jeferson"
        ),
        conversation
    )

    assert state_manager.obter_estado(
        conversation.id
    ) == States.AGUARDANDO_SERVICO

    # ------------------------------------------------------
    # SERVIÇO
    # ------------------------------------------------------

    processor.processar(
        criar_dados(
            "integration-state-003",
            "Instalação de LED"
        ),
        conversation
    )

    assert state_manager.obter_estado(
        conversation.id
    ) == States.ORCAMENTO

    # ------------------------------------------------------
    # DADOS DA SESSÃO
    # ------------------------------------------------------

    dados = session_manager.obter_dados(
        conversation.id
    )

    assert dados["nome"] == "Jeferson"

    assert dados["servico"] == "Instalação de LED"


# ==========================================================
# TESTE 4
# ==========================================================

def test_mensagem_duplicada_nao_gera_nova_resposta(
    integration,
    conversation
):
    """
    Uma mensagem com o mesmo ID não deve
    ser processada duas vezes.
    """

    processor = integration["processor"]

    bot = integration["bot"]

    repository = integration["repository"]

    dados = criar_dados(
        "integration-duplicate-001",
        "Olá"
    )

    # ------------------------------------------------------
    # PRIMEIRO PROCESSAMENTO
    # ------------------------------------------------------

    processor.processar(
        dados,
        conversation
    )

    # ------------------------------------------------------
    # SEGUNDO PROCESSAMENTO
    # MESMA MENSAGEM
    # ------------------------------------------------------

    processor.processar(
        dados,
        conversation
    )

    # Apenas uma resposta deve ter sido enviada.

    assert bot.mensagens_enviadas == [
        "Olá! Qual seu nome?"
    ]

    # Apenas duas mensagens devem existir:
    #
    # 1. mensagem do usuário
    # 2. resposta do bot

    historico = repository.history(
        conversation.id,
        limite=10
    )

    assert len(historico) == 2

    # A conversa também deve ter sido
    # atualizada somente uma vez.

    conversation_manager = integration[
        "conversation_manager"
    ]

    assert len(
        conversation_manager.atualizacoes
    ) == 1


# ==========================================================
# TESTE 5
# ==========================================================

def test_fluxo_completo_de_atendimento(
    integration,
    conversation
):
    """
    Deve executar um atendimento completo
    passando pelo MessageProcessor,
    FlowManager, StateManager, SessionManager,
    Bot e MessageRepository.
    """

    processor = integration["processor"]

    bot = integration["bot"]

    repository = integration["repository"]

    state_manager = integration["state_manager"]

    session_manager = integration["session_manager"]

    mensagens = [

        (
            "integration-full-001",
            "Olá"
        ),

        (
            "integration-full-002",
            "Jeferson"
        ),

        (
            "integration-full-003",
            "Instalação de LED"
        ),

        (
            "integration-full-004",
            "Pode gerar"
        ),

        (
            "integration-full-005",
            "Sim"
        )

    ]

    for message_id, texto in mensagens:

        dados = criar_dados(
            message_id,
            texto
        )

        processor.processar(
            dados,
            conversation
        )

    # ======================================================
    # RESPOSTAS ENVIADAS
    # ======================================================

    assert bot.mensagens_enviadas == [

        "Olá! Qual seu nome?",

        (
            "Prazer Jeferson! "
            "Qual serviço você precisa?"
        ),

        "Vou preparar seu orçamento.",

        (
            "Orçamento para "
            "Instalação de LED foi criado."
        ),

        "Obrigado! Atendimento finalizado."

    ]

    # ======================================================
    # ESTADO FINAL
    # ======================================================

    assert state_manager.obter_estado(
        conversation.id
    ) == States.FINALIZADO

    # ======================================================
    # DADOS DA SESSÃO
    # ======================================================

    dados_sessao = session_manager.obter_dados(
        conversation.id
    )

    assert dados_sessao == {

        "nome": "Jeferson",

        "servico": "Instalação de LED"

    }

    # ======================================================
    # HISTÓRICO
    # ======================================================

    historico = repository.history(
        conversation.id,
        limite=20
    )

    assert len(historico) == 10

    # ------------------------------------------------------
    # MENSAGENS DO USUÁRIO
    # ------------------------------------------------------

    assert historico[0] == {
        "role": "user",
        "content": "Olá"
    }

    assert historico[2] == {
        "role": "user",
        "content": "Jeferson"
    }

    assert historico[4] == {
        "role": "user",
        "content": "Instalação de LED"
    }

    assert historico[6] == {
        "role": "user",
        "content": "Pode gerar"
    }

    assert historico[8] == {
        "role": "user",
        "content": "Sim"
    }

    # ------------------------------------------------------
    # RESPOSTAS DO BOT
    # ------------------------------------------------------

    assert historico[1] == {
        "role": "assistant",
        "content": "Olá! Qual seu nome?"
    }

    assert historico[3] == {
        "role": "assistant",
        "content": (
            "Prazer Jeferson! "
            "Qual serviço você precisa?"
        )
    }

    assert historico[5] == {
        "role": "assistant",
        "content": (
            "Vou preparar seu orçamento."
        )
    }

    assert historico[7] == {
        "role": "assistant",
        "content": (
            "Orçamento para "
            "Instalação de LED foi criado."
        )
    }

    assert historico[9] == {
        "role": "assistant",
        "content": (
            "Obrigado! Atendimento finalizado."
        )
    }

    # ======================================================
    # TODAS AS MENSAGENS ORIGINAIS FORAM RESPONDIDAS
    # ======================================================

    cursor = repository.db.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM mensagens
        WHERE conversation_id = ?
        AND recebida = 1
        AND respondida = 1
        """,
        (
            conversation.id,
        )
    )

    respondidas = cursor.fetchone()[0]

    assert respondidas == 5

@pytest.fixture
def conversation_manager(db):

    repository = ConversationRepository(
        db
    )

    return ConversationManager(
        repository
    )


def test_message_processor_atualiza_conversa_real(
    db,
    integration,
    conversation_manager
    ):
    """
    Deve integrar MessageProcessor,
    ConversationManager e
    ConversationRepository.

    ```
    A mensagem recebida deve atualizar
    a última mensagem da conversa no banco.
    """

    processor = integration[
        "processor"
    ]

# ======================================================
# CRIA CONVERSA REALMENTE PELO MANAGER
# ======================================================

    conversation = (
        conversation_manager.obter_conversa(
            "Jeferson"
        )
    )


# ======================================================
# SUBSTITUI O FAKE PELO MANAGER REAL
# ======================================================

    processor.conversation_manager = (
        conversation_manager
    )


# ======================================================
# CRIA MENSAGEM
# ======================================================

    dados = SimpleNamespace(

        id="integration-conversation-001",

        autor="Jeferson",

        texto="Olá",

        recebida=True,

        hora="16:00"

    )


# ======================================================
# PROCESSA
# ======================================================

    processor.processar(

        dados,

        conversation

    )


# ======================================================
# VERIFICA BANCO
# ======================================================

    cursor = db.cursor()

    cursor.execute(
        """
        SELECT
            ultima_mensagem
        FROM conversas
        WHERE id = ?
        """,
        (
            conversation.id,
        )
    )

    resultado = cursor.fetchone()


    assert resultado is not None


    assert resultado[0] == "Olá"


# ======================================================
# VERIFICA OBJETO EM MEMÓRIA
# ======================================================

    assert (
        conversation.ultima_mensagem
        == "Olá"
    )
