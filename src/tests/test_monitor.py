from types import SimpleNamespace

from monitor import Monitor


# ==========================================================
# FAKES
# ==========================================================

class FakeChatManager:
    """
    Simula o gerenciamento de chats do WhatsApp.
    """

    def __init__(self, chats=None):
        self.chats = chats or []
        self.abertos = []

    def listar_nao_lidas(self):
        return self.chats

    def abrir(self, chat):
        self.abertos.append(chat)
        return True


class FakeConversationManager:
    """
    Simula o ConversationManager.
    """

    def __init__(self):
        self.conversas = {}
        self.obtidas = []

    def obter_conversa(self, contato):
        self.obtidas.append(contato)

        if contato not in self.conversas:

            self.conversas[contato] = SimpleNamespace(
                id=f"conversation-{contato}",
                contato=contato
            )

        return self.conversas[contato]


class FakeBot:
    """
    Simula o WhatsAppBot.
    """

    def __init__(self, mensagens=None):
        self.mensagens = mensagens or []
        self.conversas_lidas = []

    def ler_ultimas_mensagens(self, conversation_id):

        self.conversas_lidas.append(
            conversation_id
        )

        return self.mensagens


class FakeMessageProcessor:
    """
    Simula o MessageProcessor.
    """

    def __init__(self):
        self.processadas = []

    def processar(
        self,
        mensagem,
        conversation
    ):

        self.processadas.append(
            (
                mensagem,
                conversation
            )
        )


# ==========================================================
# HELPERS
# ==========================================================

def criar_chat(nome="Jeferson"):

    return SimpleNamespace(
        nome=nome
    )


def criar_mensagem(
    message_id="msg-001",
    texto="Olá"
):

    return SimpleNamespace(
        id=message_id,
        autor="Jeferson",
        texto=texto,
        recebida=True,
        hora="20:00"
    )


def criar_monitor(
    chats=None,
    mensagens=None
):

    bot = FakeBot(
        mensagens=mensagens
    )

    chat_manager = FakeChatManager(
        chats=chats
    )

    conversation_manager = (
        FakeConversationManager()
    )

    message_processor = (
        FakeMessageProcessor()
    )

    monitor = Monitor(
        bot=bot,
        chat_manager=chat_manager,
        conversation_manager=conversation_manager,
        message_processor=message_processor
    )

    return (
        monitor,
        bot,
        chat_manager,
        conversation_manager,
        message_processor
    )


# ==========================================================
# MONITORAR
# ==========================================================

def test_monitorar_processa_mensagem():

    chat = criar_chat(
        "Jeferson"
    )

    mensagem = criar_mensagem(
        "msg-001",
        "Bom dia"
    )

    (
        monitor,
        bot,
        chat_manager,
        conversation_manager,
        message_processor
    ) = criar_monitor(
        chats=[chat],
        mensagens=[mensagem]
    )

    monitor.monitorar()

    # Chat foi aberto
    assert chat_manager.abertos == [
        chat
    ]

    # Conversa foi obtida pelo contato
    assert conversation_manager.obtidas == [
        "Jeferson"
    ]

    # Bot leu a conversa correta
    assert bot.conversas_lidas == [
        "conversation-Jeferson"
    ]

    # Mensagem foi processada
    assert len(
        message_processor.processadas
    ) == 1

    mensagem_processada, conversa = (
        message_processor.processadas[0]
    )

    assert mensagem_processada is mensagem

    assert conversa.id == (
        "conversation-Jeferson"
    )


def test_monitorar_processa_varias_mensagens():

    chat = criar_chat(
        "Jeferson"
    )

    mensagens = [

        criar_mensagem(
            "msg-001",
            "Bom dia"
        ),

        criar_mensagem(
            "msg-002",
            "Quero um orçamento"
        ),

        criar_mensagem(
            "msg-003",
            "Pode me ajudar?"
        )
    ]

    (
        monitor,
        bot,
        chat_manager,
        conversation_manager,
        message_processor
    ) = criar_monitor(
        chats=[chat],
        mensagens=mensagens
    )

    monitor.monitorar()

    # Todas as mensagens foram processadas
    assert len(
        message_processor.processadas
    ) == 3

    assert (
        message_processor.processadas[0][0]
        is mensagens[0]
    )

    assert (
        message_processor.processadas[1][0]
        is mensagens[1]
    )

    assert (
        message_processor.processadas[2][0]
        is mensagens[2]
    )


def test_monitorar_processa_varias_conversas():

    chat_1 = criar_chat(
        "Jeferson"
    )

    chat_2 = criar_chat(
        "Maria"
    )

    mensagem_1 = criar_mensagem(
        "msg-001",
        "Olá Jeferson"
    )

    mensagem_2 = criar_mensagem(
        "msg-002",
        "Olá Maria"
    )

    (
        monitor,
        bot,
        chat_manager,
        conversation_manager,
        message_processor
    ) = criar_monitor(
        chats=[
            chat_1,
            chat_2
        ],
        mensagens=[
            mensagem_1,
            mensagem_2
        ]
    )

    monitor.monitorar()

    # Os dois chats foram abertos
    assert chat_manager.abertos == [
        chat_1,
        chat_2
    ]

    # As duas conversas foram obtidas
    assert conversation_manager.obtidas == [
        "Jeferson",
        "Maria"
    ]

    # Cada conversa recebe as duas mensagens
    assert len(
        message_processor.processadas
    ) == 4


# ==========================================================
# CHAT NÃO PODE SER ABERTO
# ==========================================================

