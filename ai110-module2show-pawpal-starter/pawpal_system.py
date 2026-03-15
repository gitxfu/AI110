from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    """Represents a single pet care task (feeding, walk, medication, etc.)."""
    name: str
    type: str
    due_date: datetime
    completed: bool = False
    notes: str = ""

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

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
