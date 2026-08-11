from datetime import datetime

from session.session_manager import SessionManager
from state.states import States


def test_criar_sessao():

    session_manager = SessionManager()

    conversation_id = "teste-123"

    session = session_manager.criar(
        conversation_id
    )

    assert session is not None

    assert (
        session.conversation_id
        == conversation_id
    )

    assert (
        session.estado
        == States.INICIO
    )

    assert session.dados == {}

    assert (
        session.ultima_interacao
        is not None
    )


def test_criar_sessao_fica_disponivel():

    session_manager = SessionManager()

    conversation_id = "teste-123"

    session_manager.criar(
        conversation_id
    )

    assert (
        session_manager.existe(
            conversation_id
        )
        is True
    )


def test_obter_sessao_existente():

    session_manager = SessionManager()

    conversation_id = "teste-123"

    criada = session_manager.criar(
        conversation_id
    )

    obtida = session_manager.obter(
        conversation_id
    )

    assert obtida is criada


def test_obter_cria_sessao_se_nao_existir():

    session_manager = SessionManager()

    conversation_id = "teste-123"

    assert (
        session_manager.existe(
            conversation_id
        )
        is False
    )

    session = session_manager.obter(
        conversation_id
    )

    assert session is not None

    assert (
        session.conversation_id
        == conversation_id
    )

    assert (
        session.estado
        == States.INICIO
    )

    assert (
        session_manager.existe(
            conversation_id
        )
        is True
    )


def test_atualizar_interacao():

    session_manager = SessionManager()

    conversation_id = "teste-123"

    session = session_manager.criar(
        conversation_id
    )

    primeira_interacao = (
        session.ultima_interacao
    )

    session_manager.atualizar_interacao(
        conversation_id
    )

    assert (
        session.ultima_interacao
        >= primeira_interacao
    )


def test_atualizar_estado():

    session_manager = SessionManager()

    conversation_id = "teste-123"

    session_manager.criar(
        conversation_id
    )

    session = (
        session_manager.atualizar_estado(
            conversation_id,
            States.AGUARDANDO_NOME
        )
    )

    assert (
        session.estado
        == States.AGUARDANDO_NOME
    )

    assert (
        session_manager.obter_estado(
            conversation_id
        )
        == States.AGUARDANDO_NOME
    )


def test_obter_estado():

    session_manager = SessionManager()

    conversation_id = "teste-123"

    session_manager.criar(
        conversation_id
    )

    session_manager.atualizar_estado(
        conversation_id,
        States.ORCAMENTO
    )

    estado = (
        session_manager.obter_estado(
            conversation_id
        )
    )

    assert estado == States.ORCAMENTO


def test_salvar_dado():

    session_manager = SessionManager()

    conversation_id = "teste-123"

    session_manager.criar(
        conversation_id
    )

    session_manager.salvar_dado(
        conversation_id,
        "nome",
        "Jeferson"
    )

    assert (
        session_manager.obter_dado(
            conversation_id,
            "nome"
        )
        == "Jeferson"
    )


def test_salvar_varios_dados():

    session_manager = SessionManager()

    conversation_id = "teste-123"

    session_manager.criar(
        conversation_id
    )

    session_manager.salvar_dado(
        conversation_id,
        "nome",
        "Jeferson"
    )

    session_manager.salvar_dado(
        conversation_id,
        "servico",
        "Instalação elétrica"
    )

    dados = (
        session_manager.obter_dados(
            conversation_id
        )
    )

    assert dados == {
        "nome": "Jeferson",
        "servico": "Instalação elétrica"
    }


def test_obter_dado_inexistente():

    session_manager = SessionManager()

    conversation_id = "teste-123"

    session_manager.criar(
        conversation_id
    )

    resultado = (
        session_manager.obter_dado(
            conversation_id,
            "nome"
        )
    )

    assert resultado is None


def test_obter_dados():

    session_manager = SessionManager()

    conversation_id = "teste-123"

    session_manager.criar(
        conversation_id
    )

    session_manager.salvar_dado(
        conversation_id,
        "nome",
        "Jeferson"
    )

    dados = (
        session_manager.obter_dados(
            conversation_id
        )
    )

    assert dados["nome"] == "Jeferson"


def test_reiniciar_sessao():

    session_manager = SessionManager()

    conversation_id = "teste-123"

    session_manager.criar(
        conversation_id
    )

    session_manager.salvar_dado(
        conversation_id,
        "nome",
        "Jeferson"
    )

    session_manager.salvar_dado(
        conversation_id,
        "servico",
        "Instalação elétrica"
    )

    session_manager.atualizar_estado(
        conversation_id,
        States.AGUARDANDO_SERVICO
    )

    session = (
        session_manager.reiniciar(
            conversation_id
        )
    )

    assert (
        session.estado
        == States.INICIO
    )

    assert session.dados == {}

    assert (
        session.ultima_interacao
        is not None
    )

    assert (
        session_manager.existe(
            conversation_id
        )
        is True
    )


def test_reiniciar_mantem_mesma_sessao():

    session_manager = SessionManager()

    conversation_id = "teste-123"

    original = (
        session_manager.criar(
            conversation_id
        )
    )

    reiniciada = (
        session_manager.reiniciar(
            conversation_id
        )
    )

    assert reiniciada is original


def test_finalizar_sessao():

    session_manager = SessionManager()

    conversation_id = "teste-123"

    session_manager.criar(
        conversation_id
    )

    assert (
        session_manager.existe(
            conversation_id
        )
        is True
    )

    session_manager.finalizar(
        conversation_id
    )

    assert (
        session_manager.existe(
            conversation_id
        )
        is False
    )


def test_finalizar_sessao_inexistente():

    session_manager = SessionManager()

    conversation_id = "nao-existe"

    session_manager.finalizar(
        conversation_id
    )

    assert (
        session_manager.existe(
            conversation_id
        )
        is False
    )


def test_obter_apos_finalizar_cria_nova_sessao():

    session_manager = SessionManager()

    conversation_id = "teste-123"

    primeira = (
        session_manager.criar(
            conversation_id
        )
    )

    session_manager.salvar_dado(
        conversation_id,
        "nome",
        "Jeferson"
    )

    session_manager.finalizar(
        conversation_id
    )

    segunda = (
        session_manager.obter(
            conversation_id
        )
    )

    assert segunda is not primeira

    assert (
        segunda.estado
        == States.INICIO
    )

    assert segunda.dados == {}


def test_dados_nao_vazam_entre_sessoes():

    session_manager = SessionManager()

    primeira_id = "teste-1"
    segunda_id = "teste-2"

    session_manager.salvar_dado(
        primeira_id,
        "nome",
        "Jeferson"
    )

    session_manager.salvar_dado(
        segunda_id,
        "nome",
        "Maria"
    )

    assert (
        session_manager.obter_dado(
            primeira_id,
            "nome"
        )
        == "Jeferson"
    )

    assert (
        session_manager.obter_dado(
            segunda_id,
            "nome"
        )
        == "Maria"
    )