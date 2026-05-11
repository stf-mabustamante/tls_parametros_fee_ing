from utils.dict_utils import get_nested


class FrameworkValidator:

    def validate(self, task, task_definition):

        errors = []

        required_params = task_definition.get(
            'required_params',
            []
        )

        for required_param in required_params:

            value = get_nested(
                task.params,
                required_param
            )

            if value is None:

                errors.append(
                    f'Task [{task.task_name}] '
                   f'no tiene parámetro requerido: '
                    f'{required_param}'
                )

        return errors
