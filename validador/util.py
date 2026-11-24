from dataclasses import dataclass, field


@dataclass
class Resultado:
    aceita: bool
    traco: list = field(default_factory=list)
    motivo: str = ""
