from datetime import datetime
from pawpal_system import Task, Pet


def test_mark_complete_changes_status():
    task = Task(name="Morning walk", type="walk", due_date=datetime(2026, 3, 15, 8, 0))
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_count():
    pet = Pet(name="Buddy", species="dog", breed="Golden Retriever", age=3)
    assert len(pet.tasks) == 0
    pet.add_task(Task(name="Feeding", type="feeding", due_date=datetime(2026, 3, 15, 9, 0)))
    assert len(pet.tasks) == 1
