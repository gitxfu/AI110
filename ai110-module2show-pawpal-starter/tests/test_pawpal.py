from datetime import datetime, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


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


def test_sort_by_time_returns_chronological_order():
    owner = Owner(name="Alex", email="alex@example.com")
    pet = Pet(name="Buddy", species="dog", breed="Lab", age=2)
    owner.add_pet(pet)

    pet.add_task(Task(name="Lunch", type="feeding", due_date=datetime(2026, 3, 15, 12, 0)))
    pet.add_task(Task(name="Walk", type="walk", due_date=datetime(2026, 3, 15, 7, 0)))
    pet.add_task(Task(name="Meds", type="medication", due_date=datetime(2026, 3, 15, 9, 0)))

    scheduler = Scheduler()
    scheduler.add_owner(owner)
    sorted_tasks = scheduler.sort_by_time()

    times = [task.due_date for _, task in sorted_tasks]
    assert times == sorted(times)


def test_daily_recurrence_creates_next_day_task():
    task = Task(name="Walk", type="walk", due_date=datetime(2026, 3, 15, 8, 0), frequency="daily")
    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.completed is False
    assert next_task.due_date == datetime(2026, 3, 16, 8, 0)


def test_detect_conflicts_flags_same_time():
    owner = Owner(name="Alex", email="alex@example.com")
    buddy = Pet(name="Buddy", species="dog", breed="Lab", age=2)
    whiskers = Pet(name="Whiskers", species="cat", breed="Siamese", age=3)
    owner.add_pet(buddy)
    owner.add_pet(whiskers)

    same_time = datetime(2026, 3, 15, 8, 0)
    buddy.add_task(Task(name="Walk", type="walk", due_date=same_time))
    whiskers.add_task(Task(name="Feeding", type="feeding", due_date=same_time))

    scheduler = Scheduler()
    scheduler.add_owner(owner)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "Walk" in conflicts[0]
    assert "Feeding" in conflicts[0]


def test_pet_with_no_tasks_returns_empty_schedule():
    """INTENTIONALLY FAILING: expects 1 task but pet has none."""
    owner = Owner(name="Alex", email="alex@example.com")
    pet = Pet(name="Buddy", species="dog", breed="Lab", age=2)
    owner.add_pet(pet)

    scheduler = Scheduler()
    scheduler.add_owner(owner)
    todays = scheduler.get_tasks_due_today()

    # this assert is wrong — pet has no tasks, so len should be 0
    assert len(todays) == 1, "Expected 1 task but got none"
