from datetime import datetime
import pandas as pd
import time
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt



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
        return f"[{status}] {self.title} - Priority: {self.priority}, Due: {self.due_date.date()}, Logic: {self.logical_expression}"

    def evaluate_logic(self, p=True, q=False):
        try:
            expr = self.logical_expression
            expr = expr.replace('∧', ' and ').replace('∨', ' or ').replace('¬', ' not ')
            expr = expr.replace('→', '<=').replace('↔', '==')

          
            allowed_names = {'p': p, 'q': q, 'and': lambda a,b: a and b, 'or': lambda a,b: a or b,
                             'not': lambda a: not a, '<=': lambda a,b: a <= b, '==': lambda a,b: a == b,
                             'True': True, 'False': False}


            result = eval(expr, {"__builtins__": None}, {'p': p, 'q': q})
            return bool(result)
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

            while j >= 0 and (
                task_list[j].priority > key.priority or
                (task_list[j].priority == key.priority and
                 not task_list[j].evaluate_logic() and key.evaluate_logic())
            ):
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
            l = left[0]
            r = right[0]

            if (l.priority < r.priority or
                (l.priority == r.priority and l.evaluate_logic() and not r.evaluate_logic())):
                result.append(left.pop(0))
            else:
                result.append(right.pop(0))
        result.extend(left)
        result.extend(right)
        return result




def recursive_search(tasks, title, index=0):
    if index >= len(tasks):
        return None
    if tasks[index].title == title:
        return tasks[index]
    return recursive_search(tasks, title, index + 1)




class TaskManager:
    def __init__(self):
        self.tasks = []
        self.task_dict = {}

    def add_task(self, title, description, due_date, priority, logical_expression):
        if title in self.task_dict:
            raise ValueError("Task with this title already exists.")
        task = Task(title, description, due_date, priority, logical_expression)
        self.tasks.append(task)
        self.task_dict[title] = task

    def delete_task(self, title):
        task = self.task_dict.pop(title, None)
        if task:
            self.tasks.remove(task)
        else:
            raise ValueError("Task not found.")

    def mark_task_completed(self, title):
        task = self.task_dict.get(title)
        if task:
            task.completed = True
        else:
            raise ValueError("Task not found.")

    def get_all_tasks(self):
        return self.tasks

    def get_pending_tasks(self):
        return [t for t in self.tasks if not t.completed]

    def get_completed_tasks(self):
        return [t for t in self.tasks if t.completed]

    def load_tasks_from_csv(self, filename):
        df = pd.read_csv(filename)
        for _, row in df.iterrows():

            try:
                completed = row.get('completed', False)
                if isinstance(completed, str):
                    completed = completed.lower() in ['true', '1', 'yes']
                self.add_task(row['title'], row['description'], row['due_date'],
                              int(row['priority']), row['logical_expression'])
                self.task_dict[row['title']].completed = completed
            except Exception as e:
                print(f"Skipping row due to error: {e}")

    def save_tasks_to_csv(self, filename):
        data = [{
            'title': t.title,
            'description': t.description,
            'due_date': t.due_date.strftime("%d.%m.%Y"),
            'priority': t.priority,
            'logical_expression': t.logical_expression,
            'completed': t.completed
        } for t in self.tasks]
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)




task_manager = TaskManager()


def display_tasks(task_list):
    if not task_list:
        print("No tasks available.")
    else:
        for task in task_list:
            print(task)


def add_task_ui():
    try:
        title = input('Enter task title: ')
        description = input("Enter task description: ")
        due_date = input('Enter task due date (dd.mm.yyyy): ')
        priority = int(input('Enter task priority (1-High, 2-Medium, 3-Low): '))
        logic = input('Enter logical expression (use p, q, ∧, ∨, →, ¬, ↔): ')
        task_manager.add_task(title, description, due_date, priority, logic)
        print('Task has been successfully added.')
    except ValueError as e:
        print(f"Error: {e}")
    except Exception:
        print("Invalid input, please try again.")


