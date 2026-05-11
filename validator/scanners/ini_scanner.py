from pathlib import Path


class IniScanner:

    def scan(self, base_path: str):

        ini_files = []

        for file in Path(base_path).rglob('*.ini'):
            ini_files.append(file)

        return ini_files
