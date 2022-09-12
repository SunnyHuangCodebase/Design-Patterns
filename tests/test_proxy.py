import pytest

from patterns.structural.proxy.user_manager import App, InsufficientPermissions, Log, LoggingUserManager, User, UserManager, UserPermissionLevel


class TestUserManager:

  @pytest.fixture
  def user(self) -> User:
    return User("User", UserPermissionLevel.USER)

  @pytest.fixture
  def admin(self) -> User:
    return User("Admin", UserPermissionLevel.ADMIN)

  @pytest.fixture
  def user_manager(self) -> UserManager:
    return UserManager()

  @pytest.fixture
  def log(self) -> Log:
    return Log()

  @pytest.fixture()
  def logged_user_manager(self, user_manager: UserManager,
                          log: Log) -> LoggingUserManager:
    return LoggingUserManager(user_manager, log)

  @pytest.fixture
  def app(self, user_manager: UserManager) -> App:
    return App(user_manager)

  @pytest.fixture
  def logged_app(self, logged_user_manager: LoggingUserManager):
    return App(logged_user_manager)

  def test_admin_ban_user(self, app: App, admin: User, user: User):
    """Admin bans a user using the regular app."""
    app.ban(admin, user)
    assert user.banned == True
    assert user.inbox.messages[0] == "You have been banned from using the app."

  def test_admin_ban_user_logged(self, logged_app: App, admin: User,
                                 user: User):
    """Admin bans a user using the logged app."""
    logged_app.ban(admin, user)
    assert logged_app.manager.log.history[0] == f"Admin has banned User."
    assert user.banned == True

  def test_user_ban_admin(self, app: App, admin: User, user: User):
    """User should be unable to ban an admin."""
    with pytest.raises(InsufficientPermissions):
      app.ban(user, admin)

  def test_user_ban_admin_logged(self, logged_app: App, admin: User,
                                 user: User):
    """User should be unable to ban an admin."""
    with pytest.raises(InsufficientPermissions):
      logged_app.ban(user, admin)


if __name__ == "__main__":
  pytest.main([__file__])
