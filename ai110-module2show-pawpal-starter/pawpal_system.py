from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class Task:
    """Represents a single pet care task (feeding, walk, medication, etc.)."""
    name: str
    type: str
    due_date: datetime
    frequency: str = "once"  # "once", "daily", "weekly"
    completed: bool = False
    notes: str = ""

    def mark_complete(self):
        """Mark this task as completed. Returns a new Task for the next occurrence if recurring, else None."""
        self.completed = True
        if self.frequency == "daily":
            return Task(name=self.name, type=self.type,
                        due_date=self.due_date + timedelta(days=1),
                        frequency=self.frequency, notes=self.notes)
        elif self.frequency == "weekly":
            return Task(name=self.name, type=self.type,
                        due_date=self.due_date + timedelta(weeks=1),
                        frequency=self.frequency, notes=self.notes)
        return None

    def reschedule(self, new_date: datetime):
        """Reschedule this task to a new date/time."""
        self.due_date = new_date

    def is_overdue(self) -> bool:
        """Check if this task is past its due date."""
        return not self.completed and self.due_date < datetime.now()


@dataclass
class Pet:
    """Represents a pet with its details and associated tasks."""
    name: str
    species: str
    breed: str
    age: int
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task):
        """Remove a task from this pet's task list."""
        self.tasks.remove(task)

    def get_tasks(self) -> list:
        """Return all tasks for this pet."""
        return self.tasks


@dataclass
class Owner:
    """Represents a pet owner who manages multiple pets."""
    name: str
    email: str
    pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's collection."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet):
        """Remove a pet from this owner's collection."""
        self.pets.remove(pet)

    def get_pets(self) -> list:
        """Return all pets belonging to this owner."""
        return self.pets


class Scheduler:
    """The brain of PawPal+ — organizes and manages tasks across all pets."""

    def __init__(self):
        self.owners: list = []

    def add_owner(self, owner: Owner):
        """Register an owner with the scheduler."""
        self.owners.append(owner)

    def get_all_tasks(self) -> list:
        """Retrieve all tasks across all owners and their pets."""
        tasks = []
        for owner in self.owners:
            for pet in owner.get_pets():
                for task in pet.get_tasks():
                    tasks.append((pet.name, task))
        return tasks

    def get_tasks_due_today(self) -> list:
        """Return only tasks that are due today."""
        today = datetime.now().date()
        return [
            (pet_name, task)
            for pet_name, task in self.get_all_tasks()
            if task.due_date.date() == today
        ]

    def get_overdue_tasks(self) -> list:
        """Return all tasks that are past their due date."""
        return [
            (pet_name, task)
            for pet_name, task in self.get_all_tasks()
            if task.is_overdue()
        ]

    def get_tasks_by_pet(self, pet: Pet) -> list:
        """Return all tasks for a specific pet."""
        return pet.get_tasks()

    def sort_by_time(self, tasks: list = None) -> list:
        """Sort tasks by due_date. Uses all tasks if none provided."""
        if tasks is None:
            tasks = self.get_all_tasks()
        return sorted(tasks, key=lambda item: item[1].due_date)

    def filter_by_status(self, completed: bool) -> list:
        """Filter all tasks by completion status."""
        return [
            (pet_name, task)
            for pet_name, task in self.get_all_tasks()
            if task.completed == completed
        ]

    def filter_by_pet_name(self, pet_name: str) -> list:
        """Filter all tasks for a specific pet by name."""
        return [
            (pn, task)
            for pn, task in self.get_all_tasks()
            if pn == pet_name
        ]

    def detect_conflicts(self) -> list:
        """Detect tasks scheduled at the same time. Returns list of warning strings."""
        warnings = []
        all_tasks = self.get_all_tasks()
        for i in range(len(all_tasks)):
            for j in range(i + 1, len(all_tasks)):
                pet_a, task_a = all_tasks[i]
                pet_b, task_b = all_tasks[j]
                if task_a.due_date == task_b.due_date:
                    warnings.append(
                        f"Conflict: '{task_a.name}' ({pet_a}) and "
                        f"'{task_b.name}' ({pet_b}) at {task_a.due_date.strftime('%I:%M %p')}"
                    )
        return warnings
