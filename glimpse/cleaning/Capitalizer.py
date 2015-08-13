class Capitalizer(object):
    '''
    Returns the uppercase version of a field
    '''
    
    def __init__(self, cm):
        self.cm = cm
    
    def cleanValue(self, v):
        if v is not None:
            return v.upper()
        else:
            return None