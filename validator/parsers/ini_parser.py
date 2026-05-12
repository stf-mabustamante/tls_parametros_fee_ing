import json

from models.framework_task import FrameworkTask


class IniParser:

    def parse(self, file_path: str):

        params = {}

        with open(file_path, 'r', encoding='utf-8') as f:

            for raw_line in f:

                line = raw_line.strip()

                if not line:
                    continue

                if line.startswith('#'):
                    continue

                if '=' not in line:
                    continue

                key, value = line.split(
                    '=',
                    1
                )

                key = key.strip()

                value = value.strip().strip('\"')

                if key == 'MESSAGE':

                    try:
                        params[key] = json.loads(value)

                    except Exception:
                        params[key] = value

                else:
                    params[key] = value

        task_name = params.get('TASK')

        if task_name is None:

            raise Exception(
                f'Archivo {file_path} no tiene TASK'
            )

        return FrameworkTask(
            task_name=task_name,
            params=params
        )
