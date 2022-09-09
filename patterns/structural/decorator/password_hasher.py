"""Password Hasher uses the Decorator design pattern to hash passwords.

Example Usage:
  password = Password("keep this password secret!")
  bcrypt_password = BCrypt(password)
  hash_password(bcrypt_password)

Disclaimer: This module is for educational purposes only!
Python has a built-in @decorator implementation.
Do not use the following code to store real users' passwords in production.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
import base64
from hashlib import scrypt
import os
import bcrypt


class Password:
  _string: bytes

  def __init__(self, string: str = ""):
    self._string = bytes(string, "UTF-8")

  @property
  def string(self):
    return self._string

  @property
  def encoded_string(self):
    return base64.b64encode(self._string)

  @classmethod
  def from_string(cls, string: str) -> Password:
    """Alternate string constructor using a different byte conversion method."""
    password = super().__new__(cls)
    password._string = string.encode("UTF-8")
    return password

  @classmethod
  def from_bytes(cls, byte_string: bytes) -> Password:
    """Alternate byte constructor.
    
    Example 1: b"Password"
    Example 2: "Password".encode("UTF-8")
    """

    password = super().__new__(cls)
    password._string = byte_string
    return password


class PasswordHash(ABC):
  """Abstract password hashing algorithm."""
  password: Password
  salt: bytes

  def __init__(self, password: Password, rounds: int = 14):
    self.password = password
    self.rounds = rounds

  @abstractmethod
  def generate_salt(self) -> bytes:
    """Generate a salt to prevent rainbow table lookups."""

  @abstractmethod
  def hashed_password(self) -> bytes:
    """Cryptographic function to generate more secure passwords."""


class BCrypt(PasswordHash):
  """Hashes a password using the bcrypt module."""

  def generate_salt(self, rounds: int = 0) -> bytes:
    self.salt = bcrypt.gensalt(rounds or self.rounds)
    return self.salt

  def hashed_password(self) -> bytes:
    """Returns hashed password using bcrypt."""
    return bcrypt.hashpw(self.password.string, self.generate_salt())


class SCrypt(PasswordHash):
  """Hashes a pasword using hashlib.scrypt."""

  def generate_salt(self, rounds: int = 0) -> bytes:
    self.salt = os.urandom(rounds or self.rounds)
    return self.salt

  def hashed_password(self) -> bytes:
    """Returned hashed password using scrypt"""
    return scrypt(self.password.string,
                  salt=self.generate_salt(),
                  n=16384,
                  r=8,
                  p=1)


def hash_password(hash: PasswordHash) -> bytes:
  """Returned hashed password."""
  return hash.hashed_password()
