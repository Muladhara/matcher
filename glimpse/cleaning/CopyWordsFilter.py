class CopyWordsFilter():
    '''
    A cleaning criterion that simply copies a field.
    Used as default case
    '''

    def cleanValue(self, v):
        return v