import re

class ZipcodeParser(object):
    '''
    Extracts a zipcode from a field
    '''
    
    def __init__(self, cm):
        self.cm = cm
        self.zip_pattern = re.compile(r"[0]*(\d{5})",flags=re.I)

    def cleanValue(self, v):
        v2 = None
        if v is not None:
            m = re.search(self.zip_pattern, v)
            if m is not None: # if a zipcode is not found, None is returned
                v2 = m.groups()[0]
        return v2