
import sqlite3
from datetime import datetime

import pytest

from database.migrations import Migration
from database.conversation_repository import (ConversationRepository)
from models import Conversation


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
    Cria um ConversationRepository utilizando
    o banco temporário.
    """

    return ConversationRepository(db)


@pytest.fixture
def conversa():
    """
    Cria uma conversa para os testes.
    """

    return Conversation(
        id="conversation-test-001",
        contato="Jeferson",
        ultima_mensagem="Olá",
        atualizada_em=datetime(
            2026,
            8,
            8,
            13,
            0
        ),
        ativa=True
    )


# ==========================================================
# SALVAR
# ==========================================================


def test_salvar_conversa(
    repository,
    conversa
):
    """
    Deve salvar uma conversa corretamente.
    """

    resultado = repository.salvar(
        conversa
    )

    assert resultado is conversa

    encontrada = (
        repository.buscar_por_contato(
            "Jeferson"
        )
    )

    assert encontrada is not None
    assert encontrada.id == conversa.id
    assert encontrada.contato == conversa.contato
    assert (
        encontrada.ultima_mensagem
        == conversa.ultima_mensagem
    )
    assert encontrada.ativa is True


def test_salvar_varias_conversas(
    repository
):
    """
    Deve permitir salvar conversas de
    contatos diferentes.
    """

    conversa_1 = Conversation(
        id="conversation-001",
        contato="Jeferson",
        ultima_mensagem="Olá",
        atualizada_em=datetime(
            2026,
            8,
            8,
            13,
            0
        ),
        ativa=True
    )

    conversa_2 = Conversation(
        id="conversation-002",
        contato="Maria",
        ultima_mensagem="Bom dia",
        atualizada_em=datetime(
            2026,
            8,
            8,
            13,
            1
        ),
        ativa=True
    )

    repository.salvar(
        conversa_1
    )

    repository.salvar(
        conversa_2
    )

    resultado_1 = (
        repository.buscar_por_contato(
            "Jeferson"
        )
    )

    resultado_2 = (
        repository.buscar_por_contato(
            "Maria"
        )
    )

    assert resultado_1 is not None
    assert resultado_2 is not None

    assert resultado_1.id == "conversation-001"
    assert resultado_2.id == "conversation-002"


# ==========================================================
# BUSCAR
# ==========================================================


def test_buscar_conversa_por_contato(
    repository,
    conversa
):
    """
    Deve encontrar uma conversa pelo contato.
    """

    repository.salvar(
        conversa
    )

    resultado = (
        repository.buscar_por_contato(
            "Jeferson"
        )
    )

    assert resultado is not None
    assert resultado.contato == "Jeferson"


def test_buscar_conversa_inexistente(
    repository
):
    """
    Deve retornar None quando o contato
    não existe.
    """

    resultado = (
        repository.buscar_por_contato(
            "Contato inexistente"
        )
    )

    assert resultado is None


def test_buscar_contato_exato(
    repository,
    conversa
):
    """
    A busca deve respeitar o contato informado.
    """

    repository.salvar(
        conversa
    )

    resultado = (
        repository.buscar_por_contato(
            "Jef"
        )
    )

    assert resultado is None


# ==========================================================
# ATUALIZAÇÃO / UPSERT
# ==========================================================


def test_atualizar_conversa_existente(
    repository,
    conversa
):
    """
    Deve atualizar os dados quando a conversa
    com o mesmo contato já existe.
    """

    repository.salvar(
        conversa
    )

    conversa_atualizada = Conversation(
        id="novo-id-que-nao-deve-substituir",
        contato="Jeferson",
        ultima_mensagem="Preciso de um orçamento",
        atualizada_em=datetime(
            2026,
            8,
            8,
            13,
            10
        ),
        ativa=True
    )

    repository.salvar(
        conversa_atualizada
    )

    resultado = (
        repository.buscar_por_contato(
            "Jeferson"
        )
    )

    assert resultado is not None

    assert resultado.contato == "Jeferson"

    assert (
        resultado.ultima_mensagem
        == "Preciso de um orçamento"
    )

    assert (
        resultado.atualizada_em
        == datetime(
            2026,
            8,
            8,
            13,
            10
        )
    )

    assert resultado.ativa is True

    # O seu SQL atual faz UPDATE somente dos campos
    # definidos no ON CONFLICT. Portanto, o ID original
    # deve continuar sendo o mesmo.
    assert resultado.id == conversa.id


def test_atualizar_conversa_inativa(
    repository
):
    """
    Deve permitir alterar uma conversa para inativa.
    """

    conversa = Conversation(
        id="conversation-003",
        contato="Jeferson",
        ultima_mensagem="Finalizado",
        atualizada_em=datetime(
            2026,
            8,
            8,
            13,
            0
        ),
        ativa=True
    )

    repository.salvar(
        conversa
    )

    conversa_inativa = Conversation(
        id=conversa.id,
        contato="Jeferson",
        ultima_mensagem="Atendimento encerrado",
        atualizada_em=datetime(
            2026,
            8,
            8,
            13,
            10
        ),
        ativa=False
    )

    repository.salvar(
        conversa_inativa
    )

    resultado = (
        repository.buscar_por_contato(
            "Jeferson"
        )
    )

    assert resultado is not None
    assert resultado.ativa is False
    assert (
        resultado.ultima_mensagem
        == "Atendimento encerrado"
    )

    assert (
        resultado.atualizada_em
        == datetime(
            2026,
            8,
            8,
            13,
            10
        )
    )


# ==========================================================
# DADOS OPCIONAIS
# ==========================================================


def test_salvar_conversa_sem_ultima_mensagem(
    repository
):
    """
    Deve permitir uma conversa sem
    última mensagem.
    """

    conversa = Conversation(
        id="conversation-004",
        contato="Jeferson",
        ultima_mensagem=None,
        atualizada_em=None,
        ativa=True
    )

    repository.salvar(
        conversa
    )

    resultado = (
        repository.buscar_por_contato(
            "Jeferson"
        )
    )

    assert resultado is not None
    assert resultado.ultima_mensagem is None
    assert resultado.atualizada_em is None


def test_conversa_ativa_por_padrao(
    repository
):
    """
    O modelo Conversation deve iniciar
    como uma conversa ativa.
    """

    conversa = Conversation(
        id="conversation-005",
        contato="Jeferson"
    )

    assert conversa.ativa is True

    repository.salvar(
        conversa
    )

    resultado = (
        repository.buscar_por_contato(
            "Jeferson"
        )
    )

    assert resultado.ativa is True

