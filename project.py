
from datetime import datetime
import pandas as pd
import time
import re 
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt

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
            p, q = True, False 
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

task_dict = {}

def add_task():
    try:
        title = input('Enter task title: ')
        if title in task_dict:
            print("Task with this title already exists.")
            return
        description = input("Enter task description: ")
        due_date = input('Enter task due date (dd.mm.yyyy): ')
        priority = int(input('Enter task priority (1-High, 2-Medium, 3-Low): '))
        logic = input('Enter logical expression (use p, q, ∧, ∨, →, ¬): ')
        task = Task(title, description, due_date, priority, logic)
        tasks.append(task)
        task_dict[title] = task
        print('Task has been successfully added.')
    except ValueError:
        print("Invalid priority or date format. Please try again.")
    except Exception as e:
        print(f"Error: {e}")


def delete_task():
    title = input("Enter title of task to delete: ")
    task = task_dict.pop(title, None)
    if task:
        tasks.remove(task)
        print("Task deleted.")
    else:
        print("Task not found.")

    
def mark_task_completed():
    title = input("Enter title of completed task: ")
    task = task_dict.get(title)
    if task:
        task.completed = True
        print("Task marked as completed.")
    else:
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

def recursive_search(title, index=0):
    if index >= len(tasks):
        return None
    if tasks[index].title == title:
        return tasks[index]
    return recursive_search(title, index + 1)

#csv
def read_tasks_from_csv(filename):
    try:
        df = pd.read_csv(filename)
        for _, row in df.iterrows():
            task = Task(row['title'], row['description'], row['due_date'], row['priority'], row['logical_expression'], row['completed'])
            tasks.append(task)
            task_dict[task.title] = task
        print("Tasks loaded successfully.")
    except Exception as e:
        print(f"Failed to read file: {e}")

def write_tasks_to_csv(filename):
    try:
        data = [{
            'title': t.title,
            'description': t.description,
            'due_date': t.due_date.strftime("%d.%m.%Y"),
            'priority': t.priority,
            'logical_expression': t.logical_expression,
            'completed': t.completed
        } for t in tasks]
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print("Tasks saved successfully.")
    except Exception as e:
        print(f"Failed to write file: {e}")

#7) menu

def display_menu():
    print("\n--- Task Manager ---")
    print("1. Add Task")
    print("2. Delete Task")
    print("3. Mark Task Completed")
    print("4. View All Tasks")
    print("5. View Pending Tasks")
    print("6. View Completed Tasks")
    print("7. Sort Tasks (Insertion Sort)")
    print("8. Sort Tasks (Merge Sort)")
    print("9. Search Task (Recursive)")
    print("10. Load Tasks from CSV")
    print("11. Save Tasks to CSV")
    print("12. Analyze Sort Performance")
    print("0. Exit")

def analyze_sort_performance():
    print("\nAnalyzing performance:")
    algorithms = [InsertionSort, MergeSort]
    times = []

    for SortAlgorithm in algorithms:
        start = time.time()
        SortAlgorithm().sort(tasks[:])
        end = time.time()
        duration = end - start
        times.append(duration)
        print(f"{SortAlgorithm.__name__} took {duration:.6f} seconds on current dataset.")


    names = [algo.__name__ for algo in algorithms]
    plt.bar(names, times, color=['skyblue', 'lightgreen'])
    plt.title("Sorting Algorithm Performance")
    plt.xlabel("Algorithm")
    plt.ylabel("Time (seconds)")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

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
            sort_tasks(InsertionSort)
        elif choice == '8':
            sort_tasks(MergeSort)
        elif choice == '9':
            title = input("Enter title: ")
            result = recursive_search(title)
            print(result if result else "Task not found.")
        elif choice == '10':
            filename = input("Enter filename: ")
            read_tasks_from_csv(filename)
        elif choice == '11':
            filename = input("Enter filename to save to: ")
            write_tasks_to_csv(filename)
        elif choice == '12':
            analyze_sort_performance()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == '__main__':
    task_manager()
