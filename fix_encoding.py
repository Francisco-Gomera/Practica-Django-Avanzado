import json
import chardet

# Detectar la codificación
with open('datadump.json', 'rb') as f:
    raw_data = f.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    print(f"Codificación detectada: {encoding}")

# Leer con la codificación correcta y guardar en UTF-8
with open('datadump.json', 'r', encoding=encoding) as f:
    data = json.load(f)

with open('datadump.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("Archivo convertido a UTF-8 exitosamente")
