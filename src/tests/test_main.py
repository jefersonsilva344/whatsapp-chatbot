
from unittest.mock import Mock, patch

import main


# ==========================================================
# TESTE DA EXECUÇÃO PRINCIPAL
# ==========================================================

@patch("main.Container")
def test_main_inicia_e_executa_container(
    mock_container
):

    container = mock_container.return_value

    main.main()

    # Container foi criado
    mock_container.assert_called_once_with()

    # Container foi inicializado
    container.iniciar.assert_called_once()

    # Monitor foi executado
    container.executar.assert_called_once()

    # Recursos foram encerrados
    container.fechar.assert_called_once()


# ==========================================================
# TESTE DE ENCERRAMENTO APÓS ERRO
# ==========================================================

@patch("main.Container")
def test_main_fecha_container_se_ocorrer_erro(
    mock_container
):

    container = mock_container.return_value

    container.executar.side_effect = (
        RuntimeError("Erro de teste")
    )

    main.main()

    # Inicialização ocorreu
    container.iniciar.assert_called_once()

    # Execução ocorreu
    container.executar.assert_called_once()

    # Mesmo com erro, deve fechar
    container.fechar.assert_called_once()


# ==========================================================
# TESTE DE ERRO NA INICIALIZAÇÃO
# ==========================================================

@patch("main.Container")
def test_main_fecha_container_se_inicializacao_falhar(
    mock_container
):

    container = mock_container.return_value

    container.iniciar.side_effect = (
        RuntimeError("Falha na inicialização")
    )

    main.main()

    # Tentou inicializar
    container.iniciar.assert_called_once()

    # Como a inicialização falhou,
    # executar não deve ser chamado
    container.executar.assert_not_called()

    # O finally deve fechar os recursos
    container.fechar.assert_called_once()


# ==========================================================
# TESTE DE ERRO NO EXECUTAR
# ==========================================================

@patch("main.Container")
def test_main_continua_fluxo_de_encerramento_apos_erro(
    mock_container
):

    container = mock_container.return_value

    container.executar.side_effect = (
        Exception("Erro durante execução")
    )

    main.main()

    container.iniciar.assert_called_once()
    container.executar.assert_called_once()
    container.fechar.assert_called_once()




