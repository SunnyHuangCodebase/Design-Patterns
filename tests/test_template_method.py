import textwrap
import pytest
from pytest import CaptureFixture, MonkeyPatch
from patterns.behavioral.template_method.two_factor_authentication import CallAuthenticator, EmailAuthenticator, TextAuthenticator, User


class TestTemplateMethod:

  @pytest.fixture
  def user(self) -> User:
    return User(
        phone="1234567890",
        email="username@email.com",
        two_factor_authentication=True,
    )

  def test_text_authentication(self, user: User, capsys: CaptureFixture[str],
                               monkeypatch: MonkeyPatch):
    authenticator = TextAuthenticator()
    monkeypatch.setattr("builtins.input", lambda: authenticator.code)
    user.confirm_identity(authenticator)
    captured = capsys.readouterr()
    assert authenticator.authorized == True
    assert captured.out == textwrap.dedent(f"""\
      Sent a code to {authenticator.obfuscate_user_info(user)}.
      Successfully logged in!
    """)

  def test_call_authentication(self, user: User, capsys: CaptureFixture[str],
                               monkeypatch: MonkeyPatch):
    authenticator = CallAuthenticator()
    monkeypatch.setattr("builtins.input", lambda: authenticator.code)
    user.confirm_identity(authenticator)
    captured = capsys.readouterr()
    assert authenticator.authorized == True
    assert captured.out == textwrap.dedent(f"""\
      Calling in authentication code to {authenticator.obfuscate_user_info(user)}.
      Successfully logged in!
    """)

  def test_email_authentication(self, user: User, capsys: CaptureFixture[str],
                                monkeypatch: MonkeyPatch):
    authenticator = EmailAuthenticator()
    monkeypatch.setattr("builtins.input", lambda: authenticator.code)
    user.confirm_identity(authenticator)
    captured = capsys.readouterr()
    assert authenticator.authorized == True
    assert captured.out == textwrap.dedent(f"""\
      Sent a code to {authenticator.obfuscate_user_info(user)}.
      Successfully logged in!
    """)

  def test_failed_authentication(self, user: User, capsys: CaptureFixture[str],
                                 monkeypatch: MonkeyPatch):
    authenticator = TextAuthenticator()
    monkeypatch.setattr("builtins.input", lambda: "Wrong code")
    user.confirm_identity(authenticator)
    captured = capsys.readouterr()
    assert authenticator.authorized == False
    assert captured.out == textwrap.dedent(f"""\
      Sent a code to {authenticator.obfuscate_user_info(user)}.
      Please try logging in again!
    """)


if __name__ == "__main__":
  pytest.main([__file__])
