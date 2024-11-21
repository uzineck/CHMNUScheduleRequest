import json
from typing import Any


class JsonHandler:
    @staticmethod
    def convert_from_json_to_py_obj(value) -> Any:
        return json.load(value)

    @staticmethod
    def convert_from_json_to_py_obj_file(path_to_file) -> Any:
        with open(path_to_file, 'r', encoding='UTF-8') as file:
            return json.load(file)

    @staticmethod
    def save_to_json(data: dict | list, file_name) -> None:
        with open(f'../fixtures/{file_name}.json', 'w', encoding='UTF-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
