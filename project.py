#task management system
from datetime import datetime

def create_task(title, description, due_date, priority):
    return {'title': title, 'description': description, 'due_date': datetime.strptime(due_date, "%d.%m.%Y"), "priority": priority, 'completed': False}

#tasks = []

task_dict = {}

#1) create task

def add_task():
    title = input('Enter task title: ')
    description = input("Enter task description: ")
    due_date = input('Enter task due date: ') 
    priority = int(input('Enter task priority (1-High, 2-Medium, 3-Low): '))
    task = create_task(title, description, due_date, priority)
    tasks.append(task)
    task_dict[title] = task
    print('Task has been successfully added')

def delete_task():
    title = input("Enter the title of the task to delete: ")
    if title in task_dict:
        tasks.remove(task_dict[title])
        del task_dict[title]
        print('Task has been deleted')
    else:
        print('Task is not in the list')


#2) do something to the task + truth table check 
def mark_task_completed():
    title = input("Enter the title of the completed task: ")
    if title in task_dict:
        task_dict[title]['completed'] = True
        print(f"Task '{title}' marked as completed.")
    else:
        print("Task not found.")


def view_all_tasks():
    if not tasks:
        print("No tasks available.")
        return
    for task in tasks:
        if task['completed']:
            status = '✔'
        elif not task['completed']:
            status = '✘'
        print(f"[{status}] {task['title']} - Priority: {task['priority']}, Due: {task['due_date'].date()}")

def view_pending_tasks():
    pending_tasks = [task for task in tasks if not task['completed']]
    if not pending_tasks:
        print("No pending tasks.")
        return
    for task in pending_tasks:
        if task['completed']:
            status = '✔'
        elif not task['completed']:
            status = '✘'
        print(f"[{status}] {task['title']} - Priority: {task['priority']}, Due: {task['due_date'].date()}")


#4) sorting the tasks
def sort_tasks_by_priority():
    sorted_tasks = []
    for task in tasks:
        inserted = False
        for i in range(len(sorted_tasks)):
            if task['priority'] < sorted_tasks[i]['priority']:
                sorted_tasks.insert(i, task)
                inserted = True
                break
        if not inserted:
            sorted_tasks.append(task)

    for task in sorted_tasks:
        if task['completed'] == True:
            status = '✔'
        elif task['completed'] == False:
            status = '✘'
        else:
            status = '?'
        print(f"[{status}] {task['title']} - Priority: {task['priority']}, Due: {task['due_date'].date()}")

def sort_tasks_by_due_date():
    sorted_tasks = []
    for task in tasks:
        inserted = False
        for i in range(len(sorted_tasks)):
            if task['due_date'] < sorted_tasks[i]['due_date']:
                sorted_tasks.insert(i, task)
                inserted = True
                break
        if not inserted:
            sorted_tasks.append(task)

    for task in sorted_tasks:
        if task['completed'] == True:
            status = '✔'
        elif task['completed'] == False:
            status = '✘'
        else:
            status = '?'
        print(f"[{status}] {task['title']} - Priority: {task['priority']}, Due: {task['due_date'].date()}")


#6) search

def recursive_search_task(title, index=0):
    if index < len(tasks):
        current_task = tasks[index]
        if current_task['title'] == title:
            return current_task
        else:
            return recursive_search_task(title, index + 1)
    return None





#example:

tasks = [
    {
        'title': 'Finish assignment',
        'description': 'Complete the Python project',
        'priority': 2,
        'due_date': datetime(2025, 4, 20),
        'completed': False
    },
    {
        'title': 'Buy groceries',
        'description': 'Milk, Eggs, Bread',
        'priority': 1,
        'due_date': datetime(2025, 4, 18),
        'completed': True
    },
    {
        'title': 'Workout',
        'description': 'Go for a 30 min run',
        'priority': 3,
        'due_date': datetime(2025, 4, 19),
        'completed': False
    }
]
view_all_tasks()
sort_tasks_by_due_date()
#7) menu