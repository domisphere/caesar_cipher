import json


class FileHandler:

    def save_to_file(self, filename: str, buffer: list[dict]) -> None:

        with open(filename, "w") as safe_file:
            json.dump(buffer, safe_file, indent=4)

    def load_from_file(self, filename: str) -> list[dict]:
        with open(filename, "r" ) as read_file:
            loaded_data = json.load(read_file)

        return loaded_data
