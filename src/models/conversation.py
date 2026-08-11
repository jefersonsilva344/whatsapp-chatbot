from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Conversation:

    id: str

    contato: str

    ultima_mensagem: str | None = None

    atualizada_em: datetime | None = None

    ativa: bool = True


    def atualizar(self, mensagem):

        self.ultima_mensagem = mensagem.texto

        self.atualizada_em = (
            datetime.now()
        )