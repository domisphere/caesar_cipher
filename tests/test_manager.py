from unittest.mock import Mock

import pytest

from src.buffer import Buffer
from src.constants import ROT13, ROT47, STATUS_DECRYPTED, STATUS_ENCRYPTED
from src.exceptions import RotTypeMismatchError, UnsupportedCipherError
from src.file_handler import FileHandler
from src.manager import Manager
from src.text import Text


@pytest.fixture
def buffer():
    return Buffer()


@pytest.fixture
def file_handler_mock():
    return Mock(spec=FileHandler)


@pytest.fixture
def manager(buffer, file_handler_mock):
    return Manager(buffer=buffer, file_handler=file_handler_mock)


class TestManager:
    def test_add_text_appends_text_to_buffer(self, buffer, manager):
        manager.add_text("Hello")

        assert buffer.texts == [Text(text="Hello", rot_type="", status=STATUS_DECRYPTED)]

    @pytest.mark.parametrize(
        ("rot_type", "plain_text", "expected_cipher"),
        [(ROT13, "Hello", "Uryyb"), (ROT47, "Hello", "w6==@")],
    )
    def test_process_cipher_encrypts_decrypts_text(
        self,
        buffer,
        manager,
        rot_type,
        plain_text,
        expected_cipher,
    ):
        original = Text(text=plain_text, rot_type="", status=STATUS_DECRYPTED)
        buffer.add(original)

        encrypted = manager.process_cipher(index=0, rot_type=rot_type)

        assert encrypted.text == expected_cipher
        assert encrypted.rot_type == rot_type
        assert encrypted.status == STATUS_ENCRYPTED
        assert buffer.get(0) == encrypted
        assert encrypted is not original

        decrypted = manager.process_cipher(index=0, rot_type=rot_type)

        assert decrypted.text == plain_text
        assert decrypted.rot_type == ""
        assert decrypted.status == STATUS_DECRYPTED
        assert buffer.get(0) == decrypted
        assert decrypted is not encrypted

    def test_process_cipher_raises_when_rot_type_mismatch(self, buffer, manager):
        buffer.add(Text(text="Uryyb", rot_type=ROT13, status=STATUS_ENCRYPTED))

        with pytest.raises(RotTypeMismatchError):
            manager.process_cipher(index=0, rot_type=ROT47)

        assert buffer.texts[0] == Text(text="Uryyb", rot_type=ROT13, status=STATUS_ENCRYPTED)

    def test_process_cipher_raises_value_error_for_unknown_status(self, buffer, manager):
        buffer.add(Text(text="Hello", rot_type="", status="unknown"))

        with pytest.raises(ValueError):
            manager.process_cipher(index=0, rot_type=ROT13)

        assert buffer.texts[0] == Text(text="Hello", rot_type="", status="unknown")

    def test_process_cipher_raises_for_unsupported_cipher(self, manager, buffer):
        buffer.add(Text(text="Hello", rot_type="", status=STATUS_DECRYPTED))

        with pytest.raises(UnsupportedCipherError):
            manager.process_cipher(index=0, rot_type="rot99")

        assert buffer.texts[0] == Text(text="Hello", rot_type="", status=STATUS_DECRYPTED)

    def test_save_to_file_passes_serialized_buffer_to_handler(self, file_handler_mock):
        buffer_mock = Mock(spec=Buffer)
        manager = Manager(buffer=buffer_mock, file_handler=file_handler_mock)
        buffer_data = [{"text": "Uryyb", "rot_type": ROT13, "status": STATUS_ENCRYPTED}]
        buffer_mock.to_dict_list.return_value = buffer_data

        manager.save_to_file("filename")

        buffer_mock.to_dict_list.assert_called_once_with()
        file_handler_mock.save_to_file.assert_called_once_with("data/filename.json", buffer_data)

    def test_load_from_file_populates_buffer_with_loaded_data(self, file_handler_mock):
        buffer_mock = Mock(spec=Buffer)
        manager = Manager(buffer=buffer_mock, file_handler=file_handler_mock)
        loaded_data = [{"text": "Hello", "rot_type": "", "status": STATUS_DECRYPTED}]
        file_handler_mock.load_from_file.return_value = loaded_data

        manager.load_from_file("filename")

        file_handler_mock.load_from_file.assert_called_once_with("data/filename.json")
        buffer_mock.from_dict_list.assert_called_once_with(loaded_data)
