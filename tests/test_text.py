from core.text import Text


def test_create_correct_object():
    obj = Text(text="Dominik", rot_type="rot13", status="decrypted")
    assert obj.text == "Dominik"
    assert obj.rot_type == "rot13"
    assert obj.status == "decrypted"

def test_empty_string():
    obj = Text(text="", rot_type="", status="")
    assert obj.text == ""
    assert obj.rot_type == ""
    assert obj.status == ""


def test_change_attribute():
    obj = Text(text="Dominik", rot_type="rot13", status="decrypted")
    obj.rot_type = "rot47"
    assert obj.rot_type == "rot47"


def test_pass_int_as_attribute():
    obj = Text(text=4, rot_type="rot13", status="decrypted")
    assert obj.text == 4
