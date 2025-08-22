import sys

from core.constans import STATUS_DECRYPTED, STATUS_ENCRYPTED
from core.manager import Manager


class Menu:
    def __init__(self):
        self.manager = Manager()
        self.options = {
            "1": self.add_text_option,
            "2": self.show_buffer_option,
            "3": self.encrypt_option,
            "4": self.decrypt_option,
            "5": self.save_to_file_option,
            "6": self.load_from_file_option,
            "7": self.exit_program
        }

    def run(self) -> None:
        while True:
            print("\n--- MENU ---")
            print("1. Add text")
            print("2. Show buffer")
            print("3. Encrypt")
            print("4. Decrypt")
            print("5. Save to file")
            print("6. Load from file")
            print("7. Exit")
            choice = input("Enter option: ")

            match choice:
                case "1":
                    self.add_text_option()
                case "2":
                    self.show_buffer_option()
                case "3":
                    self.encrypt_option()
                case "4":
                    self.decrypt_option()
                case "5":
                    self.save_to_file_option()
                case "6":
                    self.load_from_file_option()
                case "7":
                    self.exit_program()

    def add_text_option(self) -> None:
        user_text = input("Enter text: ")
        self.manager.add_text(user_text)
        print(f"Text '{user_text}' has been added to the buffer")

    def show_buffer_option(self, status_filter=None) -> None:
        lines = self.manager.get_buffer_strings(status_filter=status_filter)
        if not lines:
            print("Buffer is empty")
        else:
            print("Texts in buffer:")
            for line in lines:
                print(line)

    def encrypt_option(self) -> None:
        self.show_buffer_option(status_filter=STATUS_DECRYPTED)
        index = int(input("Select text: ")) - 1
        rot_type = input("Enter rot type(rot13, rot47): ")

        self.manager.encrypt(index=index, rot_type=rot_type)
        print("Text is encrypted")

    def decrypt_option(self) -> None:
        self.show_buffer_option(status_filter=STATUS_ENCRYPTED)
        index = int(input("Select text: ")) - 1

        self.manager.decrypt(index=index)
        print("Text is decrypted")

    def save_to_file_option(self) -> None:
        filename  = input("Enter file name: ")
        file_path = f"data/{filename}.json"
        self.manager.save_to_file(filename=file_path)
        print("File saved")

    def load_from_file_option(self) -> None:
        filename = input("Enter file name: ")
        file_path = f"data/{filename}.json"
        self.manager.load_from_file(filename=file_path)
        print("File loaded")

    def exit_program(self) -> None:
        print("Good bye!")
        sys.exit(0)



