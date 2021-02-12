import json

def read(file_path) -> dict:
    with open(file_path, mode='r', encoding='utf-8') as f:
        return json.load(f)


def write(file_path, json_data: json):
    with open(file_path, mode='w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
