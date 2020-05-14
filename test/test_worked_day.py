import unittest
from model.spent_time_records import WorkedDay, WorkedTask

class TestWorkedDay(unittest.TestCase):

    def test_hours_normalization_one(self):
        tasks = [
            self.__workedTask('PZ--001.001', None, 'Scrum', '00:29:10'),
            self.__workedTask('PZ--001.001', None, 'Infomeeting', '01:02:59'),
            self.__workedTask('PZ--999.999', 'AP', 'SVF-1234', '05:01:00'),
        ]

        day = WorkedDay(tasks)
        day.normalize_hours()

        self.assertEqual(day.tasks[0].hours, 0.5)
        self.assertEqual(day.tasks[1].hours, 1)
        self.assertEqual(day.tasks[2].hours, 5)

    def test_total_duration_after_normalization(self):
        tasks = [
            self.__workedTask('PZ--102.102', 'AP', 'SVF-3798', '00:15:58'),
            self.__workedTask('PA--300.001', 'AP', 'SVF-9940', '00:46:10'),
            self.__workedTask('PA--300.001', 'AP', 'SVF-9740', '01:44:10'),
            self.__workedTask('PA--300.001', 'AP', 'SVF-7387', '01:59:06'),
            self.__workedTask('PZ--001.001', '', 'Retro', '01:00:05'),
            self.__workedTask('PZ--001.001', '', 'Proxy meeting', '01:00:15'),
            self.__workedTask('PZ--999.999', 'VS', 'SVF-6516', '00:40:47'),
            self.__workedTask('PZ--001.001', '', 'Scrum', '00:30:06'),
        ]

        day = WorkedDay(tasks)
        day.normalize_hours()

        self.assertEqual(day.total_hours(), 8)

    def __get_hours(self, timestring: str):
        from datetime import datetime
        pt = datetime.strptime(timestring, '%H:%M:%S')
        total_seconds = pt.second + pt.minute*60 + pt.hour*3600
        return total_seconds / 3600

    def __workedTask(self, wo: str, act: str, descr: str, h: str) -> dict:
        return dict(
            workorder = wo,
            activity = act,
            description = descr,
            hours = self.__get_hours(h)
        )

if __name__ == '__main__':
    unittest.main()
