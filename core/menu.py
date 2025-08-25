import json
import sys

from core.exceptions import UnsupportedCipherError, EncryptionError, DecryptionError
from core.manager import Manager
from core.file_handler import FileHandler


class Menu:
    def __init__(self):
        self.manager = Manager(file_handler=FileHandler())
        self.options = {
            "1": self.add_text,
            "2": self.show_buffer,
            "3": self.encrypt,
            "4": self.decrypt,
            "5": self.save_to_file,
            "6": self.load_from_file,
            "7": self.exit_program
        }

    def main_menu(self) -> None:
        print("\n--- MENU ---")
        print("1. Add text")
        print("2. Show buffer")
        print("3. Encrypt/")
        print("4. Decrypt")
        print("5. Save to file")
        print("6. Load from file")
        print("7. Exit")

    def run(self) -> None:
        while True:
            self.main_menu()
            choice = input("Choose an option: ")

            match choice:
                case "1":
                    self.add_text()
                case "2":
                    self.show_buffer()
                case "3":
                    self.encrypt()
                case "4":
                    self.decrypt()
                case "5":
                    self.save_to_file()
                case "6":
                    self.load_from_file()
                case "7":
                    self.exit_program()
                case _:
                    print("Invalid choice, choose (1-7)")

    def add_text(self) -> None:
        user_text = input("Enter text: ")
        self.manager.add_text(user_text)
        print(f"Text '{user_text}' has been added to the buffer")

    def show_buffer(self) -> None:
        lines = self.manager.buffer.all_strings()
        if not lines:
            print("Buffer is empty")
        else:
            print("Texts in buffer:")
            for line in lines:
                print(line)

    def encrypt(self) -> None:
        while True:
            self.show_buffer()
            try:
                index = int(input("Select text: ")) - 1
                _ = self.manager.buffer.texts[index]
            except (IndexError, ValueError):
                print(f"Invalid index, try again\n")
                continue

            while True:
                rot_type = input("Enter rot type(rot13, rot47): ")
                try:
                    self.manager.encrypt(index=index, rot_type=rot_type)
                except UnsupportedCipherError as e:
                    print(f"{e}, try again\n")
                    continue
                except EncryptionError as e:
                    print(e)
                    return
                else:
                    print("Text is encrypted")
                    return
    # chyba lepiej zrobić jedną funkcję encrypt_decrypt()
    def decrypt(self) -> None:
        while True:
            self.show_buffer()
            try:
                index = int(input("Select text: ")) - 1
                self.manager.decrypt(index=index)
            except (IndexError, ValueError) as e:
                print(f"Invalid index, try again\n")
            except DecryptionError as e:
                print(e)
            else:
                print("Text is decrypted")
                break

    def save_to_file(self) -> None:
        filename  = input("Enter file name: ")
        file_path = f"data/{filename}.json"

        try:
            self.manager.save_to_file(filename=file_path)
        except OSError as e:
            print(f"Error saving file: {e}")
        else:
            print("File saved")

    def load_from_file(self) -> None:
        filename = input("Enter file name: ")
        file_path = f"data/{filename}.json"

        try:
            self.manager.load_from_file(filename=file_path)
        except FileNotFoundError:
            print("File not found")
        except json.JSONDecodeError:
            print("File corrupted or invalid JSON")
        else:
            print("File loaded")

    def exit_program(self) -> None:
        print("Good bye!")
        sys.exit(0)



