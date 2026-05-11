from pathlib import Path

from models.repo_object import RepoObject


class TLSScanner:

    def scan(self, root_path: str):

        objects = []

        for file in Path(root_path).rglob('*'):

            if file.name.startswith('schema_') and file.suffix == '.json':
                objects.append(
                    RepoObject(
                        tipo='schema',
                        nombre=file.name,
                        path=str(file),
                        repo='tls_parametros'
                    )
                )

            elif file.suffix == '.ini':
                objects.append(
                    RepoObject(
                        tipo='ini',
                        nombre=file.name,
                        path=str(file),
                        repo='tls_parametros'
                    )
                )

        return objects
