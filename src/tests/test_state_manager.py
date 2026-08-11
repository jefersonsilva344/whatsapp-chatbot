
from state.states import States
from state.state_manager import StateManager
from session.session_manager import SessionManager


def test_sessao_inicia_em_inicio():

    session_manager = SessionManager()
    state_manager = StateManager(session_manager)

    conversation_id = "teste-123"

    estado = state_manager.obter_estado(
        conversation_id
    )

    assert estado == States.INICIO


def test_transicao_inicio_para_aguardando_nome():

    session_manager = SessionManager()
    state_manager = StateManager(session_manager)

    conversation_id = "teste-123"

    resultado = state_manager.mudar_estado(
        conversation_id,
        States.AGUARDANDO_NOME
    )

    assert resultado is True

    estado = state_manager.obter_estado(
        conversation_id
    )

    assert estado == States.AGUARDANDO_NOME


def test_transicao_invalida():

    session_manager = SessionManager()
    state_manager = StateManager(session_manager)

    conversation_id = "teste-123"

    resultado = state_manager.mudar_estado(
        conversation_id,
        States.ORCAMENTO
    )

    assert resultado is False

    estado = state_manager.obter_estado(
        conversation_id
    )

    assert estado == States.INICIO


def test_fluxo_completo_de_estados():

    session_manager = SessionManager()
    state_manager = StateManager(session_manager)

    conversation_id = "teste-123"

    assert state_manager.mudar_estado(
        conversation_id,
        States.AGUARDANDO_NOME
    )

    assert state_manager.mudar_estado(
        conversation_id,
        States.AGUARDANDO_SERVICO
    )

    assert state_manager.mudar_estado(
        conversation_id,
        States.ORCAMENTO
    )

    assert state_manager.mudar_estado(
        conversation_id,
        States.CONFIRMACAO
    )

    assert state_manager.mudar_estado(
        conversation_id,
        States.FINALIZADO
    )

    assert (
        state_manager.obter_estado(
            conversation_id
        )
        == States.FINALIZADO
    )