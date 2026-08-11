from types import SimpleNamespace

from bot import WhatsAppBot
from message.message_processor import MessageProcessor

from flow.flow_manager import FlowManager
from session.session_manager import SessionManager
from state.state_manager import StateManager


class FakeBot:

    def __init__(self):

        self.meu_nome = "ilumina ai"

        self.mensagens_enviadas = []


    def enviar_mensagem(self, texto):

        self.mensagens_enviadas.append(
            texto
        )


class FakeRepository:

    def __init__(self):

        self.mensagens = {}

        self.respostas = []

        self.respondidas = []


    def exists_by_id(self, message_id):

        return message_id in self.mensagens


    def save(self, mensagem):

        self.mensagens[
            mensagem.id
        ] = mensagem

        return True


    def mark_answered(self, message_id):

        self.respondidas.append(
            message_id
        )


class FakeConversationManager:

    def __init__(self):

        self.atualizacoes = []


    def atualizar(
        self,
        conversation,
        mensagem
    ):

        self.atualizacoes.append(
            (
                conversation,
                mensagem
            )
        )


def criar_processor():

    bot = FakeBot()

    repository = FakeRepository()

    conversation_manager = (
        FakeConversationManager()
    )

    session_manager = SessionManager()

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

    return (
        processor,
        bot,
        repository,
        conversation_manager,
        session_manager,
        state_manager
    )


def criar_dados(
    message_id,
    texto,
    recebida=True
):

    return SimpleNamespace(

        id=message_id,

        autor="jefin",

        texto=texto,

        recebida=recebida,

        hora="03:00"

    )


def criar_conversa():

    return SimpleNamespace(

        id="conversation-123",

        contato="jefin"

    )


def test_processa_nova_mensagem():

    (
        processor,
        bot,
        repository,
        conversation_manager,
        session_manager,
        state_manager
    ) = criar_processor()


    conversa = criar_conversa()

    dados = criar_dados(
        "msg-001",
        "Bom dia"
    )


    processor.processar(
        dados,
        conversa
    )


    assert "msg-001" in (
        repository.mensagens
    )


    assert len(
        conversation_manager.atualizacoes
    ) == 1


    assert bot.mensagens_enviadas == [
        "Olá! Qual seu nome?"
    ]


def test_ignora_mensagem_do_bot():

    (
        processor,
        bot,
        repository,
        conversation_manager,
        session_manager,
        state_manager
    ) = criar_processor()


    conversa = criar_conversa()

    dados = criar_dados(
        "msg-002",
        "Olá",
        recebida=False
    )


    processor.processar(
        dados,
        conversa
    )


    assert repository.mensagens == {}

    assert bot.mensagens_enviadas == []

    assert (
        conversation_manager.atualizacoes
        == []
    )


def test_ignora_mensagem_duplicada():

    (
        processor,
        bot,
        repository,
        conversation_manager,
        session_manager,
        state_manager
    ) = criar_processor()


    conversa = criar_conversa()

    dados = criar_dados(
        "msg-003",
        "Bom dia"
    )


    repository.save(
        SimpleNamespace(
            id="msg-003"
        )
    )


    processor.processar(
        dados,
        conversa
    )


    assert len(
        conversation_manager.atualizacoes
    ) == 0


    assert bot.mensagens_enviadas == []


def test_salva_resposta_do_bot():

    (
        processor,
        bot,
        repository,
        conversation_manager,
        session_manager,
        state_manager
    ) = criar_processor()


    conversa = criar_conversa()

    dados = criar_dados(
        "msg-004",
        "Bom dia"
    )


    processor.processar(
        dados,
        conversa
    )


    mensagens = list(
        repository.mensagens.values()
    )


    assert len(mensagens) == 2


    resposta = mensagens[1]


    assert resposta.texto == (
        "Olá! Qual seu nome?"
    )


    assert resposta.autor == (
        "ilumina ai"
    )


    assert resposta.recebida is False

    assert resposta.role == "assistant"


def test_marca_mensagem_como_respondida():

    (
        processor,
        bot,
        repository,
        conversation_manager,
        session_manager,
        state_manager
    ) = criar_processor()


    conversa = criar_conversa()

    dados = criar_dados(
        "msg-005",
        "Bom dia"
    )


    processor.processar(
        dados,
        conversa
    )


    assert repository.respondidas == [
        "msg-005"
    ]


def test_atualiza_estado_do_fluxo():

    (
        processor,
        bot,
        repository,
        conversation_manager,
        session_manager,
        state_manager
    ) = criar_processor()


    conversa = criar_conversa()

    dados = criar_dados(
        "msg-006",
        "Bom dia"
    )


    processor.processar(
        dados,
        conversa
    )


    estado = (
        state_manager.obter_estado(
            conversa.id
        )
    )


    from state.states import States

    assert estado == (
        States.AGUARDANDO_NOME
    )


def test_fluxo_completo_com_message_processor():

    (
        processor,
        bot,
        repository,
        conversation_manager,
        session_manager,
        state_manager
    ) = criar_processor()


    conversa = criar_conversa()


    mensagens = [

        ("msg-101", "Bom dia"),

        ("msg-102", "Jeferson"),

        ("msg-103", "Instalação elétrica"),

        ("msg-104", "Pode gerar"),

        ("msg-105", "Sim")

    ]


    for message_id, texto in mensagens:

        dados = criar_dados(
            message_id,
            texto
        )

        processor.processar(
            dados,
            conversa
        )


    assert bot.mensagens_enviadas == [

        "Olá! Qual seu nome?",

        "Prazer Jeferson! "
        "Qual serviço você precisa?",

        "Vou preparar seu orçamento.",

        "Orçamento para "
        "Instalação elétrica foi criado.",

        "Obrigado! Atendimento finalizado."

    ]


    from state.states import States

    estado = (
        state_manager.obter_estado(
            conversa.id
        )
    )


    assert estado == (
        States.FINALIZADO
    )


    assert len(
        repository.mensagens
    ) == 10


    assert repository.respondidas == [

        "msg-101",
        "msg-102",
        "msg-103",
        "msg-104",
        "msg-105"

    ]