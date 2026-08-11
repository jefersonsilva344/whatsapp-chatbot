from dataclasses import dataclass, field
from datetime import datetime

from state.states import States


@dataclass
class Session:

    conversation_id: str

    estado: States = States.INICIO

    dados: dict = field(default_factory=dict)

    ultima_interacao: datetime = field(
        default_factory=datetime.now
    )