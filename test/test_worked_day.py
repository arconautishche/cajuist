import unittest
from model.worked_day import WorkedDay, Task

class TestWorkedDay(unittest.TestCase):

    def test_hours_normalization_one(self):
        tasks = [
            Task('PZ--001.001', None, 'Scrum', 0.49),
            Task('PZ--001.001', None, 'Infomeeting', 1.02),
            Task('PZ--999.999', 'AP', 'SVF-1234', 5),
        ]

        day = WorkedDay(tasks)
        day.normalize_hours()

        self.assertEqual(day.tasks[0].duration, 0.5)
        self.assertEqual(day.tasks[1].duration, 1)
        self.assertEqual(day.tasks[2].duration, 5)

    def test_hours_normalization_two(self):
        tasks = [
            Task('PZ--102.102', 'AP', 'SVF-3798', self.__get_hours('00:15:58')),
            Task('PA--300.001', 'AP', 'SVF-9940', self.__get_hours('00:46:10')),
            Task('PA--300.001', 'AP', 'SVF-9740', self.__get_hours('01:44:10')),
            Task('PA--300.001', 'AP', 'SVF-7387', self.__get_hours('01:59:06')),
            Task('PZ--001.001', '', 'Retro', self.__get_hours('01:00:05')),
            Task('PZ--001.001', '', 'Proxy meeting', self.__get_hours('01:00:15')),
            Task('PZ--999.999', 'VS', 'SVF-6516', self.__get_hours('00:40:47')),
            Task('PZ--001.001', '', 'Scrum', self.__get_hours('00:30:06')),
        ]

        day = WorkedDay(tasks)
        day.normalize_hours()

        self.assertEqual(day.tasks[0].duration, 0.25)
        self.assertEqual(day.tasks[1].duration, 0.75)
        self.assertEqual(day.tasks[2].duration, 1.75)
        self.assertEqual(day.total_hours(), 8)

    def __get_hours(self, timestring: str):
        from datetime import datetime
        pt = datetime.strptime(timestring, '%H:%M:%S')
        total_seconds = pt.second + pt.minute*60 + pt.hour*3600
        return total_seconds / 3600

if __name__ == '__main__':
    unittest.main()
