import pytest

from patterns.behavioral.memento.task_app import TaskApp, TaskManager, TaskMemento


class TestMemento:

  @pytest.fixture
  def app(self) -> TaskApp:
    return TaskApp()

  @pytest.fixture
  def task_manager(self, app: TaskApp) -> TaskManager:
    return TaskManager(app)

  def test_create_task(self, app: TaskApp, task_manager: TaskManager):
    task_manager.backup()
    app.add_task("Task 1")
    expected_history = [TaskMemento({}, {}, 0)]

    assert app.current_state() == TaskMemento({1: 'Task 1'}, {}, 1)
    assert task_manager.history == expected_history
    assert task_manager.undo_history == []

  def test_complete_task(self, app: TaskApp, task_manager: TaskManager):
    task_manager.backup()
    app.add_task("Task 1")
    expected_history = [TaskMemento({}, {}, 0)]

    task_manager.backup()
    app.complete_task(1)
    expected_history.append(TaskMemento({1: "Task 1"}, {}, 1))

    assert app.current_state() == TaskMemento({}, {1: "Task 1"}, 1)
    assert task_manager.history == expected_history
    assert task_manager.undo_history == []

  def test_delete_task(self, app: TaskApp, task_manager: TaskManager):
    task_manager.backup()
    app.add_task("Task 1")
    expected_history = [TaskMemento({}, {}, 0)]

    task_manager.backup()
    app.remove_task(1)
    expected_history.append(TaskMemento({1: 'Task 1'}, {}, 1))

    assert app.current_state() == TaskMemento({}, {}, 1)
    assert task_manager.history == expected_history
    assert task_manager.undo_history == []

  def test_undo(self, app: TaskApp, task_manager: TaskManager):
    task_manager.backup()
    app.add_task("Task 1")
    expected_history = [TaskMemento({}, {}, 0)]
    task_manager.undo()
    expected_undo_history = [TaskMemento({1: 'Task 1'}, {}, 1)]
    assert app.current_state() == TaskMemento({}, {}, 0)
    assert task_manager.history == expected_history
    assert task_manager.undo_history == expected_undo_history

  def test_redo(self, app: TaskApp, task_manager: TaskManager):
    task_manager.backup()
    app.add_task("Task 1")
    expected_history = [TaskMemento({}, {}, 0)]
    task_manager.undo()
    expected_undo_history = [TaskMemento({1: 'Task 1'}, {}, 1)]
    task_manager.redo()
    expected_history.append(expected_undo_history.pop())

    assert app.current_state() == TaskMemento({1: 'Task 1'}, {}, 1)
    assert task_manager.history == expected_history
    assert task_manager.undo_history == expected_undo_history

  def test_add_task_after_undo(self, app: TaskApp, task_manager: TaskManager):
    task_manager.backup()
    app.add_task("Task 1")
    expected_history = [TaskMemento({}, {}, 0)]
    expected_undo_history = [TaskMemento({1: 'Task 1'}, {}, 1)]
    task_manager.undo()
    task_manager.backup()
    app.add_task("Task 2")
    expected_history.append(TaskMemento({}, {}, 0))
    expected_undo_history.clear()

    assert app.current_state() == TaskMemento({1: 'Task 2'}, {}, 1)
    assert task_manager.history == expected_history
    assert task_manager.undo_history == expected_undo_history

  def test_unavailable_undo(self, app: TaskApp, task_manager: TaskManager):
    task_manager.backup()
    app.add_task("Task 1")
    expected_history = [TaskMemento({}, {}, 0)]
    task_manager.undo()
    expected_undo_history = [TaskMemento({1: 'Task 1'}, {}, 1)]
    task_manager.undo()

    assert app.current_state() == TaskMemento({}, {}, 0)
    assert task_manager.history == expected_history
    assert task_manager.undo_history == expected_undo_history

  def test_unavailable_redo(self, app: TaskApp, task_manager: TaskManager):
    task_manager.backup()
    app.add_task("Task 1")
    expected_history = [TaskMemento({}, {}, 0)]
    task_manager.undo()
    expected_undo_history = [TaskMemento({1: 'Task 1'}, {}, 1)]
    task_manager.redo()
    expected_history.append(expected_undo_history.pop())
    task_manager.redo()
    assert app.current_state() == TaskMemento({1: "Task 1"}, {}, 1)
    assert task_manager.history == expected_history
    assert task_manager.undo_history == expected_undo_history


if __name__ == "__main__":
  pytest.main([__file__])
