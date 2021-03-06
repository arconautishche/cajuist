import unittest
from model.ventouris_processor import VentourisProcessor

class TestVentourisProcessor(unittest.TestCase):

    def test_workorder_gets_trimmed(self):
        ventouris_processor = VentourisProcessor()
        self.assertEqual(ventouris_processor.process_workorder('PZ--001.001 - Algemeen'), 'PZ--001.001')
        self.assertEqual(ventouris_processor.process_workorder('PZ--999.999. Gemeenschapelijk'), 'PZ--999.999')
        self.assertEqual(ventouris_processor.process_workorder('PZ--102.102'), 'PZ--102.102')

    def test_description_with_svf_gets_trimmed(self):
        ventouris_processor = VentourisProcessor()
        self.assertEqual(ventouris_processor.process_description('SVF-1234 - Something'), 'SVF-1234')
        self.assertEqual(ventouris_processor.process_description('SVF-1234. Work'), 'SVF-1234')
        self.assertEqual(ventouris_processor.process_description('SVF-12345'), 'SVF-12345')

    def test_description_with_svf8776_untouched(self):
        ventouris_processor = VentourisProcessor()
        untouchable_descr = 'SVF-8776. Fonds'
        self.assertEqual(ventouris_processor.process_description(untouchable_descr), untouchable_descr)

    def test_description_with_usd_gets_trimmed(self):
        ventouris_processor = VentourisProcessor()
        self.assertEqual(ventouris_processor.process_description('USD5595745 - some work'), 'USD5595745')
        self.assertEqual(ventouris_processor.process_description('USD5595745. Work'), 'USD5595745')
        self.assertEqual(ventouris_processor.process_description('USD5595745'), 'USD5595745')

    def test_activity_left_untouched(self):
        ventouris_processor = VentourisProcessor()
        self.assertEqual(ventouris_processor.process_activity('AP'), 'AP')
        self.assertEqual(ventouris_processor.process_activity(''), '')

    def test_workorder_must_match_pattern(self):
        ventouris_processor = VentourisProcessor()
        with self.assertRaises(Exception):
            ventouris_processor.process_workorder('An invalid workorder')

if __name__ == '__main__':
    unittest.main()