def delete_task_ui():
    title = input("Enter title of task to delete: ")
    try:
        task_manager.delete_task(title)
        print("Task deleted.")
    except ValueError as e:
        print(e)


def mark_task_completed_ui():
    title = input("Enter title of completed task: ")
    try:
        task_manager.mark_task_completed(title)
        print("Task marked as completed.")
    except ValueError as e:
        print(e)


def sort_tasks_ui(sort_algo):
    sorter = sort_algo()
    start = time.time()
    sorted_list = sorter.sort(task_manager.get_all_tasks()[:])
    duration = time.time() - start
    display_tasks(sorted_list)
    print(f"\nSort completed in {duration:.4f} seconds.")


def search_task_ui():
    title = input("Enter task title to search: ")
    result = recursive_search(task_manager.get_all_tasks(), title)
    if result:
        print(result)
    else:
        print("Task not found.")


def analyze_sort_performance_ui():
    print("\nAnalyzing performance:")
    algorithms = [InsertionSort, MergeSort]
    times = []
    sizes = [10, 100, 500] 

    for size in sizes:
        print(f"\nDataset size: {size}")

        test_tasks = []
        for i in range(size):

            priority = (i % 3) + 1
            logic = 'p ∧ q' if i % 2 == 0 else 'p ∨ ¬q'
            due_date = "01.01.2025"
            task = Task(f"Task{i}", "desc", due_date, priority, logic)
            test_tasks.append(task)

        for SortAlgorithm in algorithms:
            sorter = SortAlgorithm()
            start = time.time()
            sorter.sort(test_tasks[:])
            duration = time.time() - start
            print(f"{SortAlgorithm.__name__} took {duration:.6f} seconds on size {size}.")
            times.append((SortAlgorithm.__name__, size, duration))


    filtered_times = [t for t in times if t[1] == sizes[-1]]
    names = [t[0] for t in filtered_times]
    vals = [t[2] for t in filtered_times]
    plt.bar(names, vals, color=['skyblue', 'lightgreen'])
    plt.title(f"Sorting Algorithm Performance on Dataset Size {sizes[-1]}")
    plt.xlabel("Algorithm")
    plt.ylabel("Time (seconds)")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


def display_menu():
    print("\n--- Task Manager ---")
    print("1. Add Task")
    print("2. Delete Task")
    print("3. Mark Task Completed")
    print("4. View All Tasks")
    print("5. View Pending Tasks")
    print("6. View Completed Tasks")
    print("7. Sort Tasks (Insertion Sort - loop)")
    print("8. Sort Tasks (Merge Sort - recursion)")
    print("9. Search Task (Recursive)")
    print("10. Load Tasks from CSV")
    print("11. Save Tasks to CSV")
    print("12. Analyze Sort Performance")
    print("0. Exit")


def task_manager_ui():
    while True:
        display_menu()
        choice = input("Choose an option: ").strip()
        if choice == '1':
            add_task_ui()
        elif choice == '2':
            delete_task_ui()
        elif choice == '3':
            mark_task_completed_ui()
        elif choice == '4':
            display_tasks(task_manager.get_all_tasks())
        elif choice == '5':
            display_tasks(task_manager.get_pending_tasks())
        elif choice == '6':
            display_tasks(task_manager.get_completed_tasks())
        elif choice == '7':
            sort_tasks_ui(InsertionSort)
        elif choice == '8':
            sort_tasks_ui(MergeSort)
        elif choice == '9':
            search_task_ui()
        elif choice == '10':
            filename = input("Enter filename to load: ")
            try:
                task_manager.load_tasks_from_csv(filename)
                print("Tasks loaded successfully.")
            except Exception as e:
                print(f"Failed to load tasks: {e}")
        elif choice == '11':
            filename = input("Enter filename to save: ")
            try:
                task_manager.save_tasks_to_csv(filename)
                print("Tasks saved successfully.")
            except Exception as e:
                print(f"Failed to save tasks: {e}")
        elif choice == '12':
            analyze_sort_performance_ui()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == '__main__':
    task_manager_ui()

