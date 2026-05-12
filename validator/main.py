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
#{'name': 'tst-stage-cu83', 'run_id': 'r_Fc1pz9ZakgtiYuqa', 'model': 'claude-sonnet-4.5', 'rules_ref': 'master', 'framework_repo': 'bch-datos/fw-ingesta-tasks', 'context_repo': 'bch-datos/inputs_ingesta_copilot', 'organization': 'devsecops'
#, 'mapeo_texto': [{'proyecto': 'bch-prj-sti-fil-pr-1231', 'dataset': 'production_stage', 'nombre_tabla': 'tbl_feebnc_running_foto_mes', 'columna_destino': 'periodo_mes', 'tipo_clave': None, 'tipo_dato': 'DATE', 'hu': 'PAS0050-1301', 'celula': 'Valhalla'}, {'proyecto': 'bch-prj-sti-fil-pr-1231', 'dataset': 'production_stage', 'nombre_tabla': 'tbl_feebnc_running_foto_mes', 'columna_destino': 'gerencia', 'tipo_clave': None, 'tipo_dato': 'STRING', 'hu': 'PAS0050-1301', 'celula': 'Valhalla'}, {'proyecto': 'bch-prj-sti-fil-pr-1231', 'dataset': 'production_stage', 'nombre_tabla': 'tbl_feebnc_running_foto_mes', 'columna_destino': 'area', 'tipo_clave': None, 'tipo_dato': 'STRING', 'hu': 'PAS0050-1301', 'celula': 'Valhalla'}]
#, 'interfaz_texto': [{'numero_columna': 1, 'nombre_campo': 'GERENCIA', 'tipo_dato': 'nvarchar(30)', 'descripcion_campo': 'Corresponde a la Gerencia donde se especifica el nombre de la gerencia Banchile.'}, {'numero_columna': 2, 'nombre_campo': 'AREA', 'tipo_dato': 'nvarchar(30)', 'descripcion_campo': 'Corresponde al área donde se especifica el nombre del área de Banchile, incluye el área digital.'}, {'numero_columna': 3, 'nombre_campo': 'ZONA', 'tipo_dato': 'nvarchar(30)', 'descripcion_campo': 'Corresponde a la zona donde se especifica el nombre de la zona de Banchile.'}]
#, 'config': {'jobName': 'tst-stage-cu83', 'description': 'Descripción de ingesta', 'responsables': {'gerencia': 'Gerencia', 'subgerencia': 'SubGerencia', 'celula': 'AdopcionGCP'}
              #, 'viewers': ['DSO_TOOLS_PRD_GDD_ADOPCIONGCP_SM', 'DSO_TOOLS_PRD_GDD_ADOPCIONGCP_DEV', 'DSO_TOOLS_PRD_GDD_ADOPCIONGCP_LT', 'DSO_TOOLS_PRD_GDD_ADOPCIONGCP_QA', 'DSO_TOOLS_PRD_GDD_QA']
              #, 'environments': [{'name': 'desa', 'gcpProjectId': 'projects/511566960224', 'gcpRegion': 'us-east4', 'cloudRunJob': True}, {'name': 'qa', 'promotion': 'aprobacion_para_qa', 'gcpProjectId': 'projects/61204556412', 'gcpRegion': 'us-east4', 'cloudRunJob': True}, {'name': 'prod', 'promotion': 'aprobacion_para_prod', 'gcpProjectId': 'projects/783049607543', 'gcpRegion': 'us-east4', 'cloudRunJob': True}]
              #, 'veracodeAppl': 'BDGTAC', 'veracodeWorkspace': 'DEVSECOPS-GCPRUNPY-BDGTAC'}}

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

    #obtenemos la definicion completa de la tarea.
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
            task, #compara la tarea del archivo .ini con definicion de tarea del archivo task_catalog.yaml. Busca parametros oblogatorios
            task_definition  #definicion de tarea del archivo task_catalog.yaml
        )

    #obtiene el producer.extractor de la tarea, por ejemplo producer {type:dbt_models,extractor: from:MESSAGE.appname} 
    #obtiene el valor del parametro especificado en el extractor, buscando dentro del .ini
    #el valor del parametro lo busca en el manifest
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