def test_monitorar_ignora_chat_que_nao_abriu():

    chat = criar_chat(
        "Jeferson"
    )

    (
        monitor,
        bot,
        chat_manager,
        conversation_manager,
        message_processor
    ) = criar_monitor(
        chats=[chat],
        mensagens=[]
    )

    # Simula falha ao abrir o chat
    chat_manager.abrir = (
        lambda chat: False
    )

    monitor.monitorar()

    # O método foi substituído,
    # portanto nenhum chat foi registrado
    assert chat_manager.abertos == []

    # Não deve buscar conversa
    assert conversation_manager.obtidas == []

    # Não deve ler mensagens
    assert bot.conversas_lidas == []

    # Não deve processar mensagens
    assert message_processor.processadas == []


# ==========================================================
# CONVERSA NÃO ENCONTRADA
# ==========================================================

def test_monitorar_ignora_conversa_inexistente():

    chat = criar_chat(
        "Jeferson"
    )

    (
        monitor,
        bot,
        chat_manager,
        conversation_manager,
        message_processor
    ) = criar_monitor(
        chats=[chat],
        mensagens=[]
    )

    # Simula conversa inexistente
    conversation_manager.obter_conversa = (
        lambda contato: None
    )

    monitor.monitorar()

    # Chat foi aberto normalmente
    assert chat_manager.abertos == [
        chat
    ]

    # Não deve tentar ler mensagens
    assert bot.conversas_lidas == []

    # Não deve processar mensagens
    assert message_processor.processadas == []


# ==========================================================
# CONVERSA SEM ID
# ==========================================================

def test_monitorar_ignora_conversa_sem_id():

    chat = criar_chat(
        "Jeferson"
    )

    (
        monitor,
        bot,
        chat_manager,
        conversation_manager,
        message_processor
    ) = criar_monitor(
        chats=[chat],
        mensagens=[]
    )

    # Simula conversa sem ID
    conversation_manager.obter_conversa = (
        lambda contato: SimpleNamespace(
            id=None,
            contato=contato
        )
    )

    monitor.monitorar()

    # Não deve ler mensagens
    assert bot.conversas_lidas == []

    # Não deve processar mensagens
    assert message_processor.processadas == []


# ==========================================================
# SEM CONVERSAS NÃO LIDAS
# ==========================================================

def test_monitorar_sem_conversas_nao_faz_nada():

    (
        monitor,
        bot,
        chat_manager,
        conversation_manager,
        message_processor
    ) = criar_monitor(
        chats=[],
        mensagens=[]
    )

    monitor.monitorar()

    # Nenhum chat
    assert chat_manager.abertos == []

    # Nenhuma conversa
    assert conversation_manager.obtidas == []

    # Nenhuma leitura
    assert bot.conversas_lidas == []

    # Nenhum processamento
    assert message_processor.processadas == []


# ==========================================================
# SEM MENSAGENS
# ==========================================================

def test_monitorar_conversa_sem_mensagens():

    chat = criar_chat(
        "Jeferson"
    )

    (
        monitor,
        bot,
        chat_manager,
        conversation_manager,
        message_processor
    ) = criar_monitor(
        chats=[chat],
        mensagens=[]
    )

    monitor.monitorar()

    # Chat foi aberto
    assert chat_manager.abertos == [
        chat
    ]

    # Conversa foi obtida
    assert conversation_manager.obtidas == [
        "Jeferson"
    ]

    # Conversa foi lida
    assert bot.conversas_lidas == [
        "conversation-Jeferson"
    ]

    # Não havia mensagens para processar
    assert message_processor.processadas == []

    # ==========================================================

# INICIAR

# ==========================================================

def test_iniciar_executa_monitoramento(
    monkeypatch
    ):


    (
        monitor,
        bot,
        chat_manager,
        conversation_manager,
        message_processor
    ) = criar_monitor()

    chamadas = []

def fake_monitorar():

    chamadas.append(
        "monitorar"
    )

    # Interrompe o while True
    # depois da primeira execução.
    raise KeyboardInterrupt

def fake_sleep(segundos):

    chamadas.append(
        f"sleep:{segundos}"
    )

    monkeypatch.setattr(
        monitor,
        "monitorar",
        fake_monitorar
    )

    monkeypatch.setattr(
        "monitor.time.sleep",
        fake_sleep
    )

    try:

        monitor.iniciar()

    except KeyboardInterrupt:

        pass

    assert chamadas == [
        "monitorar"
    ]


def test_iniciar_continua_apos_erro(
    monkeypatch
    ):


    (
        monitor,
        bot,
        chat_manager,
        conversation_manager,
        message_processor
    ) = criar_monitor()

    chamadas = []

    contador = {
        "monitorar": 0
    }

def fake_monitorar():

    contador["monitorar"] += 1

    chamadas.append(
        "monitorar"
    )

    # Primeira execução gera
    # um erro normal.
    if contador["monitorar"] == 1:

        raise Exception(
            "Erro simulado"
        )

    # Segunda execução interrompe
    # o loop do teste.
    raise KeyboardInterrupt

def fake_sleep(segundos):

    chamadas.append(
        f"sleep:{segundos}"
    )

    monkeypatch.setattr(
        monitor,
        "monitorar",
        fake_monitorar
    )

    monkeypatch.setattr(
        "monitor.time.sleep",
        fake_sleep
    )

    try:

        monitor.iniciar()

    except KeyboardInterrupt:

        pass

    assert chamadas == [
        "monitorar",
        "sleep:1",
        "monitorar"
    ]

    assert contador["monitorar"] == 2

