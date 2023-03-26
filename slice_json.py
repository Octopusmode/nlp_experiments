import json

# Чтение данных из исходного файла JSON
with open(r'source\result.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Выбор среза данных
subset = data['messages'][:100]

# Запись среза данных в новый файл JSON
with open(r'source\subset.json', 'w', encoding='utf-8') as f:
    json.dump(subset, f, ensure_ascii=False, indent=4)