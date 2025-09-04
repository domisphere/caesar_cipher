import pytest

from core.buffer import Buffer
from core.exceptions import EmptyBufferError
from core.text import Text


@pytest.fixture
def sample_text():
    return Text(text="Dominik", rot_type="rot13", status="decrypted")


@pytest.fixture
def empty_buffer():
    return Buffer()


@pytest.fixture
def filled_buffer(sample_text):
    buffer = Buffer()
    buffer.add(sample_text)
    return buffer


def test_add_text_object_to_empty_buffer(empty_buffer, sample_text):
    empty_buffer.add(sample_text)
    assert empty_buffer.texts == [sample_text]


def test_get_correct_object_when_index_valid(filled_buffer, sample_text):
    result = filled_buffer.get(0)
    assert result == sample_text


def test_should_raise_exception_when_index_invalid(filled_buffer):
    with pytest.raises(IndexError):
        filled_buffer.get(1)


def test_update_object_at_given_index(filled_buffer):
    filled_buffer.update(0, Text(text="Klaudia", rot_type="rot47", status="encrypted"))
    assert filled_buffer.texts == [Text(text="Klaudia", rot_type="rot47", status="encrypted")]


def test_return_formatted_list_when_buffer_has_one_item(filled_buffer):
    assert filled_buffer.all_strings() == ['1. Dominik - rot type: rot13, decrypted']


def test_should_raise_exception_when_buffer_is_empty(empty_buffer):
    with pytest.raises(EmptyBufferError):
        empty_buffer.all_strings()


def test_text_obj_converted_to_dict_list(filled_buffer):
    assert filled_buffer.to_dict_list() == [{'text': 'Dominik', 'rot_type': 'rot13', 'status': 'decrypted'}]


def test_convert_from_dict_list(empty_buffer):
    dicts_list = [{'text': 'Dominik', 'rot_type': 'rot13', 'status': 'decrypted'}]
    empty_buffer.from_dict_list(dicts_list)
    assert empty_buffer.texts == [Text(text='Dominik', rot_type='rot13', status='decrypted')]


def test_round_trip_conversion(filled_buffer, empty_buffer):
    data = filled_buffer.to_dict_list()
    empty_buffer.from_dict_list(data)
    assert empty_buffer.texts == filled_buffer.texts










