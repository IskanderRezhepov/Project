#task management system
from datetime import datetime

def create_task(title, description, due_date, priority):
    return {'title': title, 'description': description, 'due_date': due_date, "priority": priority, 'completed': False}

tasks = []

task_dict = {}

#1) create task

def add_task():
    title = input('Enter task title: ')
    description = input("Enter task description: ")
    due_date = input('Enter task due date: ') 
    priority = int(input('Enter task priority (1-High, 2-Medium, 3-Low): '))
    task = create_task(title, description, due_date, priority)
    task.append(tasks)
    task_dict[title] = task
    print('Task has been successfully added')

#2) do something to the task

#3) listing the tasks

#4) sorting the tasks

#5) truth table check 

#6) search

#7) menu