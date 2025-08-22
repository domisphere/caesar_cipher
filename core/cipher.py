from core.text import Text


class Cipher:

    def rot13(self, text_obj):
        new_text = ""

        for char in text_obj.text:
            if "a" <= char <= "z":
                new_text += chr((ord(char) - ord("a") + 13) % 26 + ord("a"))
            elif "A" <= char <= "Z":
                new_text += chr((ord(char) - ord("A") + 13) % 26 + ord("A"))
            else:
                new_text += char

        new_status = "encrypted" if text_obj.status == "decrypted" else "decrypted"

        return Text(text=new_text, rot_type="rot13", status=new_status)


    def rot47(self, text_obj):
        new_text = ""

        for char in text_obj.text:
            ascii_code = ord(char)
            if 33 <= ascii_code <= 126:
                new_char = chr(33 + ((ascii_code - 33 + 47) % 94))
                new_text += new_char

        new_status = "encrypted" if text_obj.status == "decrypted" else "decrypted"

        return Text(text=new_text, rot_type="rot47", status=new_status)


