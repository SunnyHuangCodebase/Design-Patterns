import pytest
from patterns.structural.bridge.webpage import AdminInterface, AdminWebpage, InsufficientPermissions, UserInterface, UserWebpage


class TestBridge:

  @pytest.fixture
  def user_interface(self) -> UserInterface:
    """"""
    return UserInterface()

  @pytest.fixture
  def admin_interface(self) -> AdminInterface:
    """"""
    return AdminInterface()

  def test_user_webpage_and_ui(self, user_interface: UserInterface):
    webpage = UserWebpage(user_interface)
    assert webpage.get_header() == ["Header"]
    assert webpage.get_post() == ["Content", "Read Later"]
    assert webpage.get_comments() == [
        "Comments", "Add Comment", "Reply to Comment"
    ]
    assert webpage.get_footer() == ["Footer"]
    assert webpage.display_webpage() == [
        "Header", "Content", "Read Later", "Comments", "Add Comment",
        "Reply to Comment", "Footer"
    ]

  def test_user_webpage_and_admin_ui(self, admin_interface: AdminInterface):
    with pytest.raises(InsufficientPermissions):
      webpage = UserWebpage(admin_interface)
      assert webpage.get_header() == ["Header"]
      assert webpage.get_post() == ["Content", "Read Later"]
      assert webpage.get_comments() == [
          "Comments", "Add Comment", "Reply to Comment"
      ]
      assert webpage.get_footer() == ["Footer"]

  def test_admin_webpage_and_interface(self, admin_interface: AdminInterface):
    """"""
    webpage = AdminWebpage(admin_interface)
    assert webpage.get_header() == ["Header"]
    assert webpage.get_post() == [
        "Content", "Read Later", "Edit Post", "Delete Post"
    ]
    assert webpage.get_comments() == [
        "Comments", "Add Comment", "Reply to Comment", "Delete Comment"
    ]
    assert webpage.get_footer() == ["Footer"]

  def test_admin_webpage_and_user_ui(self, user_interface: UserInterface):
    """"""
    webpage = AdminWebpage(user_interface)
    assert webpage.get_header() == ["Header"]
    assert webpage.get_post() == ["Content", "Read Later"]
    assert webpage.get_comments() == [
        "Comments", "Add Comment", "Reply to Comment"
    ]
    assert webpage.get_footer() == ["Footer"]


if __name__ == "__main__":
  pytest.main([__file__])
