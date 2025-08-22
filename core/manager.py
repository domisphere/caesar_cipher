from core.cipher import Cipher
from core.file_handler import FileHandler
from core.text import Text


class Manager:
    def __init__(self):
        self.buffer =  []
        self.file_handler = FileHandler()
        self.cipher = Cipher()
        self.cipher_map = {"rot13": self.cipher.rot13, "rot47": self.cipher.rot47}

    def add_text(self, user_text):
        text_obj = Text(text=user_text, rot_type="", status="decrypted")
        self.buffer.append(text_obj)
        print("Text has been added to the buffer")

    def encrypt(self, index, rot_type):
        text_object = self.buffer[index]

        new_text_obj = self.cipher_map[rot_type](text_object)
        self.buffer[index] = new_text_obj
        print(f"Text {text_object.text} is {new_text_obj.status}")

    def decrypt(self, index):
        text_object = self.buffer[index]

        new_text_obj = self.cipher_map[text_object.rot_type](text_object)
        new_text_obj.rot_type = ""
        self.buffer[index] = new_text_obj
        print(f"Text {text_object.text} is {new_text_obj.status}")

    def show_buffer(self, status_filter=None):
        print("Texts in buffer:")
        for index, text_obj in enumerate(self.buffer, start=1):
            if status_filter is None or text_obj.status == status_filter:
                print(f"{index}. {text_obj.text} - rot type: {text_obj.rot_type}, {text_obj.status}")

    def save_to_file(self, filename):
        self.file_handler.save_to_file(filename, self.buffer)

    def load_from_file(self, filename):
        self.buffer = self.file_handler.load_from_file(filename)



