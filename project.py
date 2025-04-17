#task management system
from datetime import datetime

def create_task(title, description, due_date, priority):
    return {'title': title, 'description': description, 'due_date': datetime.strptime(due_date, "%d.%m.%Y"), "priority": priority, 'completed': False}

tasks = []

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


add_task()
view_all_tasks()

#3) listing the tasks

#4) sorting the tasks

#6) search

#7) menu