from dataclasses import dataclass


@dataclass
class Message:

    id: str

    conversation_id: str

    autor: str

    texto: str

    recebida: bool

    role: str