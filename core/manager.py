from core.cipher import cipher_factory
from core.constants import STATUS_DECRYPTED, STATUS_ENCRYPTED
from core.text import Text
from core.exceptions import RotTypeMismatchError


class Manager:
    def __init__(self, buffer, file_handler):
        self.buffer =  buffer
        self.file_handler = file_handler

    def add_text(self, user_text: str) -> None:
        text_obj = Text(text=user_text, rot_type="", status=STATUS_DECRYPTED)
        self.buffer.add(text_obj)

    def process_cipher(self, index: int, rot_type: str) -> Text:
        text_obj = self.buffer.get(index=index)
        cipher = cipher_factory(rot_type=rot_type)

        if text_obj.status == STATUS_DECRYPTED:
            new_text_obj = cipher.process(text_obj=text_obj, rot_type=rot_type, status=STATUS_ENCRYPTED)

        elif text_obj.status == STATUS_ENCRYPTED:
            if text_obj.rot_type and text_obj.rot_type != rot_type:
                raise RotTypeMismatchError(f"Mismatch rot type: expected {text_obj.rot_type}, got {rot_type}")

            tmp = cipher.process(text_obj=text_obj, rot_type=rot_type, status=STATUS_DECRYPTED)

            new_text_obj = Text(text=tmp.text, rot_type="", status=tmp.status)
        else:
            raise ValueError(f"Unknown status: {text_obj.status}")

        self.buffer.update(index=index, text_obj=new_text_obj)

        return new_text_obj

    def save_to_file(self, filename: str) -> None:
        filename =  f"data/{filename}.json"
        self.file_handler.save_to_file(filename, self.buffer.to_dict_list())

    def load_from_file(self, filename: str) -> None:
        filename = f"data/{filename}.json"
        loaded_data = self.file_handler.load_from_file(filename)

        self.buffer.from_dict_list(loaded_data)



