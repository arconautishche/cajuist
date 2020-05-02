import math

class Task:
    def __init__(self, workorder, activity, description, duration):
        self.workorder = workorder
        self.description = description
        self.duration = duration

        if activity is None:
            self.activity = ''
        else:
            self.activity = activity

class WorkedDay:
    def __init__(self, tasks: list):
        self.tasks = tasks.copy()

    def normalize_hours(self):
        for task in self.tasks:
            task.duration = round(task.duration * 4) / 4

    def total_hours(self):
        return sum(task.duration for task in self.tasks)
