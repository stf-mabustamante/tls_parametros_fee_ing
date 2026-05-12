from pathlib import Path

from parsers.ini_parser import IniParser
from parsers.yaml_parser import YamlParser
from parsers.json_parser import ManifestParser

from scanners.ini_scanner import IniScanner

from validators.framework_validator import FrameworkValidator
from validators.manifest_validator import ManifestValidator


BASE_DIR = Path(__file__).resolve().parent
print("BASE_DIR:",BASE_DIR)

TASK_CATALOG_PATH = (
    BASE_DIR
    / 'config'
    / 'task_catalog.yaml'
)


MANIFEST_PATH = (
    BASE_DIR.parent
    / 'manifest'
    / 'promotion-manifest.json'
)

TLS_PARAMETROS_PATH = (
    BASE_DIR.parent
     / 'work_edge'
)


print('Loading task catalog...')

catalog = YamlParser().load(
    str(TASK_CATALOG_PATH)
)
print("catalog:",catalog)

print('Loading manifest...')

manifest = ManifestParser().load(
    str(MANIFEST_PATH)
)
print("manifest:",manifest)

print('Scanning ini files...')

ini_files = IniScanner().scan(
    str(TLS_PARAMETROS_PATH)
)
print("ini_files:",ini_files)

framework_validator = FrameworkValidator()
manifest_validator = ManifestValidator()


all_errors = []


for ini_file in ini_files:

    print(f'Processing: {ini_file}')

    tasks = IniParser().parse(
        str(ini_file)
    )

    for task in tasks:

        task_definition = catalog[
            'tasks'
        ].get(task.task_name)
        print("task_definition:",task_definition)
        if task_definition is None:

            all_errors.append(
                f'Task no registrada: '
                f'{task.task_name}'
            )

            continue

        if not task_definition.get(
            'promocionable',
            False
        ):
            continue

        framework_errors = framework_validator.validate(
            task,
            task_definition
        )

        manifest_errors = manifest_validator.validate(
            task,
            task_definition,
            manifest
        )

        all_errors.extend(framework_errors)
        all_errors.extend(manifest_errors)


if all_errors:

    print('\nVALIDATION ERRORS:\n')

    for error in all_errors:
        print(error)

    raise Exception(
        'Promotion validation failed'
    )
print('\nPromotion validation successful')
