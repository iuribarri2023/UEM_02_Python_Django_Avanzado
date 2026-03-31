import json

with open("datadump.json", "r", encoding="latin-1") as source_file:
    data = json.load(source_file)

with open("datadump_utf8.json", "w", encoding="utf-8") as target_file:
    json.dump(data, target_file, ensure_ascii=False, indent=4)

print("Archivo convertido a UTF-8: datadump_utf8.json")
