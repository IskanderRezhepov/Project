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

#7) menu


def display_menu():
    print("\n--- Task Manager ---")
    print("1. Add Task")
    print("2. Delete Task")
    print("3. Mark Task Completed")
    print("4. View All Tasks")
    print("5. View Pending Tasks")
    print("6. View Completed Tasks")
    print("7. Sort Tasks by Priority")
    print("8. Sort Tasks by Due Date")
    print("9. Search Task by Title")
    print("0. Exit")

def task_manager():
    while True:
        display_menu()
        choice = input("Choose an option: ")

        if choice == '1':
            add_task()
        elif choice == '2':
            delete_task()
        elif choice == '3':
            mark_task_completed()
        elif choice == '4':
            view_all_tasks()
        elif choice == '5':
            view_pending_tasks()
        elif choice == '6':
            view_completed_tasks()
        elif choice == '7':
            sort_tasks_by_priority()
        elif choice == '8':
            sort_tasks_by_due_date()
        elif choice == '9':
            title = input("Enter task title to search: ")
            result = recursive_search_task(title)
            print(result if result else "Task not found.")
        elif choice == '0':
            print("Exiting task manager...")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == '__main__':
    task_manager()