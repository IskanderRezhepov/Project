#task management system
from datetime import datetime

def create_task(title, description, due_date, priority):
    return {'title': title, 'description': description, 'due_date': datetime.strptime(due_date, "%d.%m.%Y"), "priority": priority, 'completed': False}

tasks = []

task_dict = {}

#1) create task
class Task:
    def __init__(self, title, description, due_date, priority, logical_expression, completed=False):
        self.title = title
        self.description = description
        self.due_date = datetime.strptime(due_date, "%d.%m.%Y")
        self.priority = int(priority)
        self.logical_expression = logical_expression
        self.completed = completed

    def __str__(self):
        status = '✔' if self.completed else '✘'
        return f"[{status}] {self.title} - Priority: {self.priority}, Due: {self.due_date.date()}"

    def evaluate_logic(self):
        try:
            p, q = True, False  # default for evaluation
            return eval(self.logical_expression.replace('∧', 'and').replace('∨', 'or')
                        .replace('¬', 'not ').replace('→', '<=').replace('↔', '=='))
        except Exception:
            return False

class Sorter(ABC):
    @abstractmethod
    def sort(self, task_list):
        pass

class InsertionSort(Sorter):
    def sort(self, task_list):
        for i in range(1, len(task_list)):
            key = task_list[i]
            j = i - 1
            while j >= 0 and (task_list[j].priority > key.priority or (
                task_list[j].priority == key.priority and not task_list[j].evaluate_logic() and key.evaluate_logic())):
                task_list[j + 1] = task_list[j]
                j -= 1
            task_list[j + 1] = key
        return task_list
    
class MergeSort(Sorter):
    def sort(self, task_list):
        if len(task_list) <= 1:
            return task_list
        mid = len(task_list) // 2
        left = self.sort(task_list[:mid])
        right = self.sort(task_list[mid:])
        return self.merge(left, right)

    def merge(self, left, right):
        result = []
        while left and right:
            if (left[0].priority < right[0].priority or
                (left[0].priority == right[0].priority and left[0].evaluate_logic() and not right[0].evaluate_logic())):
                result.append(left.pop(0))
            else:
                result.append(right.pop(0))
        result.extend(left + right)
        return result

tasks = []

def add_task():
    title = input('Enter task title: ')
    description = input("Enter task description: ")
    due_date = input('Enter task due date (dd.mm.yyyy): ')
    priority = int(input('Enter task priority (1-High, 2-Medium, 3-Low): '))
    logic = input('Enter logical expression (use p, q, ∧, ∨, →, ¬): ')
    try:
        task = Task(title, description, due_date, priority, logic)
        tasks.append(task)
        print('Task has been successfully added.')
    except Exception as e:
        print(f"Error: {e}")

def delete_task():
    title = input("Enter title of task to delete: ")
    for task in tasks:
        if task.title == title:
            tasks.remove(task)
            print("Task deleted.")
            return
    print("Task not found.")

def mark_task_completed():
    title = input("Enter title of completed task: ")
    for task in tasks:
        if task.title == title:
            task.completed = True
            print("Task marked as completed.")
            return
    print("Task not found.")

def view_all_tasks():
    if not tasks:
        print("No tasks available.")
        return
    for task in tasks:
        print(task)

def view_pending_tasks():
    pending = [t for t in tasks if not t.completed]
    if not pending:
        print("No pending tasks.")
        return
    for task in pending:
        print(task)

def view_completed_tasks():
    done = [t for t in tasks if t.completed]
    if not done:
        print("No completed tasks.")
        return
    for task in done:
        print(task)


#4) sorting the tasks
def sort_tasks(algorithm):
    sorter = algorithm()
    start = time.time()
    sorted_list = sorter.sort(tasks[:])
    duration = time.time() - start
    for t in sorted_list:
        print(t)
    print(f"\nSort completed in {duration:.4f} seconds.")


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