import unittest
from model.worked_day import WorkedTask

class TestWorkedTask(unittest.TestCase):

    def test_workorder_gets_trimmed(self):
        task_w_dash = WorkedTask('PZ--001.001 - Algemeen', '', '', 0.5)
        self.assertEqual(task_w_dash.workorder, 'PZ--001.001')

        task_w_dot = WorkedTask('PZ--999.999. Gemeenschapelijk', '', '', 0.5)
        self.assertEqual(task_w_dot.workorder, 'PZ--999.999')

        task_clean = WorkedTask('PZ--102.102', '', '', 0.5)
        self.assertEqual(task_clean.workorder, 'PZ--102.102')

    def test_description_with_svf_gets_trimmed(self):
        task_w_dash = WorkedTask('PZ--001.001', '', 'SVF-1234 - Something', 0.5)
        self.assertEqual(task_w_dash.description, 'SVF-1234')

        task_w_dot = WorkedTask('PZ--001.001', '', 'SVF-1234. Work', 0.5)
        self.assertEqual(task_w_dot.description, 'SVF-1234')

        task_clean = WorkedTask('PZ--102.102', '', 'SVF-1234', 0.5)
        self.assertEqual(task_clean.description, 'SVF-1234')

if __name__ == '__main__':
    unittest.main()
