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
#{'tasks': 
#                 {'fw_ingesta_tasks.dbt/run:dbt_run': 
#	                                                 {'category': 'DBT'
#	                                                 , 'promocionable': True, 
#	                                                 'required_params': ['BYPASS', 'CLOUD_RUN_NAME', 'CONDA_ENV', 'ENABLED', 'FLG_CLOUD_RUN', 'FLG_PCM', 'MASTER_MACHINE_TYPE', 'MESSAGE.appname', 'MESSAGE.runid', 'MESSAGE.periodo', 'NUN_WORKERS', 'PCM_CLOUDRUN_JOB', 'PCM_DATABASE_URL', 'PCM_DEFAULT_CONTROLS_SA', 'PCM_DEFAULT_SA', 'PCM_DOM_BUCKET_RAW', 'PCM_DOM_BUCKET_UDF', 'PCM_DOM_PROJECT_ID', 'PCM_ENVIRONMENT', 'PCM_EXTRA_VARS', 'PCM_INVOKER_SA', 'PCM_PROJECT_ID', 'PCM_PUBSUB_TOPIC', 'PROJECT', 'SERVICE_ACCOUNT', 'SISTEMA', 'TOPICS_EXECUTE', 'TOPICS_MONITOR', 'WORKER_BOOT_DISK_SIZE']
#                                                     , 'optional_params': ['WORKER_MACHINE_TYPE']
#                                                     , 'produces': {'type': 'dbt_model', 'extractor': {'from': 'MESSAGE.appname'}}
#                                                     }
#	             }
#       }

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
#ini_files: [PosixPath('/home/runner/work/tls_parametros_fee_ing/tls_parametros_fee_ing/work_edge/FDDFEE-UNI004-P-E-301.ini')]

framework_validator = FrameworkValidator()
manifest_validator = ManifestValidator()


all_errors = []


for ini_file in ini_files:

    print(f'Processing: {ini_file}')

    task = IniParser().parse(
        str(ini_file)
    )
    print("task:",task)
    #FrameworkTask(task_name='fw_ingesta_tasks.dbt/run:dbt_run', params={'TASK': 'fw_ingesta_tasks.dbt/run:dbt_run,'ACCION': 'execute_framework', 'SISTEMA': 'fee'...
    
    task_definition = catalog['tasks'].get(task.task_name)
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
