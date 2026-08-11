from models import (
    Message,
    ChatMessage,
)


def chat_to_message(
    chat: ChatMessage,
    conversation_id: str
) -> Message:

    return Message(

        id=chat.id,

        conversation_id=conversation_id,

        autor=chat.autor,

        texto=chat.texto,

        recebida=chat.recebida,

        role=(
            "user"
            if chat.recebida
            else "assistant"
        )

    )