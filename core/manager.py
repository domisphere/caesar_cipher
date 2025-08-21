from cipher import Cipher
from file_handler import FileHandler
from text import Text


class Manager:
    def __init__(self):
        self.buffer =  []
        self.cipher = Cipher()
        self.file_handler = FileHandler()

    def add_text(self, user_text):
        text_obj = Text(text=user_text, rot_type="rot13", status="decrypted")
        self.buffer.append(text_obj)
        print("Text has been added to the buffer")

    def encrypt_decrypt(self, index):
        text_object = self.buffer[index]
        cipher_map = {"rot13": self.cipher.rot13, "rot47": self.cipher.rot47}

        new_text_obj = cipher_map[text_object.rot_type](text_object)
        self.buffer[index] = new_text_obj
        print(f"Text {text_object.text} is {new_text_obj.status}")

    def show_buffer(self):
        print("Texts in buffer:")
        for index, text_obj in enumerate(self.buffer, start=1):
            print(f"{index}. {text_obj.text} - rot type: {text_obj.rot_type}, {text_obj.status}")

    def save_to_file(self, filename):
        self.file_handler.save_to_file(filename, self.buffer)

    def load_from_file(self, filename):
        self.buffer = self.file_handler.load_from_file(filename)



