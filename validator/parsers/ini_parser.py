import json
import configparser

from models.framework_task import FrameworkTask


class IniParser:

    def parse(self, file_path: str):

        parser = configparser.ConfigParser()

        parser.optionxform = str

        parser.read(file_path)

        tasks = []

        for section in parser.sections():

            params = {}

            for key, value in parser[section].items():

                if key == 'MESSAGE':
                  
                    try:
                        params[key] = json.loads(value)

                    except Exception:
                        params[key] = value

                else:
                    params[key] = value

            task = FrameworkTask(
                task_name=section,
                params=params
            )

            tasks.append(task)

        return tasks
