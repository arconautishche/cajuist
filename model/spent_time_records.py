import re

class ICaptionProcessor:
    def process_workorder(self, text: str) -> str:
        pass

    def process_activity(self, text: str) -> str:
        pass

    def process_description(self, text: str) -> str:
        pass

class WorkedTask:
    def __init__(self, workorder: str, activity: str, description: str, hours: float, caption_processor: ICaptionProcessor = None):
        self.processor = caption_processor

        self.workorder = self.__process_workorder(workorder)
        self.description = self.__process_description(description)
        self.hours = self.__process_hours(hours)
        self.activity = self.__process_activity(activity)
        
    def __process_workorder(self, text: str) -> str:
        if not self.processor:
            return text
        
        return self.processor.process_workorder(text)

    def __process_description(self, text: str) -> str:
        if not self.processor:
            return text
        
        return self.processor.process_description(text)

    def __process_activity(self, text: str) -> str:
        if not self.processor:
            return text

        activity = self.processor.process_activity(text)
        if activity is None:
            return ''
        else:
            return activity

    def __process_hours(self, hours: float) -> float:
        return hours

class WorkedDay:
    def __init__(self, tasks: list, caption_processor: ICaptionProcessor = None):
        self.tasks = list(
            WorkedTask(t['workorder'], t['activity'], t['description'], t['hours'], caption_processor=caption_processor) for t in tasks
        )

    def normalize_hours(self):
        for task in self.tasks:
            task.hours = round(task.hours * 4) / 4

    def total_hours(self):
        total_hours = sum(task.hours for task in self.tasks)
        if (total_hours < 0):
            raise Exception(f'Total hours {total_hours} < 0')

        return total_hours
