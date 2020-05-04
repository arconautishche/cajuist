import re

class WorkedTask:
    def __init__(self, workorder: str, activity: str, description: str, hours: float):
        self.workorder = self.__process_workorder(workorder)
        self.description = self.__process_description(description)
        self.hours = self.__process_hours(hours)
        self.activity = self.__process_activity(activity)
        
    def __process_workorder(self, text: str):
        return re.search(r'.*\d', text).group(0)

    def __process_description(self, text: str):
        svf_num = re.search(r'SVF-[\d]{4,}', text)
        if svf_num is not None:
            return svf_num.group(0)
        else:
            return text

    def __process_activity(self, text: str):
        if text is None:
            return ''
        else:
            return text

    def __process_hours(self, hours: float):
        return hours

class WorkedDay:
    def __init__(self, tasks: list):
        self.tasks = tasks.copy()

    def normalize_hours(self):
        for task in self.tasks:
            task.hours = round(task.hours * 4) / 4

    def total_hours(self):
        return sum(task.hours for task in self.tasks)
