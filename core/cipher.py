from core.constans import STATUS_ENCRYPTED, STATUS_DECRYPTED, ROT13, ROT47
from core.text import Text
from core.exceptions import UnsupportedCipherError

from abc import ABC, abstractmethod


class Cipher(ABC):
    @abstractmethod
    def cipher(self, text_obj: Text) -> str:
        pass

    @abstractmethod
    def process(self, text_obj, process_type):
        pass

    # @abstractmethod
    # def encrypt(self, text_obj: Text) -> Text:
    #     pass
    #
    # @abstractmethod
    # def decrypt(self, text_obj: Text) -> Text:
    #     pass

class CipherRot13(Cipher):
    def cipher(self, text_obj: Text) -> str:
        new_text = ""

        for char in text_obj.text:
            if "a" <= char <= "z":
                new_text += chr((ord(char) - ord("a") + 13) % 26 + ord("a"))
            elif "A" <= char <= "Z":
                new_text += chr((ord(char) - ord("A") + 13) % 26 + ord("A"))
            else:
                new_text += char

        return new_text

    def process(self, text_obj, process_type):
        text = self.cipher(text_obj)

        return Text(text=text, rot_type=ROT13, status=process_type)

    # def encrypt(self, text_obj: Text) -> Text:
    #     text = self.cipher(text_obj)
    #
    #     return Text(text=text, rot_type=ROT13, status=STATUS_ENCRYPTED)
    #
    # def decrypt(self, text_obj: Text) -> Text:
    #     text = self.cipher(text_obj)
    #
    #     return Text(text=text, rot_type=ROT13, status=STATUS_DECRYPTED)


class CipherRot47(Cipher):

    def cipher(self, text_obj: Text) -> str:
        new_text = ""

        for char in text_obj.text:
            ascii_code = ord(char)
            if 33 <= ascii_code <= 126:
                new_char = chr(33 + ((ascii_code - 33 + 47) % 94))
                new_text += new_char
            else:
                new_text += char

        return new_text

    def encrypt(self, text_obj: Text) -> Text:
        text = self.cipher(text_obj)

        return Text(text=text, rot_type=ROT47, status=STATUS_ENCRYPTED)

    def decrypt(self, text_obj: Text) -> Text:
        text = self.cipher(text_obj)

        return Text(text=text, rot_type=ROT47, status=STATUS_DECRYPTED)


def cipher_factory(rot_type: str) -> Cipher:
    if rot_type == ROT13:
        return CipherRot13()
    elif rot_type == ROT47:
        return CipherRot47()
    else:
        raise UnsupportedCipherError(f"Unsupported rot type: {rot_type}")