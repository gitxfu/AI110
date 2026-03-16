# Week 4 - PawPal+ System

---

## Phase 1: UML Design (Assigned)

### TFs should:

- [X] Generate UML Design

My prompt: I'm designing a pet care management app called PawPal+. It needs four core classes: Owner, Pet, Task, and Scheduler. The Owner has multiple Pets, each Pet has multiple Tasks (like feedings, walks, medications), and the Scheduler organizes tasks across all pets. Generate a Mermaid.js class diagram showing these classes with their attributes, methods, and relationships.

- [X] Map UML to Python classes (`pawpal_system.py`)

My prompt: Based on this UML diagram, generate Python class skeletons using dataclasses for Task and Pet. Don't implement any logic yet.

- [X] Identify relationships (Owner → Pet → Task → Scheduler)

### TFs may skip:

- Mermaid formatting work
- Extended design writing

---

## Phase 2: Core Implementation (Assigned)

### TFs should:

My prompt (Step 1, 2): Implement core functions in pawpal_system and write a main.py demo script that imports from pawpal_system.py, creates an Owner named 'Alex' with two pets (a dog named 'Buddy' and a cat named 'Whiskers'), adds 3 tasks with different times to each, and prints a formatted toady's schedule to the terminal.

My prompt (Step 3): Generate two pytest tests for my pawpal_system.py: one that verifies mark_complete() changes a task's status from False to True, and one that verifies adding a task to a Pet increases len(pet.tasks) by 1.

- [X] Set up code for classes in `pawpal_systems.py` (Owner, Pet, Task, Scheduler)
- [X] Run `main.py` demo
- [X] `main.py` implementation should include:
  - [X] One owner, two pets, at least 3 tasks
  - [X] Testing scheduler
- [X] Trace data flow across classes
- [X] Verify task creation and retrieval
- [X] Inspect at least one class method carefully

### TFs may skip:

- Writing full implementations (enough that `main.py` works and shows the flow)
- Creating large datasets of pets/tasks
- Building a full pytest suite (generate at least 2 tests)

**High-risk student confusion areas:**

- Owner → Scheduler access patterns
- Task storage structure

---

## Phase 3: UI Integration (Assigned)

### TFs should:

My prompt (Step 1, 2): Implement core functions in pawpal_system and write a main.py demo script that imports from pawpal_system.py, creates an Owner named 'Alex' with two pets (a dog named 'Buddy' and a cat named 'Whiskers'), adds 3 tasks with different times to each, and prints a formatted toady's schedule to the terminal.

- [X] Integrate backend (`pawpal_system.py`) into the UI (`app.py`)
- [X] Implement at least one function (e.g., adding a pet, scheduling a task)
- [X] Understand `st.session_state` usage
- [X] Identify the common "state reset" bug
- [X] Trace one UI action to backend logic

### TFs may skip:

- UI styling
- Layout polish

**New concept:** Streamlit state persistence model

---

## Phase 4: Algorithmic Layer (Assigned)

### TFs should:

- [X] Pick 2 of the listed algorithms
- [X] Implement Sorting and Filtering
- [X] Verify conflict detection behavior
- [X] Reason through recurring task logic
- [X] Debug at least one edge case

### TFs may skip:

- Implementing every algorithm from scratch
- Heavy optimization work
- Documentation

**Why this matters:** This phase generates significant breakout traffic.

---

## Phase 5: Testing (Spot Check)

### TFs should:

- [X] Use AI to generate a test suite
- [X] Run `pytest`
- [X] Interpret one failing test scenario
  A failing test is I created a pet with no tasks, `get_tasks_due_today()` correctly returns []. I put a wrong assertion == 1, which should be == 0.

### TFs may view:

- Documentation
