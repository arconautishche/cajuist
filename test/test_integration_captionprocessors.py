import unittest
from model.spent_time_records import WorkedTask, ICaptionProcessor

class DummyCaptionProcessor(ICaptionProcessor):
    def process_workorder(self, text: str) -> str:
        return text[0]

    def process_activity(self, text: str) -> str:
        return text[1]

    def process_description(self, text: str) -> str:
        return text[2]

class TestIntegrationWorkedTaskWithCaptionProcessor(unittest.TestCase):
    
    def test_processing_applied(self):
        ventouris_processor = DummyCaptionProcessor()
        task = WorkedTask('PZ--001.001', 'VS', 'SVF-1234. Trololo', 1.5, caption_processor=ventouris_processor)

        self.assertEqual(task.workorder, 'P')
        self.assertEqual(task.activity, 'S')
        self.assertEqual(task.description, 'F')

    def test_processing_not_mandatory(self):
        ventouris_processor = DummyCaptionProcessor()
        task = WorkedTask('OrigWO', 'OA', 'Original Description', 1.5)

        self.assertEqual(task.workorder, 'OrigWO')
        self.assertEqual(task.activity, 'OA')
        self.assertEqual(task.description, 'Original Description')

