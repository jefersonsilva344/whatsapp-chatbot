from dataclasses import dataclass


@dataclass(slots=True)
class ChatMessage:

    id: str

    conversation_id: str

    autor: str

    role: str

    hora: str

    texto: str

    recebida: bool

    origem: str = "whatsapp"