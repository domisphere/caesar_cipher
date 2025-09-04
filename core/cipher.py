from abc import ABC, abstractmethod

from core.constants import ROT13, ROT47
from core.exceptions import UnsupportedCipherError
from core.text import Text


class Cipher(ABC):
    @abstractmethod
    def cipher(self, text_obj: Text) -> str:
        raise NotImplementedError

    def process(self, text_obj: Text, rot_type: str, status: str) -> Text:
        transformed = self.cipher(text_obj)

        return Text(text=transformed, rot_type=rot_type, status=status)


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


def cipher_factory(rot_type: str) -> Cipher:
    if rot_type == ROT13:
        return CipherRot13()
    elif rot_type == ROT47:
        return CipherRot47()
    else:
        raise UnsupportedCipherError(f"Unsupported rot type: {rot_type}")
