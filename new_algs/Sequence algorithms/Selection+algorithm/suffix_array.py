"""
@author: David Lei
@since: 5/10/2017

Implementation of a suffix array.

Note: There are better complexity methods, however this is just an implementation for understanding.

Creation:
- using radix sort O(n^2)
- using suffix tree O(n * alpha) where alpha is the alphabet size (bounded by 26?).

Resources:
- http://www.cs.jhu.edu/~langmea/resources/lecture_notes/suffix_arrays.pdf
- https://louisabraham.github.io/notebooks/suffix_arrays.html
- https://gist.github.com/prasoon2211/cc3f3d5b43a0885c0e7a
"""

class SuffixArray:
    def __init__(self, string):
        self.suffixes = []
        self.array = []
        self._make_suffix_array(string)

    def _make_suffix_array(self, string):  # O(n^2 log n)
        suffixes = []
        for i in range(len(string)):
            suffixes.append((i, string[i:]))  # Append (index, suffix).
        suffixes.sort(key = lambda t:t[1])  # Sort by suffix.
        self.suffixes = [t[1] for t in suffixes]
        self.array = [t[0] for t in suffixes]

    def pattern_exists(self, pattern):  # O(m (log n + number_of_matches))
        # Returns a single string if the string has a prefix of pattern.
        # If you want a range of strings all with prefix pattern can either return hi and lo and iterate through that
        # which is worst case O(n) or longest common prefix pre processing.
        lo = 0
        hi = len(self.array) - 1

        while hi >= lo:
            mid = (lo + hi) // 2
            if self.suffixes[mid].startswith(pattern):
                return self.suffixes[mid]
            elif self.suffixes[mid] < pattern:
                lo = mid + 1
            else:
                hi = mid - 1
        return None


if __name__ == "__main__":
    s = "bananabatman"
    suffix_array = SuffixArray(s)
    print(suffix_array.pattern_exists("n"))
    print(suffix_array.pattern_exists("batman"))
    print(suffix_array.pattern_exists("bat"))
    print(suffix_array.pattern_exists("man"))
    print(suffix_array.pattern_exists("z"))
    print(suffix_array.pattern_exists("nana"))



