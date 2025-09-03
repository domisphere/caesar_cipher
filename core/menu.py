import json
import sys

from core.exceptions import UnsupportedCipherError, EmptyBufferError
from core.manager import Manager
from core.file_handler import FileHandler
from core.buffer import Buffer


class Menu:
    def __init__(self):
        self.manager = Manager(buffer=Buffer(), file_handler=FileHandler())
        self.options = {
            "1": self.add_text,
            "2": self.show_buffer,
            "3": self.encrypt_decrypt,
            "4": self.save_to_file,
            "5": self.load_from_file,
            "6": self.exit_program
        }

    def main_menu(self) -> None:
        print("\n--- MENU ---")
        print("1. Add text")
        print("2. Show buffer")
        print("3. Encrypt/Decrypt")
        print("4. Save to file")
        print("5. Load from file")
        print("6. Exit")

    def run(self) -> None:
        while True:
            self.main_menu()
            choice = input("Choose an option: ")

            action = self.options.get(choice)
            if action:
                action()
            else:
                print("Invalid choice, choose (1-6)")

    def add_text(self) -> None:
        user_text = input("Enter text: ")
        self.manager.add_text(user_text)
        print(f"Text '{user_text}' has been added to the buffer")

    def show_buffer(self) -> bool:
        try:
            lines = self.manager.buffer.all_strings()
            print("Texts in buffer:")
            for line in lines:
                print(line)
            return True
        except EmptyBufferError as e:
            print(e)
            return False

    def encrypt_decrypt(self) -> None:
        while True:
            if not self.show_buffer():
                return

            try:
                index = int(input("Select text: ")) - 1
                _ = self.manager.buffer.get(index)
            except (ValueError, IndexError):
                print("Invalid index, try again\n")
                continue

            rot_type = input("Enter rot type(rot13, rot47): ")
            try:
                status = self.manager.process_cipher(index=index, rot_type=rot_type)
            except UnsupportedCipherError as e:
                print(f"{e}, try again\n")
                continue
            else:
                print(f"Text is {status}")
                return

    def save_to_file(self) -> None:
        filename  = input("Enter file name: ")

        try:
            self.manager.save_to_file(filename=filename)
        except OSError as e:
            print(f"Error saving file: {e}")
        else:
            print("File saved")

    def load_from_file(self) -> None:
        filename = input("Enter file name: ")

        try:
            self.manager.load_from_file(filename=filename)
        except FileNotFoundError:
            print("File not found")
        except json.JSONDecodeError:
            print("File corrupted or invalid JSON")
        else:
            print("File loaded")

    def exit_program(self) -> None:
        print("Good bye!")
        sys.exit(0)



