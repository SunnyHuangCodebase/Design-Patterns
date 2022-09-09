import base64
from hashlib import scrypt
import pytest

from patterns.structural.decorator.password_hasher import Password, SCrypt, BCrypt, hash_password

import bcrypt


class TestDecorator:

  @pytest.fixture
  def password(self):
    return Password('password')

  def test_password(self, password: Password):
    assert password.string == b'password'
    assert password.encoded_string == base64.b64encode(b'password')

  def test_alternate_constructors(self, password: Password):
    password_from_string = Password.from_string("password")
    password_from_bytes = Password.from_bytes(b"password")

    assert password.string == password_from_string.string == password_from_bytes.string

  def test_default_password_hash(self, password: Password):
    bcrypt_password_default = BCrypt(password)
    scrypt_password_default = SCrypt(password)

    assert bcrypt_password_default.rounds == 14
    assert scrypt_password_default.rounds == 14

    bcrypt_password = BCrypt(password, 1)
    scrypt_password = SCrypt(password, 10)

    assert bcrypt_password.rounds == 1
    assert scrypt_password.rounds == 10

  def test_password_hash(self, password: Password):
    bcrypt_password = BCrypt(password)
    scrypt_password = SCrypt(password)

    assert bcrypt.checkpw(password.string, hash_password(bcrypt_password))
    assert hash_password(scrypt_password) == scrypt(password.string,
                                                    salt=scrypt_password.salt,
                                                    n=16384,
                                                    r=8,
                                                    p=1)


if __name__ == "__main__":
  pytest.main([__file__])
