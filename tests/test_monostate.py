from threading import Lock, Thread
from time import sleep
import pytest
from patterns.creational.monostate.state_manager import StateManager


class TestMonostate:

  def test_instantiation(self):
    instance1 = StateManager()
    instance2 = StateManager()

    assert instance1 != instance2
    assert id(instance1.history) == id(instance2.history)
    assert id(instance1.__dict__) == id(instance2.__dict__)

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

    assert instance1.history == instance2.history

    instance2.undo()
    instance1.add_state("State 3")

    assert instance1.history == instance2.history == ["State 1", "State 3"]

    instance1.clear()

  def test_multithreading(self):
    """Runs multiple locked threads that call the Singleton"""

    def add_app_state(value: str, lock: Lock):
      with lock:
        app = StateManager()
        app.add_state(value)

        if value == "State 2":
          sleep(1)
          app.undo()

    lock = Lock()
    threads = [
        Thread(target=add_app_state, args=(f"State {i}", lock))
        for i in range(1, 5)
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
