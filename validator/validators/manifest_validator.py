class ManifestValidator:

    def validate(self, manifest_objects, repo_objects):

        errors = []

        manifest_names = {
            obj.nombre for obj in manifest_objects
        }

        repo_names = {
            obj.nombre for obj in repo_objects
        }

        sobrantes = repo_names - manifest_names
        faltantes = manifest_names - repo_names

        for item in sobrantes:
            errors.append(
                f'Objeto no declarado en verdad.json: {item}'
            )

        for item in faltantes:
            errors.append(
                f'Objeto declarado pero inexistente: {item}'
            )

        return errors
