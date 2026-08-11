from session.session_manager import SessionManager
from state.state_manager import StateManager
from state.states import States
from flow.flow_manager import FlowManager


# ==========================================================
# FIXTURE
# ==========================================================

def criar_flow_manager():

    session_manager = SessionManager()

    state_manager = StateManager(
        session_manager
    )

    flow_manager = FlowManager(
        session_manager,
        state_manager,
        responder=None
    )

    return (
        flow_manager,
        session_manager,
        state_manager
    )


# ==========================================================
# TESTE 1
# ==========================================================

def test_inicio_pergunta_nome():

    (
        flow_manager,
        session_manager,
        state_manager
    ) = criar_flow_manager()

    conversation_id = "conversation-1"

    resposta = flow_manager.processar(
        conversation_id,
        "Olá"
    )

    assert resposta == (
        "Olá! Qual seu nome?"
    )

    assert (
        state_manager.obter_estado(
            conversation_id
        )
        == States.AGUARDANDO_NOME
    )


# ==========================================================
# TESTE 2
# ==========================================================

def test_captura_nome():

    (
        flow_manager,
        session_manager,
        state_manager
    ) = criar_flow_manager()

    conversation_id = "conversation-2"

    flow_manager.processar(
        conversation_id,
        "Olá"
    )

    resposta = flow_manager.processar(
        conversation_id,
        "Jeferson"
    )

    assert resposta == (
        "Prazer Jeferson! "
        "Qual serviço você precisa?"
    )

    assert (
        session_manager.obter_dado(
            conversation_id,
            "nome"
        )
        == "Jeferson"
    )

    assert (
        state_manager.obter_estado(
            conversation_id
        )
        == States.AGUARDANDO_SERVICO
    )


# ==========================================================
# TESTE 3
# ==========================================================

def test_captura_servico():

    (
        flow_manager,
        session_manager,
        state_manager
    ) = criar_flow_manager()

    conversation_id = "conversation-3"

    flow_manager.processar(
        conversation_id,
        "Olá"
    )

    flow_manager.processar(
        conversation_id,
        "Jeferson"
    )

    resposta = flow_manager.processar(
        conversation_id,
        "Instalação de iluminação"
    )

    assert resposta == (
        "Vou preparar seu orçamento."
    )

    assert (
        session_manager.obter_dado(
            conversation_id,
            "servico"
        )
        == "Instalação de iluminação"
    )

    assert (
        state_manager.obter_estado(
            conversation_id
        )
        == States.ORCAMENTO
    )


# ==========================================================
# TESTE 4
# ==========================================================

def test_geracao_orcamento():

    (
        flow_manager,
        session_manager,
        state_manager
    ) = criar_flow_manager()

    conversation_id = "conversation-4"

    flow_manager.processar(
        conversation_id,
        "Olá"
    )

    flow_manager.processar(
        conversation_id,
        "Jeferson"
    )

    flow_manager.processar(
        conversation_id,
        "Instalação de LED"
    )

    resposta = flow_manager.processar(
        conversation_id,
        "Pode gerar"
    )

    assert resposta == (
        "Orçamento para "
        "Instalação de LED "
        "foi criado."
    )

    assert (
        state_manager.obter_estado(
            conversation_id
        )
        == States.CONFIRMACAO
    )


# ==========================================================
# TESTE 5
# ==========================================================

def test_finalizacao_atendimento():

    (
        flow_manager,
        session_manager,
        state_manager
    ) = criar_flow_manager()

    conversation_id = "conversation-5"

    flow_manager.processar(
        conversation_id,
        "Olá"
    )

    flow_manager.processar(
        conversation_id,
        "Jeferson"
    )

    flow_manager.processar(
        conversation_id,
        "Instalação elétrica"
    )

    flow_manager.processar(
        conversation_id,
        "Gerar orçamento"
    )

    resposta = flow_manager.processar(
        conversation_id,
        "Confirmar"
    )

    assert resposta == (
        "Obrigado! Atendimento finalizado."
    )

    assert (
        state_manager.obter_estado(
            conversation_id
        )
        == States.FINALIZADO
    )


# ==========================================================
# TESTE 6
# ==========================================================

def test_fluxo_completo():

    (
        flow_manager,
        session_manager,
        state_manager
    ) = criar_flow_manager()

    conversation_id = "conversation-completa"

    resposta_1 = flow_manager.processar(
        conversation_id,
        "Olá"
    )

    assert resposta_1 == (
        "Olá! Qual seu nome?"
    )

    assert (
        state_manager.obter_estado(
            conversation_id
        )
        == States.AGUARDANDO_NOME
    )


    resposta_2 = flow_manager.processar(
        conversation_id,
        "Jeferson"
    )

    assert resposta_2 == (
        "Prazer Jeferson! "
        "Qual serviço você precisa?"
    )

    assert (
        session_manager.obter_dado(
            conversation_id,
            "nome"
        )
        == "Jeferson"
    )

    assert (
        state_manager.obter_estado(
            conversation_id
        )
        == States.AGUARDANDO_SERVICO
    )


    resposta_3 = flow_manager.processar(
        conversation_id,
        "Automação residencial"
    )

    assert resposta_3 == (
        "Vou preparar seu orçamento."
    )

    assert (
        session_manager.obter_dado(
            conversation_id,
            "servico"
        )
        == "Automação residencial"
    )

    assert (
        state_manager.obter_estado(
            conversation_id
        )
        == States.ORCAMENTO
    )


    resposta_4 = flow_manager.processar(
        conversation_id,
        "Gerar orçamento"
    )

    assert resposta_4 == (
        "Orçamento para "
        "Automação residencial "
        "foi criado."
    )

    assert (
        state_manager.obter_estado(
            conversation_id
        )
        == States.CONFIRMACAO
    )


    resposta_5 = flow_manager.processar(
        conversation_id,
        "Confirmar"
    )

    assert resposta_5 == (
        "Obrigado! Atendimento finalizado."
    )

    assert (
        state_manager.obter_estado(
            conversation_id
        )
        == States.FINALIZADO
    )


# ==========================================================
# TESTE 7
# ==========================================================

def test_fluxo_reinicia_apos_finalizado():

    (
        flow_manager,
        session_manager,
        state_manager
    ) = criar_flow_manager()

    conversation_id = "conversation-6"

    # Executa o fluxo até FINALIZADO

    flow_manager.processar(
        conversation_id,
        "Olá"
    )

    flow_manager.processar(
        conversation_id,
        "Jeferson"
    )

    flow_manager.processar(
        conversation_id,
        "Instalação elétrica"
    )

    flow_manager.processar(
        conversation_id,
        "Gerar orçamento"
    )

    flow_manager.processar(
        conversation_id,
        "Confirmar"
    )

    assert (
        state_manager.obter_estado(
            conversation_id
        )
        == States.FINALIZADO
    )


    # Nova mensagem após finalização

    resposta = flow_manager.processar(
        conversation_id,
        "Olá novamente"
    )

    assert resposta == (
        "Olá! Qual seu nome?"
    )

    assert (
        state_manager.obter_estado(
            conversation_id
        )
        == States.AGUARDANDO_NOME
    )


    # Dados antigos devem ter sido apagados

    assert (
        session_manager.obter_dado(
            conversation_id,
            "nome"
        )
        is None
    )

    assert (
        session_manager.obter_dado(
            conversation_id,
            "servico"
        )
        is None
    )