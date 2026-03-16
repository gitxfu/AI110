from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler

# --- Create Owner ---
alex = Owner(name="Alex", email="alex@example.com")

# --- Create Pets ---
buddy = Pet(name="Buddy", species="dog", breed="Golden Retriever", age=3)
whiskers = Pet(name="Whiskers", species="cat", breed="Siamese", age=5)

alex.add_pet(buddy)
alex.add_pet(whiskers)

# --- Add Tasks (out of order to test sorting) ---
today = datetime.now().replace(second=0, microsecond=0)

buddy.add_task(Task(name="Flea medication", type="medication", due_date=today.replace(hour=12, minute=0)))
buddy.add_task(Task(name="Morning walk", type="walk", due_date=today.replace(hour=7, minute=30), frequency="daily"))
buddy.add_task(Task(name="Breakfast", type="feeding", due_date=today.replace(hour=8, minute=0), frequency="daily"))

whiskers.add_task(Task(name="Play session", type="enrichment", due_date=today.replace(hour=10, minute=0)))
whiskers.add_task(Task(name="Breakfast", type="feeding", due_date=today.replace(hour=7, minute=0), frequency="daily"))
# Conflict: same time as Buddy's morning walk
whiskers.add_task(Task(name="Grooming", type="appointment", due_date=today.replace(hour=7, minute=30)))

# --- Build Scheduler ---
scheduler = Scheduler()
scheduler.add_owner(alex)

# === 1. Sorting by time ===
print("=" * 55)
print("  PawPal+ -- Today's Schedule for", alex.name)
print("  " + today.strftime("%A, %B %d, %Y"))
print("=" * 55)

sorted_tasks = scheduler.sort_by_time(scheduler.get_tasks_due_today())
for pet_name, task in sorted_tasks:
    time_str = task.due_date.strftime("%I:%M %p")
    freq = f" [{task.frequency}]" if task.frequency != "once" else ""
    status = "[x]" if task.completed else "[ ]"
    print(f"  {status} {time_str}  [{pet_name}] {task.name} ({task.type}){freq}")

print(f"\n  Total tasks: {len(sorted_tasks)}")

# === 2. Conflict detection ===
print("\n" + "-" * 55)
print("  CONFLICT CHECK")
print("-" * 55)
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  !! {warning}")
else:
    print("  No conflicts found.")

# === 3. Filtering by pet ===
print("\n" + "-" * 55)
print("  FILTER: Buddy's tasks only")
print("-" * 55)
buddy_tasks = scheduler.filter_by_pet_name("Buddy")
for pet_name, task in buddy_tasks:
    print(f"  {task.due_date.strftime('%I:%M %p')}  {task.name} ({task.type})")

# === 4. Recurring task demo ===
print("\n" + "-" * 55)
print("  RECURRING TASK DEMO")
print("-" * 55)
walk_task = buddy.get_tasks()[1]  # Morning walk (daily)
print(f"  Completing '{walk_task.name}' (frequency: {walk_task.frequency})...")
next_task = walk_task.mark_complete()
if next_task:
    buddy.add_task(next_task)
    print(f"  -> New task created: '{next_task.name}' on {next_task.due_date.strftime('%A, %B %d at %I:%M %p')}")

# === 5. Filter by status ===
print("\n" + "-" * 55)
print("  FILTER: Incomplete tasks only")
print("-" * 55)
incomplete = scheduler.filter_by_status(completed=False)
for pet_name, task in incomplete:
    print(f"  [ ] {task.due_date.strftime('%I:%M %p')}  [{pet_name}] {task.name}")

print("\n" + "=" * 55)
