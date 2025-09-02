from core.cipher import cipher_factory
from core.constans import STATUS_DECRYPTED, STATUS_ENCRYPTED
from core.text import Text
from core.exceptions import UnsupportedCipherError



class Manager:
    def __init__(self, buffer, file_handler):
        self.buffer =  buffer
        self.file_handler = file_handler

    def add_text(self, user_text: str) -> None:
        text_obj = Text(text=user_text, rot_type="", status=STATUS_DECRYPTED)
        self.buffer.add(text_obj)

    def process_cipher(self, index, rot_type):
        text_obj = self.buffer.get(index=index)

        cipher = cipher_factory(rot_type=rot_type)

        if text_obj.rot_type != rot_type and text_obj.rot_type != "":
            raise UnsupportedCipherError(f"Unsupported rot type: {rot_type}")

        if text_obj.status == STATUS_DECRYPTED:
            new_text_obj = cipher.process(text_obj=text_obj, rot_type=rot_type, status=STATUS_ENCRYPTED)
        elif text_obj.status == STATUS_ENCRYPTED:
            new_text_obj = cipher.process(text_obj=text_obj, rot_type="", status=STATUS_DECRYPTED)

        self.buffer.update(index=index, text_obj=new_text_obj)

        return new_text_obj.status

    def save_to_file(self, filename: str) -> None:
        filename =  f"data/{filename}.json"
        self.file_handler.save_to_file(filename, self.buffer.to_dict_list())

    def load_from_file(self, filename: str) -> None:
        filename = f"data/{filename}.json"
        loaded_data = self.file_handler.load_from_file(filename)

        self.buffer.from_dict_list(loaded_data)



