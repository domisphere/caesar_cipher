from unittest.mock import Mock

import pytest

from src.cipher import Cipher, CipherRot13, CipherRot47, cipher_factory
from src.constants import ROT13, ROT47, STATUS_DECRYPTED, STATUS_ENCRYPTED
from src.exceptions import UnsupportedCipherError
from src.text import Text


@pytest.fixture
def input_text():
    return Text(text="Hello", rot_type=ROT13, status=STATUS_DECRYPTED)


class TestCipherBase:
    def test_cipher_base_raise_not_implemented_method_when_called(self, input_text):
        class DummyCipher(Cipher):
            def cipher(self, text_obj):
                return super().cipher(text_obj)

        dummy = DummyCipher()
        with pytest.raises(NotImplementedError):
            dummy.cipher(input_text)

    def test_process_delegates_and_wraps_result(self, input_text):
        cipher = CipherRot13()
        cipher.cipher = Mock(return_value="MOCKED_RESULT")
        result = cipher.process(text_obj=input_text, rot_type=ROT47, status=STATUS_ENCRYPTED)

        cipher.cipher.assert_called_once_with(input_text)
        assert result.text == "MOCKED_RESULT"
        assert result.rot_type == ROT47
        assert result.status == STATUS_ENCRYPTED
        assert result is not input_text
        assert isinstance(result, Text)

    def test_process_does_not_mutate_input(self, input_text):
        cipher = CipherRot13()
        original = (input_text.text, input_text.rot_type, input_text.status)
        result = cipher.process(text_obj=input_text, rot_type=ROT13, status=STATUS_ENCRYPTED)

        assert (input_text.text, input_text.rot_type, input_text.status) == original
        assert result is not input_text

    def test_process_propagates_cipher_exception(self, input_text):
        cipher = CipherRot13()
        cipher.cipher = Mock(side_effect=ValueError("Boom"))

        with pytest.raises(ValueError) as e:
            cipher.process(text_obj=input_text, rot_type=ROT47, status=STATUS_ENCRYPTED)

        assert "Boom" in str(e.value)

    def test_process_handles_empty_text(self):
        cipher = CipherRot13()
        input_text = Text(text="", rot_type=ROT13, status=STATUS_DECRYPTED)
        result = cipher.process(text_obj=input_text, rot_type=ROT13, status=STATUS_ENCRYPTED)

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
    def test_process_sets_provided_metadata(self, rot_type, status):
        cipher = CipherRot13()
        cipher.cipher = Mock(return_value="OK")
        input_text = Text(text="X", rot_type=ROT47, status="something_else")
        result = cipher.process(text_obj=input_text, rot_type=rot_type, status=status)

        assert result.text == "OK"
        assert result.rot_type == rot_type
        assert result.status == status


class TestCipherRot13:
    def test_rot13_encrypt_known_case(self, input_text):
        cipher = CipherRot13()
        result = cipher.cipher(input_text)

        assert result == "Uryyb"

    def test_rot13_double_encrypt_returns_original(self, input_text):
        cipher = CipherRot13()
        once = cipher.cipher(input_text)
        twice = cipher.cipher(text_obj=Text(text=once, rot_type=ROT13, status=STATUS_DECRYPTED))

        assert twice == input_text.text

    def test_rot13_ignores_non_alphabetic_characters(self):
        cipher = CipherRot13()
        s = "1234 !?-_"
        result = cipher.cipher(text_obj=Text(text=s, rot_type=ROT13, status=STATUS_DECRYPTED))

        assert result == s


class TestCipherRot47:
    def test_rot47_double_encrypt_returns_original(self):
        cipher = CipherRot47()
        original = "Hello! 123 ~>@"
        once = cipher.cipher(text_obj=Text(text=original, rot_type=ROT47, status=STATUS_DECRYPTED))
        twice = cipher.cipher(text_obj=Text(text=once, rot_type=ROT47, status=STATUS_DECRYPTED))

        assert twice == original

    def test_rot47_leaves_non_ascii_33_126_unchanged(self):
        cipher = CipherRot47()
        s = "ą\n🙂"
        result = cipher.cipher(text_obj=Text(text=s, rot_type=ROT47, status=STATUS_DECRYPTED))

        assert result == s


class TestCipherFactory:
    def test_returns_cipherrot13_when_rot13_given(self):
        cipher = cipher_factory(ROT13)

        assert isinstance(cipher, CipherRot13)

    def test_returns_cipherrot47_when_rot13_given(self):
        cipher = cipher_factory(ROT47)

        assert isinstance(cipher, CipherRot47)

    def test_raises_error_when_rot_type_is_invalid(self):
        with pytest.raises(UnsupportedCipherError):
            cipher_factory("rot99")
