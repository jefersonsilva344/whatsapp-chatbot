from selenium.webdriver.common.by import By

# ==========================================================
# PERFIL
# ==========================================================

PROFILE_BUTTON = [

    (
        By.CSS_SELECTOR,
        'button[aria-label="Perfil"]'
    ),

    (
        By.XPATH,
        '//button[@data-navbar-item="true"]'
    )

]


PROFILE_NAME = [

    (
        By.XPATH,
        '//span[normalize-space()="Nome comercial"]/following-sibling::span[1]'
    ),

    (
        By.XPATH,
        '//*[normalize-space()="Nome comercial"]/following::span[1]'
    )

]


PROFILE_CLOSE = [

    (
        By.CSS_SELECTOR,
        '[data-testid="close-refreshed"]'
    )

]


# ==========================================================
# WHATSAPP
# ==========================================================

SIDEBAR = (
    By.ID,
    "side"
)


# ==========================================================
# LISTA DE CONVERSAS
# ==========================================================

CHAT_LIST = (
    By.CSS_SELECTOR,
    '#pane-side [data-testid="chat-list"]'
)


CHAT_ITEMS = (
    By.CSS_SELECTOR,
    '#pane-side [data-testid^="list-item-"]'
)


CHAT_CONTAINER = (
    By.CSS_SELECTOR,
    '[data-testid="cell-frame-container"]'
)


CHAT_NAME = (
    By.CSS_SELECTOR,
    'span[title]'
)


CHAT_TIME = (
    By.CSS_SELECTOR,
    '[data-testid="cell-frame-primary-detail"]'
)


LAST_MESSAGE = (
    By.CSS_SELECTOR,
    '[data-testid="last-msg-status"]'
)


# ==========================================================
# MENSAGENS NÃO LIDAS
# ==========================================================

UNREAD_BADGE = (
    By.CSS_SELECTOR,
    '[data-testid="icon-unread-count"]'
)


UNREAD_COUNT = (
    By.CSS_SELECTOR,
    '[data-testid="icon-unread-count"] span'
)


# ==========================================================
# PESQUISA
# ==========================================================

SEARCH_BOX = [

    (
        By.XPATH,
        '//input[@role="textbox" and contains(@aria-label,"Pesquisar")]'
    ),

    (
        By.CSS_SELECTOR,
        'input[aria-label*="Pesquisar"]'
    ),

    (
        By.CSS_SELECTOR,
        'input[role="textbox"]'
    )

]


# ==========================================================
# CONVERSA
# ==========================================================

MESSAGE_BOX = [

    (
        By.CSS_SELECTOR,
        '[data-testid="conversation-compose-box-input"]'
    ),

    (
        By.CSS_SELECTOR,
        'div[contenteditable="true"]'
    ),

    (
        By.XPATH,
        '//div[@contenteditable="true"]'
    )

]

CHAT_TITLE = (
    By.CSS_SELECTOR,
    '[data-testid="conversation-info-header-chat-title"]'
)

BACK_BUTTON = (
    By.CSS_SELECTOR,
    '[data-testid="back"]'
)

MESSAGE_LIST = (
    By.CSS_SELECTOR,
    'div.copyable-text'
)


MESSAGE_TEXT = (
    By.CSS_SELECTOR,
    "span[data-testid='selectable-text']"
)


# ==========================================================
# CONTATO ESPECÍFICO
# ==========================================================

def CONTACT(nome):

    return (
        By.XPATH,
        f'//span[@title="{nome}"]'
    )