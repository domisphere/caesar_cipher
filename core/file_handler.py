import json
import os
from dataclasses import asdict

from core.text import Text


class FileHandler:

    def save_to_file(self, filename, buffer):
        new_buffer = [asdict(obj) for obj in buffer]

        with open(filename, "w") as save_file:
            json.dump(new_buffer, save_file, indent=4)

    def load_from_file(self, filename):
        if not os.path.exists(filename):
            return []
        try:
            with open(filename, "r" ) as read_file:
                loaded_data = json.load(read_file)
                return [Text(**d) for d in loaded_data]
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("File format error")
            return []

