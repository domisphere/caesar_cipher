from unittest.mock import Mock

import pytest

from src.cipher import Cipher, CipherRot13, CipherRot47, cipher_factory
from src.constants import ROT13, ROT47, STATUS_DECRYPTED, STATUS_ENCRYPTED
from src.exceptions import UnsupportedCipherError
from src.text import Text


@pytest.fixture
def input_text():
    return Text(text="Hello", rot_type=ROT13, status=STATUS_DECRYPTED)


@pytest.fixture
def cipher_rot13():
    return CipherRot13()


@pytest.fixture
def cipher_rot47():
    return CipherRot47()


class TestCipherBase:
    def test_cipher_base_raise_not_implemented_error_when_called(self, input_text):
        class DummyCipher(Cipher):
            def cipher(self, text_obj):
                return super().cipher(text_obj)

        dummy = DummyCipher()
        with pytest.raises(NotImplementedError):
            dummy.cipher(input_text)

    def test_process_delegates_and_wraps_result(self, cipher_rot13, input_text):
        cipher_rot13.cipher = Mock(return_value="MOCKED_RESULT")
        result = cipher_rot13.process(text_obj=input_text, rot_type=ROT47, status=STATUS_ENCRYPTED)

        cipher_rot13.cipher.assert_called_once_with(input_text)
        assert result.text == "MOCKED_RESULT"
        assert result.rot_type == ROT47
        assert result.status == STATUS_ENCRYPTED
        assert result is not input_text
        assert isinstance(result, Text)

    def test_process_does_not_mutate_input(self, cipher_rot13, input_text):
        original = (input_text.text, input_text.rot_type, input_text.status)
        result = cipher_rot13.process(text_obj=input_text, rot_type=ROT13, status=STATUS_ENCRYPTED)

        assert (input_text.text, input_text.rot_type, input_text.status) == original
        assert result is not input_text

    def test_process_propagates_cipher_exception(self, cipher_rot13, input_text):
        cipher_rot13.cipher = Mock(side_effect=ValueError("Boom"))

        with pytest.raises(ValueError) as e:
            cipher_rot13.process(text_obj=input_text, rot_type=ROT47, status=STATUS_ENCRYPTED)

        assert "Boom" in str(e.value)

    def test_process_handles_empty_text(self, cipher_rot13):
        input_text = Text(text="", rot_type=ROT13, status=STATUS_DECRYPTED)
        result = cipher_rot13.process(text_obj=input_text, rot_type=ROT13, status=STATUS_ENCRYPTED)

        assert result.text == ""
        assert result.rot_type == ROT13
        assert result.status == STATUS_ENCRYPTED
        assert result is not input_text

    @pytest.mark.parametrize(
        "rot_type, status",
        [
            (ROT13, STATUS_ENCRYPTED),
            (ROT47, STATUS_DECRYPTED),
            (ROT13, "custom"),
        ],
    )
    def test_process_sets_provided_metadata(self, cipher_rot13, rot_type, status):
        cipher_rot13.cipher = Mock(return_value="OK")
        input_text = Text(text="X", rot_type=ROT47, status="something_else")
        result = cipher_rot13.process(text_obj=input_text, rot_type=rot_type, status=status)

        assert result.text == "OK"
        assert result.rot_type == rot_type
        assert result.status == status


class TestCipherRot13:
    def test_rot13_encrypt_known_case(self, cipher_rot13, input_text):
        result = cipher_rot13.cipher(text_obj=input_text)

        assert result == "Uryyb"

    def test_rot13_double_encrypt_returns_original(self, cipher_rot13, input_text):
        once = cipher_rot13.cipher(input_text)
        twice = cipher_rot13.cipher(
            text_obj=Text(text=once, rot_type=ROT13, status=STATUS_DECRYPTED)
        )

        assert twice == input_text.text

    def test_rot13_ignores_non_alphabetic_characters(self, cipher_rot13):
        s = "1234 !?-_"
        result = cipher_rot13.cipher(text_obj=Text(text=s, rot_type=ROT13, status=STATUS_DECRYPTED))

        assert result == s


class TestCipherRot47:
    def test_rot47_double_encrypt_returns_original(self, cipher_rot47):
        original = "Hello! 123 ~>@"
        once = cipher_rot47.cipher(
            text_obj=Text(text=original, rot_type=ROT47, status=STATUS_DECRYPTED)
        )
        twice = cipher_rot47.cipher(
            text_obj=Text(text=once, rot_type=ROT47, status=STATUS_DECRYPTED)
        )

        assert twice == original

    def test_rot47_leaves_non_ascii_33_126_unchanged(self, cipher_rot47):
        s = "ą\n🙂"
        result = cipher_rot47.cipher(text_obj=Text(text=s, rot_type=ROT47, status=STATUS_DECRYPTED))

        assert result == s


class TestCipherFactory:
    def test_returns_cipherrot13_when_rot13_given(self):
        instance = cipher_factory(ROT13)

        assert isinstance(instance, CipherRot13)

    def test_returns_cipherrot47_when_rot47_given(self):
        instance = cipher_factory(ROT47)

        assert isinstance(instance, CipherRot47)

    def test_raises_error_when_rot_type_is_invalid(self):
        with pytest.raises(UnsupportedCipherError):
            cipher_factory("rot99")
