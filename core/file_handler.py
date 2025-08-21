import json
from dataclasses import asdict

from text import Text


class FileHandler:

    def save_to_file(self, filename, buffer):
        buffer_dicts = [asdict(obj) for obj in buffer]

        with open(filename, "w") as save_file:
            json.dump(buffer_dicts, save_file, indent=4)

    def load_from_file(self, filename):
        try:
            with open(filename, "r" ) as read_file:
                loaded_data = json.load(read_file)
                return [Text(**d) for d in loaded_data]
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("File format error")
            return []

