class WorkedTask:
    def __init__(self, workorder, activity, description, hours):
        self.workorder = workorder
        self.description = description
        self.hours = hours

        if activity is None:
            self.activity = ''
        else:
            self.activity = activity

class WorkedDay:
    def __init__(self, tasks: list):
        self.tasks = tasks.copy()

    def normalize_hours(self):
        for task in self.tasks:
            task.hours = round(task.hours * 4) / 4

    def total_hours(self):
        return sum(task.hours for task in self.tasks)
