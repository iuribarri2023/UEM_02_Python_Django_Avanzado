import json
from pathlib import Path

SOURCE = Path('datadump.json')
TARGET = Path('datadump_utf8.json')
ENCODINGS = ('utf-8', 'cp1252', 'latin-1')

for encoding in ENCODINGS:
    try:
        with SOURCE.open('r', encoding=encoding) as source_file:
            data = json.load(source_file)
        with TARGET.open('w', encoding='utf-8') as target_file:
            json.dump(data, target_file, ensure_ascii=False, indent=4)
        print(f'Archivo convertido a UTF-8 desde {encoding}: {TARGET.name}')
        break
    except UnicodeDecodeError:
        continue
else:
    raise UnicodeDecodeError('unknown', b'', 0, 1, 'No se pudo detectar una codificacion valida para datadump.json')
