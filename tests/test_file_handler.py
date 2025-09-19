import json

import pytest

from src.file_handler import FileHandler


@pytest.fixture
def file_handler():
    return FileHandler()


class TestFileHandler:
    def test_save_to_file_writes_json_content(self, tmp_path, file_handler):
        filename = tmp_path / "buffer.json"
        buffer_data = [
            {"text": "Uryyb", "rot_type": "rot13", "status": "encrypted"},
            {"text": "World", "rot_type": "", "status": "decrypted"},
        ]

        file_handler.save_to_file(str(filename), buffer_data)

        saved_content = filename.read_text()

        assert saved_content == json.dumps(buffer_data, indent=4)

    def test_load_from_file_returns_parsed_json(self, tmp_path, file_handler):
        filename = tmp_path / "buffer.json"
        buffer_data = [
            {"text": "Uryyb", "rot_type": "rot47", "status": "encrypted"},
        ]
        filename.write_text(json.dumps(buffer_data))

        loaded_data = file_handler.load_from_file(str(filename))

        assert loaded_data == buffer_data

    def test_load_from_file_missing_file_raises_error(self, tmp_path, file_handler):
        filename = tmp_path / "missing.json"

        with pytest.raises(FileNotFoundError):
            file_handler.load_from_file(str(filename))

    def test_load_from_file_raises_on_invalid_json(self, tmp_path, file_handler):
        broken_file = tmp_path / "broken.json"
        broken_file.write_text('{"invalid_json"}')

        with pytest.raises(json.JSONDecodeError):
            file_handler.load_from_file(str(broken_file))
