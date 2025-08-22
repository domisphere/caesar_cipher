from core.constans import STATUS_ENCRYPTED, STATUS_DECRYPTED, ROT13, ROT47
from core.text import Text


class Cipher:

    def rot13(self, text_obj: Text) -> Text:
        new_text = ""

        for char in text_obj.text:
            if "a" <= char <= "z":
                new_text += chr((ord(char) - ord("a") + 13) % 26 + ord("a"))
            elif "A" <= char <= "Z":
                new_text += chr((ord(char) - ord("A") + 13) % 26 + ord("A"))
            else:
                new_text += char

        new_status = STATUS_ENCRYPTED if text_obj.status == STATUS_DECRYPTED else STATUS_DECRYPTED

        return Text(text=new_text, rot_type=ROT13, status=new_status)


    def rot47(self, text_obj: Text) -> Text:
        new_text = ""

        for char in text_obj.text:
            ascii_code = ord(char)
            if 33 <= ascii_code <= 126:
                new_char = chr(33 + ((ascii_code - 33 + 47) % 94))
                new_text += new_char
            else:
                new_text += char

        new_status = STATUS_ENCRYPTED if text_obj.status == STATUS_DECRYPTED else STATUS_DECRYPTED

        return Text(text=new_text, rot_type=ROT47, status=new_status)


