import re
from typing import Tuple

from model.spent_time_records import ICaptionProcessor

class VentourisProcessor(ICaptionProcessor):
    def process_workorder(self, text: str) -> str:
        valid_wo_pattern = r'.*\d'
        wo_match = re.search(valid_wo_pattern, text)
        if wo_match is None:
            raise Exception(f'Workorder is not in a supported format, should match {valid_wo_pattern}')
        
        return wo_match.group(0)

    def process_activity(self, text: str) -> str:
        return text

    def process_description(self, text: str) -> str: 
        untouchable_patterns = [
            r'SVF-8776',
            r'SVF-9402',
            r'SVF-7387'
        ]
        is_untouchable = any(p for p in untouchable_patterns if re.search(p, text))
        if is_untouchable:
            return text

        trimmable_patterns = [
            r'SVF-[\d]{4,}',
            r'USD[\d]{5,}'
        ]
        is_trimmable = any(p for p in trimmable_patterns if re.search(p, text))
        for pattern in trimmable_patterns:
            match = re.search(pattern, text)
            if match is not None:
                return match.group(0)
            else:
                continue

        return text