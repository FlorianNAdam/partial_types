from pydantic import BaseModel

from partial_types.pydantic import Partial


class User(BaseModel):
    id: int
    name: str
    email: str


def test_partial_user_all_optional():
    PartialUser = Partial[User]

    # Can create with no fields
    u1 = PartialUser()
    assert u1.id is None
    assert u1.name is None
    assert u1.email is None

    # Can create with some fields
    u2 = PartialUser(name="Alice")
    assert u2.id is None
    assert u2.name == "Alice"
    assert u2.email is None

    # Can create with all fields
    u3 = PartialUser(id=1, name="Bob", email="bob@example.com")
    assert u3.id == 1
    assert u3.name == "Bob"
    assert u3.email == "bob@example.com"
