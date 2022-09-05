from threading import Thread
from time import sleep
import pytest
from patterns.creational.singleton.state_manager import StateManager, thread_lock


class TestSingleton:

  @pytest.fixture
  def registry(self):
    """Initialize all image prototypes."""

  def test_instantiation(self):
    instance1 = StateManager()
    instance2 = StateManager()
    assert instance1 == instance2
    instance1.clear()

  def test_state_undo_and_redo(self):
    instance = StateManager()
    instance.add_state("State 1")
    instance.add_state("State 2")
    assert instance.current_state == "State 2"
    assert instance.history == ["State 1", "State 2"]
    assert instance.future == []

    instance.undo()
    assert instance.current_state == "State 1"
    assert instance.history == ["State 1"]
    assert instance.future == ["State 2"]

    instance.redo()
    assert instance.current_state == "State 2"
    assert instance.history == ["State 1", "State 2"]
    assert instance.future == []
    instance.clear()

  def test_threading_locking(self):
    instance1 = StateManager()
    instance2 = StateManager()
    instance1.add_state("State 1")
    instance2.add_state("State 2")
    instance2.undo()
    instance1.add_state("State 3")
    assert instance1.history == instance2.history == ["State 1", "State 3"]
    instance1.clear()

  def test_multithreading(self):
    """Runs multiple locked threads that call the Singleton"""

    @thread_lock()
    def add_app_state(value: str):
      app = StateManager()
      app.add_state(value)

      if value == "State 2":
        sleep(1)
        app.undo()

    threads = [
        Thread(target=add_app_state, args=(f"State {i}",)) for i in range(1, 5)
    ]

    for thread in threads:
      thread.start()

    for thread in threads:
      thread.join()

    app = StateManager()
    assert app.history == ["State 1", "State 3", "State 4"]
    app.clear()


if __name__ == "__main__":
  pytest.main([__file__])
