from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler

# --- Create Owner ---
alex = Owner(name="Alex", email="alex@example.com")

# --- Create Pets ---
buddy = Pet(name="Buddy", species="dog", breed="Golden Retriever", age=3)
whiskers = Pet(name="Whiskers", species="cat", breed="Siamese", age=5)

alex.add_pet(buddy)
alex.add_pet(whiskers)

# --- Add Tasks for Buddy ---
today = datetime.now().replace(second=0, microsecond=0)

buddy.add_task(Task(name="Morning walk", type="walk", due_date=today.replace(hour=7, minute=30)))
buddy.add_task(Task(name="Breakfast", type="feeding", due_date=today.replace(hour=8, minute=0)))
buddy.add_task(Task(name="Flea medication", type="medication", due_date=today.replace(hour=12, minute=0)))

# --- Add Tasks for Whiskers ---
whiskers.add_task(Task(name="Breakfast", type="feeding", due_date=today.replace(hour=7, minute=0)))
whiskers.add_task(Task(name="Play session", type="enrichment", due_date=today.replace(hour=10, minute=0)))
whiskers.add_task(Task(name="Vet appointment", type="appointment", due_date=today.replace(hour=14, minute=30)))

# --- Build Schedule ---
scheduler = Scheduler()
scheduler.add_owner(alex)

todays_tasks = scheduler.get_tasks_due_today()
# Sort by time
todays_tasks.sort(key=lambda item: item[1].due_date)

# --- Print Formatted Schedule ---
print("=" * 50)
print(f"  PawPal+ -- Today's Schedule for {alex.name}")
print(f"  {today.strftime('%A, %B %d, %Y')}")
print("=" * 50)

for pet_name, task in todays_tasks:
    time_str = task.due_date.strftime("%I:%M %p")
    status = "[x]" if task.completed else "[ ]"
    print(f"  {status} {time_str}  [{pet_name}] {task.name} ({task.type})")

print("=" * 50)
print(f"  Total tasks: {len(todays_tasks)}")
print()

# --- Test mark_complete ---
print("Marking 'Morning walk' as complete...")
buddy.get_tasks()[0].mark_complete()

print()
print("Updated schedule:")
print("-" * 50)
for pet_name, task in todays_tasks:
    time_str = task.due_date.strftime("%I:%M %p")
    status = "[x]" if task.completed else "[ ]"
    print(f"  {status} {time_str}  [{pet_name}] {task.name} ({task.type})")
print("-" * 50)
