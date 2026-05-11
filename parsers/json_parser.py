import json

from models.repo_object import RepoObject
from models.manifest import Manifest


class ManifestParser:

    def load(self, path: str) -> Manifest:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        objetos = []

        config = data.get("config", {})

        for mapping in data.get("mapeo_texto", []):
            table_name = mapping.get("nombre_tabla")

            objetos.append(
                RepoObject(
                    tipo="tabla_stg",
                    nombre=table_name,
                    path="N/A",
                    repo="stg"
                )
            )

        return Manifest(objetos=objetos)
