#! -*- coding: utf-8 -*-
import re

class GeneralCleaning():
    '''
    Applies some general cleanings to fields.
    '''

    def __init__(self):
        self.base_repl = (
        # PULIZIE GENERALI
        (re.compile(r"\b.$",flags=re.I), ''),
        #(re.compile(r"[.\s,]+",flags=re.I), ''),
        (re.compile(r"[.,]+",flags=re.I), ''),  
        (re.compile(r"^\s+",flags=re.I), ''),
        (re.compile(r"\s+$",flags=re.I), ''),
        
        (re.compile(r"\b\s-\s\b",flags=re.I), ''), # deletes ' - '
        (re.compile(r"\"",flags=re.I), ''), # deletes "
        (re.compile(r"[^\&\/A-ZÀÈÉÌÒÙ0-9]",flags=re.I), ' '), 
        (re.compile(r"[^\&\/A-ZÀÈÉÌÒÙ0-9]",flags=re.I), ' '),
        (re.compile(r"^\s+",flags=re.I), ''),
        (re.compile(r"\s+$",flags=re.I), ''),
        (re.compile(r"\s\s+",flags=re.I), ' '),
        
        )
    
    def cleanValue(self, v):
        v2=v
        if v2 is not None:
            for ptrn, repl in self.base_repl:
                v2=re.sub(ptrn, repl, v2)
        return v2
    
        