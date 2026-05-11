from pathlib import Path
from parsers.json_parser import ManifestParser

from scanners.tls_scanner import TLSScanner
#from scanners.stg_scanner import STGScanner
#from scanners.universal_scanner import UniversalScanner

from validators.manifest_validator import ManifestValidator
#from validators.naming_validator import NamingValidator
#from validators.framework_validator import FrameworkValidator
#from validators.dependency_validator import DependencyValidator

#from ai.review_agent import ReviewAgent

BASE_DIR = Path(__file__).resolve().parent

manifest_path = (
    BASE_DIR.parent
    / 'manifest'
    / 'promotion-manifest.json'
)

if not manifest_path.exists():
    raise FileNotFoundError(
        f'No existe manifest: {manifest_path.resolve()}'
    )
manifest = ManifestParser().load(
    str(manifest_path)
)
print("manifest",manifest)
repo_objects = []

repo_objects.extend(
    TLSScanner().scan('./tls_parametros')
)
print("repo_objects",repo_objects)
#repo_objects.extend(
 #   STGScanner().scan('./stg')
#)

#repo_objects.extend(
#    UniversalScanner().scan('./universal')
#)

errors = []

errors.extend(
    ManifestValidator().validate(
        manifest.objetos,
        repo_objects
    )
)

#errors.extend(
#    NamingValidator().validate(repo_objects)
#)

#errors.extend(
#    DependencyValidator().validate(repo_objects)
#)

for error in errors:
    print(f'ERROR: {error}')

#if errors:
#    raise Exception('Validación fallida')
#  comments = ReviewAgent().review(
#    errors,
#    repo_objects
#)

#for comment in comments:
 #   print(comment)
