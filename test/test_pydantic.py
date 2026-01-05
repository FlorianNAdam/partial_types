from typing import Optional, TypedDict, get_args

import pytest
from pydantic import BaseModel

from partial_types.pydantic import Partial

# --- Sample models for testing ---


class User(BaseModel):
    id: int
    name: str
    email: Optional[str] = None  # already optional


class Config(TypedDict):
    host: str
    port: int
    user: Optional[str]


# --- Import Partial from your module ---
# from your_module import Partial  # replace with actual import

# -------------------
# Tests for BaseModel
# -------------------


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


def test_partial_user_dict_output():
    PartialUser = Partial[User]
    u = PartialUser(id=42)
    data = u.model_dump()
    assert data["id"] == 42
    assert data["name"] is None
    assert data["email"] is None


# ----------------------
# Tests for TypedDict
# ----------------------


def test_partial_config_all_optional():
    PartialConfig = Partial[Config]

    # Can create with no fields
    c1 = PartialConfig()
    assert c1.host is None
    assert c1.port is None
    assert c1.user is None

    # Can create with some fields
    c2 = PartialConfig(host="localhost")
    assert c2.host == "localhost"
    assert c2.port is None
    assert c2.user is None

    # Can create with all fields
    c3 = PartialConfig(host="127.0.0.1", port=8080, user="admin")
    assert c3.host == "127.0.0.1"
    assert c3.port == 8080
    assert c3.user == "admin"


def test_partial_config_dict_output():
    PartialConfig = Partial[Config]
    c = PartialConfig(host="example.com", port=80)
    data = c.model_dump()
    assert data["host"] == "example.com"
    assert data["port"] == 80
    assert data["user"] is None


def test_partial_typed_dict_preserves_optional():
    PartialConfig = Partial[Config]
    c = PartialConfig()

    typ = type(c).model_fields["user"].annotation
    args = get_args(typ)
    # The 'user' field was already Optional in TypedDict
    assert type(None) in args  # still optional


# ----------------------
# Run all tests
# ----------------------


def func() -> Partial[Config]:
    return Partial[Config]()


if __name__ == "__main__":
    pytest.main([__file__])
