import pytest

from patterns.behavioral.mediator.group_chat import Database, MessengerFactory, User


class TestMediator:

  @pytest.fixture
  def database(self):
    factory = MessengerFactory()
    return Database(factory)

  @pytest.fixture
  def friends(self, database: Database):
    return [database.new_user(f"Friend {i}") for i in range(1, 5)]

  def test_add_participant(self, database: Database, friends: list[User]):
    chat = database.new_chat("Friend Chat")
    chat.add_participant(friends[0])
    assert chat.participants == [friends[0]]

  def test_duplicate_participants(self, database: Database,
                                  friends: list[User]):
    chat = database.new_chat("Friend Chat")
    chat.add_participant(friends[0])
    assert chat.participants == [friends[0]]
    chat.add_participant(friends[0])
    assert chat.participants == [friends[0]]

  def test_chat(self, database: Database, friends: list[User]):
    chat = database.new_chat("Friend Chat")

    for friend in friends:
      chat.add_participant(friend)

    friends[0].send_group_message("Message 1")

    for i in range(len(friends)):
      assert friends[i].display_messages() == "Friend 1: Message 1"

    friends[1].send_group_message("Message 2")

    for i in range(len(friends)):
      assert friends[i].display_messages(
      ) == "Friend 1: Message 1\nFriend 2: Message 2"


if __name__ == "__main__":
  pytest.main([__file__])
