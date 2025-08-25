from dataclasses import asdict

from core.text import Text

class Buffer:
    def __init__(self):
        self.texts: list[Text] = []

    def add(self, text_obj: Text):
        self.texts.append(text_obj)

    def get(self, index: int) -> Text:
        if index < 0 or index >= len(self.texts):
            raise IndexError("Invalid index")
        return self.texts[index]

    def update(self, index: int, text_obj: Text) -> None:
        self.texts[index] = text_obj

    def all_strings(self) -> list[str]:
        return [
            f"{i}. {t.text} - rot type: {t.rot_type}, {t.status}"
            for i, t in enumerate(self.texts, start=1)
        ]

    def to_dict_list(self) -> list[dict]:
        return [asdict(text_obj) for text_obj in self.texts]

    def from_dict_list(self, data) -> None:
        self.texts = [Text(**d) for d in data]