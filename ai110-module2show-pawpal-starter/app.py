import streamlit as st
from datetime import datetime, time
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("A smart pet care management system")

# --- Session State: persist objects across reruns ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="", email="")
    st.session_state.scheduler = Scheduler()
    st.session_state.scheduler.add_owner(st.session_state.owner)

owner = st.session_state.owner
scheduler = st.session_state.scheduler

# --- Owner Info ---
st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name or "Jordan")
owner.email = st.text_input("Email", value=owner.email or "jordan@example.com")

st.divider()

# --- Add a Pet ---
st.subheader("Add a Pet")
col1, col2 = st.columns(2)
with col1:
    new_pet_name = st.text_input("Pet name", value="Mochi")
    new_species = st.selectbox("Species", ["dog", "cat", "other"])
with col2:
    new_breed = st.text_input("Breed", value="")
    new_age = st.number_input("Age", min_value=0, max_value=30, value=2)

if st.button("Add pet"):
    pet = Pet(name=new_pet_name, species=new_species, breed=new_breed, age=new_age)
    owner.add_pet(pet)
    st.success(f"Added {new_pet_name}!")

# Show current pets
if owner.get_pets():
    st.markdown("**Your pets:** " + ", ".join(p.name for p in owner.get_pets()))
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Add a Task ---
st.subheader("Add a Task")

if owner.get_pets():
    pet_names = [p.name for p in owner.get_pets()]
    selected_pet_name = st.selectbox("Assign to pet", pet_names)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        task_type = st.selectbox("Type", ["walk", "feeding", "medication", "appointment", "enrichment"])
    with col3:
        task_time = st.time_input("Time", value=time(8, 0))

    if st.button("Add task"):
        selected_pet = next(p for p in owner.get_pets() if p.name == selected_pet_name)
        due = datetime.combine(datetime.now().date(), task_time)
        task = Task(name=task_title, type=task_type, due_date=due)
        selected_pet.add_task(task)
        st.success(f"Added '{task_title}' for {selected_pet_name}!")
else:
    st.info("Add a pet first before scheduling tasks.")

st.divider()

# --- Generate Schedule ---
st.subheader("Today's Schedule")

if st.button("Generate schedule"):
    todays_tasks = scheduler.get_tasks_due_today()
    todays_tasks.sort(key=lambda item: item[1].due_date)

    if todays_tasks:
        table_data = []
        for pet_name, task in todays_tasks:
            table_data.append({
                "Time": task.due_date.strftime("%I:%M %p"),
                "Pet": pet_name,
                "Task": task.name,
                "Type": task.type,
                "Done": "Yes" if task.completed else "No",
            })
        st.table(table_data)
    else:
        st.warning("No tasks scheduled for today. Add some tasks above!")
