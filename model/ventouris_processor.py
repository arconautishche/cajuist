import re
from typing import Tuple

from model.worked_day import ICaptionProcessor

class VentourisProcessor(ICaptionProcessor):
    def process_workorder(self, text: str) -> str:
        return re.search(r'.*\d', text).group(0)

    def process_activity(self, text: str) -> str:
        pass

    def process_description(self, text: str) -> str:
        untouchable_patterns = [
            r'SVF-8776',
            r'SVF-9402'
        ]

        is_untouchable = any(p for p in untouchable_patterns if re.search(p, text))
        if is_untouchable:
            return text

        svf_num = re.search(r'SVF-[\d]{4,}', text)
        if svf_num is not None:
            return svf_num.group(0)
        else:
            return text

    # def __untouchable(self, text: str) -> Tuple[bool, str]:
    #     untouchable_patterns = [
    #         r'SVF-8776',
    #         r'SVF-9402'
    #     ]

    #     is_untouchable = any(p for p in untouchable_patterns if re.search(p, text))
    #     if is_untouchable:
    #         return (True, text)
        
    #     return (False, text)
