from dataclasses import asdict

from core.cipher import cipher_factory
from core.constans import STATUS_DECRYPTED, STATUS_ENCRYPTED
from core.text import Text
from core.exceptions import EncryptionError, DecryptionError
from core.buffer import Buffer


class Manager:
    def __init__(self, file_handler):
        self.buffer =  Buffer()
        self.file_handler = file_handler

    def add_text(self, user_text: str) -> None:
        text_obj = Text(text=user_text, rot_type="", status=STATUS_DECRYPTED)
        self.buffer.add(text_obj)

    def process(self, index, rot_type):
        text_obj = self.buffer.get(index=index)

        cipher = cipher_factory(rot_type=rot_type)

        if text_obj.status == STATUS_ENCRYPTED:
            new_text_obj = cipher.process(text_obj=text_obj, process_type="decrypted")
        elif text_obj.status == STATUS_DECRYPTED:
            new_text_obj = cipher.process(text_obj=text_obj, process_type="encrypted")

        self.buffer.update(index=index, text_obj=new_text_obj)




    # def encrypt(self, index: int, rot_type: str) -> None:
    #     text_obj = self.buffer.get(index=index)
    #
    #     if text_obj.status == STATUS_ENCRYPTED:
    #         raise EncryptionError(f"Text '{text_obj.text}' is already encrypted")
    #
    #     cipher = cipher_factory(rot_type=rot_type)
    #     new_text_obj = cipher.encrypt(text_obj)
    #
    #     self.buffer.update(index=index, text_obj=new_text_obj)
    #
    # def decrypt(self, index: int) -> None:
    #     text_obj = self.buffer.get(index=index)
    #
    #     if text_obj.status == STATUS_DECRYPTED:
    #         raise DecryptionError(f"Text '{text_obj.text}' is already decrypted")
    #
    #     cipher = cipher_factory(text_obj.rot_type)
    #     new_text_obj = cipher.decrypt(text_obj)
    #
    #     self.buffer.update(index=index, text_obj=new_text_obj)

    def save_to_file(self, filename: str) -> None:
        self.file_handler.save_to_file(filename, self.buffer.to_dict_list())

    def load_from_file(self, filename: str) -> None:
        loaded_data = self.file_handler.load_from_file(filename)

        self.buffer.from_dict_list(loaded_data)



