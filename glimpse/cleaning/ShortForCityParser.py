import re

class ShortForCityParser(object):
    '''
    Extracts the short names for cities, es: (MI) from
    complex strings, removing the brakets.
    '''

    def __init__(self, cm):
        self.cm = cm
        self.zip_pattern = re.compile(r"\(([A-Z]{2})\)",flags=re.I)
    
    def cleanValue(self, v):
        v2 = None
        if v is not None:
            m = re.search(self.zip_pattern, v)
            if m is not None: # if a city is not found, None is returned
                v2 = m.groups()[0]
        return v2