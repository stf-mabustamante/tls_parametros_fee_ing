from dataclasses import dataclass
from typing import List

from models.repo_object import RepoObject


@dataclass
class Manifest:
    objetos: List[RepoObject]
