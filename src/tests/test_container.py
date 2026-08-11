from unittest.mock import Mock, patch

import pytest

from container import Container


# ==========================================================
# FIXTURE
# ==========================================================

@pytest.fixture
def container():
    return Container()


# ==========================================================
# TESTES DE INICIALIZAÇÃO
# ==========================================================

@patch("container.Monitor")
@patch("container.MessageProcessor")
@patch("container.FlowManager")
@patch("container.StateManager")
@patch("container.SessionManager")
@patch("container.ConversationManager")
@patch("container.ChatManager")
@patch("container.ConversationRepository")
@patch("container.MessageRepository")
@patch("container.Migration")
@patch("container.DatabaseConnection")
@patch("container.WhatsAppBot")
@patch("container.Responder")
def test_iniciar_cria_todas_dependencias(
    mock_responder,
    mock_bot,
    mock_database,
    mock_migration,
    mock_message_repository,
    mock_conversation_repository,
    mock_chat_manager,
    mock_conversation_manager,
    mock_session_manager,
    mock_state_manager,
    mock_flow_manager,
    mock_message_processor,
    mock_monitor,
    container
):

    # ------------------------------------------------------
    # Configuração dos mocks
    # ------------------------------------------------------

    bot_instance = mock_bot.return_value
    bot_instance.driver = Mock()

    db_instance = mock_database.return_value

    # ------------------------------------------------------
    # Executa
    # ------------------------------------------------------

    resultado = container.iniciar()

    # ------------------------------------------------------
    # Verificações
    # ------------------------------------------------------

    assert resultado is container

    assert container.db is db_instance
    assert container.bot is bot_instance

    assert (
        container.chat_manager
        is mock_chat_manager.return_value
    )

    assert (
        container.conversation_manager
        is mock_conversation_manager.return_value
    )

    assert (
        container.session_manager
        is mock_session_manager.return_value
    )

    assert (
        container.state_manager
        is mock_state_manager.return_value
    )

    assert (
        container.responder
        is not None
    )

    assert (
        container.flow_manager
        is mock_flow_manager.return_value
    )

    assert (
        container.message_processor
        is mock_message_processor.return_value
    )

    assert (
        container.monitor
        is mock_monitor.return_value
    )


# ==========================================================
# TESTE DA ORDEM BÁSICA DE INICIALIZAÇÃO
# ==========================================================

@patch("container.Monitor")
@patch("container.MessageProcessor")
@patch("container.FlowManager")
@patch("container.StateManager")
@patch("container.SessionManager")
@patch("container.ConversationManager")
@patch("container.ChatManager")
@patch("container.ConversationRepository")
@patch("container.MessageRepository")
@patch("container.Migration")
@patch("container.DatabaseConnection")
@patch("container.WhatsAppBot")
@patch("container.Responder")
def test_iniciar_executa_migration_e_inicia_bot(
    mock_responder,
    mock_bot,
    mock_database,
    mock_migration,
    mock_message_repository,
    mock_conversation_repository,
    mock_chat_manager,
    mock_conversation_manager,
    mock_session_manager,
    mock_state_manager,
    mock_flow_manager,
    mock_message_processor,
    mock_monitor,
    container
):

    bot_instance = mock_bot.return_value
    bot_instance.driver = Mock()

    migration_instance = mock_migration.return_value

    container.iniciar()

    # Banco foi criado
    mock_database.assert_called_once_with()

    # Migration recebeu o banco
    mock_migration.assert_called_once_with(
        mock_database.return_value
    )

    # Migration foi executada
    migration_instance.run.assert_called_once()

    # Bot foi criado
    mock_bot.assert_called_once_with()

    # Bot foi iniciado
    bot_instance.iniciar.assert_called_once()


# ==========================================================
# TESTE DAS DEPENDÊNCIAS DO MONITOR
# ==========================================================

@patch("container.Monitor")
@patch("container.MessageProcessor")
@patch("container.FlowManager")
@patch("container.StateManager")
@patch("container.SessionManager")
@patch("container.ConversationManager")
@patch("container.ChatManager")
@patch("container.ConversationRepository")
@patch("container.MessageRepository")
@patch("container.Migration")
@patch("container.DatabaseConnection")
@patch("container.WhatsAppBot")
@patch("container.Responder")
def test_monitor_recebe_dependencias_corretas(
    mock_responder,
    mock_bot,
    mock_database,
    mock_migration,
    mock_message_repository,
    mock_conversation_repository,
    mock_chat_manager,
    mock_conversation_manager,
    mock_session_manager,
    mock_state_manager,
    mock_flow_manager,
    mock_message_processor,
    mock_monitor,
    container
):

    bot_instance = mock_bot.return_value
    bot_instance.driver = Mock()

    container.iniciar()

    mock_monitor.assert_called_once_with(
        bot_instance,
        mock_chat_manager.return_value,
        mock_conversation_manager.return_value,
        mock_message_processor.return_value
    )


# ==========================================================
# TESTE DO EXECUTAR
# ==========================================================

def test_executar_sem_container_iniciado():

    container = Container()

    with pytest.raises(
        RuntimeError,
        match="Container não foi iniciado."
    ):
        container.executar()


@patch("container.Monitor")
@patch("container.MessageProcessor")
@patch("container.FlowManager")
@patch("container.StateManager")
@patch("container.SessionManager")
@patch("container.ConversationManager")
@patch("container.ChatManager")
@patch("container.ConversationRepository")
@patch("container.MessageRepository")
@patch("container.Migration")
@patch("container.DatabaseConnection")
@patch("container.WhatsAppBot")
@patch("container.Responder")
def test_executar_inicia_monitor(
    mock_responder,
    mock_bot,
    mock_database,
    mock_migration,
    mock_message_repository,
    mock_conversation_repository,
    mock_chat_manager,
    mock_conversation_manager,
    mock_session_manager,
    mock_state_manager,
    mock_flow_manager,
    mock_message_processor,
    mock_monitor,
    container
):

    bot_instance = mock_bot.return_value
    bot_instance.driver = Mock()

    container.iniciar()

    container.executar()

    mock_monitor.return_value.iniciar.assert_called_once()


# ==========================================================
# TESTE DO FECHAR
# ==========================================================

def test_fechar_sem_recursos():

    container = Container()

    # Não deve gerar erro
    container.fechar()


@patch("container.Monitor")
@patch("container.MessageProcessor")
@patch("container.FlowManager")
@patch("container.StateManager")
@patch("container.SessionManager")
@patch("container.ConversationManager")
@patch("container.ChatManager")
@patch("container.ConversationRepository")
@patch("container.MessageRepository")
@patch("container.Migration")
@patch("container.DatabaseConnection")
@patch("container.WhatsAppBot")
@patch("container.Responder")
def test_fechar_fecha_bot_e_banco(
    mock_responder,
    mock_bot,
    mock_database,
    mock_migration,
    mock_message_repository,
    mock_conversation_repository,
    mock_chat_manager,
    mock_conversation_manager,
    mock_session_manager,
    mock_state_manager,
    mock_flow_manager,
    mock_message_processor,
    mock_monitor,
    container
):

    bot_instance = mock_bot.return_value
    bot_instance.driver = Mock()

    db_instance = mock_database.return_value

    container.iniciar()

    container.fechar()

    bot_instance.fechar.assert_called_once()
    db_instance.close.assert_called_once()