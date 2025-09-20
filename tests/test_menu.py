import json
from types import SimpleNamespace

import pytest

from src.exceptions import EmptyBufferError, RotTypeMismatchError
from src.menu import Menu


def create_menu_with_manager(manager):
    menu = Menu()
    menu.manager = manager
    return menu


class TestMenu:
    def test_add_text_adds_to_manager_and_prints(self, monkeypatch, capsys):
        recorded = {}

        class StubManager:
            def add_text(self, text):
                recorded["text"] = text

        menu = create_menu_with_manager(StubManager())

        monkeypatch.setattr("builtins.input", lambda _: "Hello")

        menu.add_text()

        captured = capsys.readouterr().out
        assert recorded["text"] == "Hello"
        assert "Text 'Hello' has been added to the buffer" in captured

    def test_main_menu_prints_all_options(self, capsys):
        menu = Menu()

        menu.main_menu()

        captured = capsys.readouterr().out
        assert "--- MENU ---" in captured
        assert "1. Add text" in captured
        assert "6. Exit" in captured

    def test_run_handles_invalid_choice_and_executes_action(self, monkeypatch, capsys):
        menu = Menu()
        called = []

        class StopLoop(Exception):
            pass

        def fake_action():
            called.append(True)
            raise StopLoop

        menu.options["1"] = fake_action

        inputs = iter(["9", "1"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        with pytest.raises(StopLoop):
            menu.run()

        captured = capsys.readouterr().out
        assert "Invalid choice" in captured
        assert called == [True]

    def test_show_buffer_prints_lines_and_returns_true(self, capsys):
        class StubBuffer:
            def all_strings(self):
                return ["first", "second"]

        menu = create_menu_with_manager(SimpleNamespace(buffer=StubBuffer()))

        assert menu.show_buffer() is True

        captured = capsys.readouterr().out
        assert "Texts in buffer:" in captured
        assert "first" in captured
        assert "second" in captured

    def test_show_buffer_handles_empty_buffer_error(self, capsys):
        class StubBuffer:
            def all_strings(self):
                raise EmptyBufferError("Buffer is empty")

        menu = create_menu_with_manager(SimpleNamespace(buffer=StubBuffer()))

        assert menu.show_buffer() is False

        captured = capsys.readouterr().out
        assert "Buffer is empty" in captured

    def test_encrypt_decrypt_happy_path(self, monkeypatch, capsys):
        class StubBuffer:
            def __init__(self):
                self.requested_index = None

            def all_strings(self):
                return ["stored text"]

            def get(self, index):
                self.requested_index = index
                if index != 0:
                    raise IndexError
                return "stored text"

        class StubManager:
            def __init__(self):
                self.buffer = StubBuffer()
                self.process_calls = []

            def process_cipher(self, index, rot_type):
                self.process_calls.append((index, rot_type))
                return SimpleNamespace(status="encrypted")

        menu = create_menu_with_manager(StubManager())

        inputs = iter(["1", "rot13"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        menu.encrypt_decrypt()

        captured = capsys.readouterr().out
        assert menu.manager.buffer.requested_index == 0
        assert menu.manager.process_calls == [(0, "rot13")]
        assert "Text is encrypted" in captured

    def test_encrypt_decrypt_returns_when_buffer_empty(self, monkeypatch):
        class StubManager:
            def __init__(self):
                self.buffer = SimpleNamespace()

        menu = create_menu_with_manager(StubManager())

        monkeypatch.setattr(menu, "show_buffer", lambda: False)

        def fail_input(_):
            raise AssertionError("input should not be called")

        monkeypatch.setattr("builtins.input", fail_input)

        assert menu.encrypt_decrypt() is None

    def test_encrypt_decrypt_retries_on_invalid_index(self, monkeypatch, capsys):
        class StubBuffer:
            def __init__(self):
                self.requested_indices = []

            def all_strings(self):
                return ["stored text"]

            def get(self, index):
                self.requested_indices.append(index)
                return "stored index"

        class StubManager:
            def __init__(self):
                self.buffer = StubBuffer()
                self.process_calls = []

            def process_cipher(self, index, rot_type):
                self.process_calls.append((index, rot_type))
                return SimpleNamespace(status="encrypted")

        menu = create_menu_with_manager(StubManager())

        inputs = iter(["x", "1", "rot13"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        menu.encrypt_decrypt()

        captured = capsys.readouterr().out
        assert "Invalid index, try again" in captured
        assert menu.manager.buffer.requested_indices == [0]
        assert menu.manager.process_calls == [(0, "rot13")]

    def test_encrypt_decrypt_retries_on_process_error(self, monkeypatch, capsys):
        class StubBuffer:
            def __init__(self):
                self.requested_indices = []

            def all_strings(self):
                return ["stored text"]

            def get(self, index):
                self.requested_indices.append(index)
                return "stored text"

        class StubManager:
            def __init__(self):
                self.buffer = StubBuffer()
                self.process_calls = []

            def process_cipher(self, index, rot_type):
                call = (index, rot_type)
                self.process_calls.append(call)
                if len(self.process_calls) == 1:
                    raise RotTypeMismatchError("Mismatch rot type")
                return SimpleNamespace(status="decrypted")

        menu = create_menu_with_manager(StubManager())

        inputs = iter(["1", "rot13", "1", "rot47"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        menu.encrypt_decrypt()

        captured = capsys.readouterr().out
        assert "Mismatch rot type, try again" in captured
        assert "Text is decrypted" in captured
        assert menu.manager.buffer.requested_indices == [0, 0]
        assert menu.manager.process_calls == [(0, "rot13"), (0, "rot47")]

    def test_save_to_file_success(self, monkeypatch, capsys):
        class StubManager:
            def __init__(self):
                self.saved_filename = None

            def save_to_file(self, filename):
                self.saved_filename = filename

        menu = create_menu_with_manager(StubManager())

        monkeypatch.setattr("builtins.input", lambda _: "session1")

        menu.save_to_file()

        captured = capsys.readouterr().out
        assert menu.manager.saved_filename == "session1"
        assert "File saved" in captured

    def test_save_to_file_handles_os_error(self, monkeypatch, capsys):
        class StubManager:
            def save_to_file(self, filename):
                raise OSError("disk full")

        menu = create_menu_with_manager(StubManager())

        monkeypatch.setattr("builtins.input", lambda _: "session1")

        menu.save_to_file()

        captured = capsys.readouterr().out
        assert "Error saving file: disk full" in captured

    def test_load_from_file_success(self, monkeypatch, capsys):
        class StubManager:
            def __init__(self):
                self.loaded_filename = None

            def load_from_file(self, filename):
                self.loaded_filename = filename

        menu = create_menu_with_manager(StubManager())

        monkeypatch.setattr("builtins.input", lambda _: "session1")

        menu.load_from_file()

        captured = capsys.readouterr().out
        assert menu.manager.loaded_filename == "session1"
        assert "File loaded" in captured

    def test_load_from_file_handles_missing_file(self, monkeypatch, capsys):
        class StubManager:
            def load_from_file(self, filename):
                raise FileNotFoundError

        menu = create_menu_with_manager(StubManager())

        monkeypatch.setattr("builtins.input", lambda _: "session1")

        menu.load_from_file()

        captured = capsys.readouterr().out
        assert "File not found" in captured

    def test_load_from_file_handles_json_error(self, monkeypatch, capsys):
        class StubManager:
            def load_from_file(self, filename):
                raise json.JSONDecodeError("msg", "doc", 0)

        menu = create_menu_with_manager(StubManager())

        monkeypatch.setattr("builtins.input", lambda _: "session1")

        menu.load_from_file()

        captured = capsys.readouterr().out
        assert "File corrupted or invalid JSON" in captured

    def test_exit_program_prints_and_exits(self, capsys):
        class StubManager:
            pass

        menu = create_menu_with_manager(StubManager())

        with pytest.raises(SystemExit) as exc:
            menu.exit_program()

        captured = capsys.readouterr().out
        assert "Good bye!" in captured
        assert exc.value.code == 0
