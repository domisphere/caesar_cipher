from core.cipher import Cipher
from core.constans import STATUS_DECRYPTED, ROT13, ROT47, STATUS_ENCRYPTED
from core.file_handler import FileHandler
from core.text import Text


class Manager:
    def __init__(self):
        self.buffer =  []
        self.file_handler = FileHandler()
        self.cipher = Cipher()
        self.cipher_map = {ROT13: self.cipher.rot13, ROT47: self.cipher.rot47}

    def add_text(self, user_text: str) -> None:
        text_obj = Text(text=user_text, rot_type="", status=STATUS_DECRYPTED)
        self.buffer.append(text_obj)

    def encrypt(self, index: int, rot_type: str) -> None:
        if index < 0 or index >= len(self.buffer):
            raise IndexError("Invalid text index")

        if rot_type not in self.cipher_map:
            raise ValueError(f"Unsupported cipher type: {rot_type}")

        text_object = self.buffer[index]

        if text_object.status == STATUS_ENCRYPTED:
            raise TypeError("Text is already encrypted")

        new_text_obj = self.cipher_map[rot_type](text_object)
        self.buffer[index] = new_text_obj

    def decrypt(self, index: int) -> None:
        text_object = self.buffer[index]

        new_text_obj = self.cipher_map[text_object.rot_type](text_object)
        self.buffer[index] = new_text_obj
        return text_object

    def get_buffer_strings(self) -> list[str]:
        lines = []
        for index, text_obj in enumerate(self.buffer, start=1):
            line = f"{index}. {text_obj.text} - rot type: {text_obj.rot_type}, {text_obj.status}"
            lines.append(line)
        return lines

    def save_to_file(self, filename: str) -> None:
        self.file_handler.save_to_file(filename, self.buffer)

    def load_from_file(self, filename: str) -> None:
        self.buffer = self.file_handler.load_from_file(filename)



