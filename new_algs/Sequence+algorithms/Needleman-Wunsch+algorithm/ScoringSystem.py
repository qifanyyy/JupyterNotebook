import pandas as pd

'''
Things to try out:
print(ScoringSystem(load_from_csv=True))
print(ScoringSystem())
print(ScoringSystem(match=10, gap=-5))
'''

class ScoringSystem:
    '''Responsible for returning proper scoring/edit cost values for any letter combination'''

    def __init__(self, match: int=1, mismatch: int=-1, gap: int=-1) -> None:
        self.match = match
        self.mismatch = mismatch
        self.gap = gap
        self.custom_scoring = None

    def load_csv(self, filename: str) -> None:
        self.custom_scoring = pd.read_csv(filename, header=0, index_col=0, sep=' ')

    def _default_scoring(self, a: str, b: str) -> int:
        '''Checks if there's a match/mismatch/gap for letters a and b'''
        if a == b:
            return self.match
        elif a == '-' or b == '-':
            return self.gap
        return self.mismatch

    def score(self, a: str, b: str) -> int:
        '''This method should be used by algorithms'''
        assert isinstance(a, str) and isinstance(b, str)
        assert len(a) == 1 and len(b) == 1

        # Use CSV file
        if self.custom_scoring is not None:
            try:
                return self.custom_scoring[a][b]
            except KeyError:
                print(f'WARNING: Key not found. You using defaults: {self.__str__}')
                # In case some letter was not present in CSV file, use default scoring value
                return self._default_scoring(a, b)
        # Simply use match/mismatch/gap values
        else:
            return self._default_scoring(a, b)
        
    def __str__(self):
        if self.custom_scoring is not None:
            # Use pandas DataFrame __str__ representation
            return str(self.custom_scoring)
        return f'Match: {self.match}, Mismatch: {self.mismatch}, Gap: {self.gap}'
