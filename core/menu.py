import sys

from core.manager import Manager


class Menu:
    def __init__(self):
        self.manager = Manager()
        self.options = {
            "1": self.add_text_option,
            "2": self.manager.show_buffer,
            "3": self.encrypt_option,
            "4": self.decrypt_option,
            "5": self.save_to_file_option,
            "6": self.load_from_file_option,
            "7": self.exit_program
        }

    def run(self):
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
                    self.manager.show_buffer()
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

    def add_text_option(self):
        user_text = input("Enter text: ")
        self.manager.add_text(user_text)

    def encrypt_option(self):
        self.manager.show_buffer(status_filter="decrypted")
        index = int(input("Select text: ")) - 1
        rot_type = input("Enter rot type(rot13, rot47): ")

        self.manager.encrypt(index=index, rot_type=rot_type)

    def decrypt_option(self):
        self.manager.show_buffer(status_filter="encrypted")
        index = int(input("Select text: ")) - 1

        self.manager.decrypt(index=index)

    def save_to_file_option(self):
        filename  = input("Enter file name: ")
        file_path = f"data/{filename}.json"
        self.manager.save_to_file(filename=file_path)

    def load_from_file_option(self):
        filename = input("Enter file name: ")
        file_path = f"data/{filename}.json"
        self.manager.load_from_file(filename=file_path)

    def exit_program(self):
        print("Good bye!")
        sys.exit(0)



