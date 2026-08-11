
import sqlite3

import pytest

from database.migrations import Migration
from database.message_repository import MessageRepository
from models import Message


@pytest.fixture
def db():
    """
    Cria um banco SQLite temporário em memória
    para cada teste.
    """

    connection = sqlite3.connect(":memory:")

    Migration(connection).run()

    yield connection

    connection.close()


@pytest.fixture
def repository(db):
    """
    Cria um MessageRepository utilizando
    o banco temporário.
    """

    return MessageRepository(db)


@pytest.fixture
def conversation(db):
    """
    Cria uma conversa necessária para respeitar
    a chave estrangeira de mensagens.
    """

    conversation_id = "conversation-test-001"

    db.execute(
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
            conversation_id,
            "Teste",
            None,
            None,
            1
        )
    )

    db.commit()

    return conversation_id


@pytest.fixture
def mensagem(conversation):
    """
    Cria uma mensagem de usuário para os testes.
    """

    return Message(
        id="message-test-001",
        conversation_id=conversation,
        autor="Jeferson",
        texto="Olá",
        recebida=True,
        role="user"
    )


# ==========================================================
# SAVE
# ==========================================================


def test_salvar_mensagem(
    repository,
    mensagem
):
    """
    Deve salvar uma mensagem corretamente.
    """

    resultado = repository.save(
        mensagem
    )

    assert resultado is True

    assert repository.exists_by_id(
        mensagem.id
    ) is True


def test_salvar_mensagem_duplicada(
    repository,
    mensagem
):
    """
    Não deve permitir duas mensagens
    com o mesmo ID.
    """

    primeiro = repository.save(
        mensagem
    )

    segundo = repository.save(
        mensagem
    )

    assert primeiro is True
    assert segundo is False


# ==========================================================
# EXISTS BY ID
# ==========================================================


def test_mensagem_existe(
    repository,
    mensagem
):
    """
    Deve encontrar uma mensagem salva.
    """

    repository.save(
        mensagem
    )

    assert repository.exists_by_id(
        mensagem.id
    ) is True


def test_mensagem_nao_existe(
    repository
):
    """
    Deve retornar False para uma mensagem
    que não existe.
    """

    resultado = repository.exists_by_id(
        "id-inexistente"
    )

    assert resultado is False


# ==========================================================
# MARK ANSWERED
# ==========================================================


def test_marcar_mensagem_como_respondida(
    repository,
    mensagem,
    db
):
    """
    Deve alterar respondida de 0 para 1.
    """

    repository.save(
        mensagem
    )

    repository.mark_answered(
        mensagem.id
    )

    cursor = db.cursor()

    cursor.execute(
        """
        SELECT respondida
        FROM mensagens
        WHERE id = ?
        """,
        (
            mensagem.id,
        )
    )

    resultado = cursor.fetchone()

    assert resultado[0] == 1


def test_marcar_mensagem_inexistente_como_respondida(
    repository
):
    """
    Não deve gerar erro ao tentar marcar
    uma mensagem inexistente.
    """

    repository.mark_answered(
        "id-inexistente"
    )


# ==========================================================
# HISTORY
# ==========================================================


def test_historico_retorna_mensagens(
    repository,
    conversation
):
    """
    Deve retornar o histórico da conversa
    no formato esperado pela IA.
    """

    mensagem_1 = Message(
        id="message-001",
        conversation_id=conversation,
        autor="Jeferson",
        texto="Olá",
        recebida=True,
        role="user"
    )

    mensagem_2 = Message(
        id="message-002",
        conversation_id=conversation,
        autor="Bot",
        texto="Olá! Qual seu nome?",
        recebida=False,
        role="assistant"
    )

    repository.save(
        mensagem_1
    )

    repository.save(
        mensagem_2
    )

    historico = repository.history(
        conversation,
        limite=10
    )

    assert len(historico) == 2

    assert historico[0]["role"] == "user"
    assert historico[0]["content"] == "Olá"

    assert historico[1]["role"] == "assistant"
    assert (
        historico[1]["content"]
        == "Olá! Qual seu nome?"
    )


def test_historico_respeita_limite(
    repository,
    conversation
):
    """
    Deve retornar no máximo a quantidade
    solicitada pelo parâmetro limite.
    """

    for numero in range(5):

        mensagem = Message(
            id=f"message-{numero}",
            conversation_id=conversation,
            autor="Jeferson",
            texto=f"Mensagem {numero}",
            recebida=True,
            role="user"
        )

        repository.save(
            mensagem
        )

    historico = repository.history(
        conversation,
        limite=3
    )

    assert len(historico) == 3


def test_historico_vazio(
    repository,
    conversation
):
    """
    Deve retornar lista vazia quando
    não existem mensagens.
    """

    historico = repository.history(
        conversation,
        limite=10
    )

    assert historico == []


def test_historico_isola_conversas(
    repository,
    conversation,
    db
):
    """
    Mensagens de outra conversa não devem
    aparecer no histórico atual.
    """

    outra_conversa = "conversation-test-002"

    db.execute(
        """
        INSERT INTO conversas (
            id,
            contato,
            ativa
        )

        VALUES (?, ?, ?)
        """,
        (
            outra_conversa,
            "Outro contato",
            1
        )
    )

    db.commit()

    mensagem_1 = Message(
        id="message-conversation-1",
        conversation_id=conversation,
        autor="Jeferson",
        texto="Mensagem A",
        recebida=True,
        role="user"
    )

    mensagem_2 = Message(
        id="message-conversation-2",
        conversation_id=outra_conversa,
        autor="Outra pessoa",
        texto="Mensagem B",
        recebida=True,
        role="user"
    )

    repository.save(
        mensagem_1
    )

    repository.save(
        mensagem_2
    )

    historico = repository.history(
        conversation,
        limite=10
    )

    assert len(historico) == 1

    assert (
        historico[0]["content"]
        == "Mensagem A"
    )
