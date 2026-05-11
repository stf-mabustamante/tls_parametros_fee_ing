from utils.dict_utils import get_nested


class ManifestValidator:

    def validate(self,
                 task,
                 task_definition,
                 manifest):

        errors = []

        produces = task_definition.get('produces')

        if not produces:
            return errors

        extractor = produces.get('extractor')
                   
        if not extractor:
            return errors

        extraction_path = extractor.get('from')

        object_name = get_nested(
            task.params,
            extraction_path
        )

        if object_name is None:

            errors.append(
                f'No se pudo extraer objeto '
                f'para task {task.task_name}'
            )

            return errors

        manifest_text = str(manifest)

        if object_name not in manifest_text:

            errors.append(
                f'Objeto [{object_name}] '
                f'no existe en promotion-manifest.json'
            )
        return errors
