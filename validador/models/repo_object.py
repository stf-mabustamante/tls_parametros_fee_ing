from dataclasses import dataclass
from typing import Optional


@dataclass
class RepoObject:
    tipo: str
    nombre: str
    path: str
    repo: str
    promocionable: bool = True
    metadata: Optional[dict] = None
