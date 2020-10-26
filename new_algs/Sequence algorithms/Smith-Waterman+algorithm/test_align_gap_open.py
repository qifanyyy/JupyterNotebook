import doctest

from uta_align.align.algorithms import align, needleman_wunsch_altshul_erikson

def test_gap_open():
    '''
    >>> ref   = b'TCCCTCAAGTCCTTCCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAACAGCCGCCACCGCCGCCGCCGCCGCCGCCGCCTCCTC'
    >>> query = b'TCCCTCAAGTCCTTCCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAACAGCCGCCACCGCCGCCGCCGCCGCCGCCGCCTCCTC'

    >>> a = align(ref, query, b'local', match_score=10, mismatch_score=-9, gap_open_score=-100, gap_extend_score=-6)
    >>> a.score
    930
    >>> a.cigar.to_string() # 1
    b'15M6D91M'

    >>> aref, aquery = a.gapped_alignment()
    >>> aref
    b'TCCCTCAAGTCCTTCCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAACAGCCGCCACCGCCGCCGCCGCCGCCGCCGCCTCCTC'
    >>> aquery
    b'...............------...........................................................................................'

    >>> a = align(ref, query, b'glocal', match_score=10, mismatch_score=-9, gap_open_score=-100, gap_extend_score=-6)
    >>> a.score
    930
    >>> a.cigar.to_string() # 2
    b'15M6D91M'

    >>> aref, aquery = a.gapped_alignment()
    >>> aref
    b'TCCCTCAAGTCCTTCCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAACAGCCGCCACCGCCGCCGCCGCCGCCGCCGCCTCCTC'
    >>> aquery
    b'...............------...........................................................................................'

    >>> a = align(ref, query, b'global', match_score=10, mismatch_score=-9, gap_open_score=-100, gap_extend_score=-6)
    >>> a.score
    930
    >>> a.cigar.to_string() # 3
    b'15M6D91M'

    >>> aref, aquery = a.gapped_alignment()
    >>> aref
    b'TCCCTCAAGTCCTTCCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAACAGCCGCCACCGCCGCCGCCGCCGCCGCCGCCTCCTC'
    >>> aquery
    b'...............------...........................................................................................'

    >>> a = align(ref, query, b'local_global', match_score=10, mismatch_score=-9, gap_open_score=-100, gap_extend_score=-6)
    >>> a.score
    930
    >>> a.cigar.to_string() # 4
    b'15M6D91M'

    >>> aref, aquery = a.gapped_alignment()
    >>> aref
    b'TCCCTCAAGTCCTTCCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAACAGCCGCCACCGCCGCCGCCGCCGCCGCCGCCTCCTC'
    >>> aquery
    b'...............------...........................................................................................'

    >>> a = needleman_wunsch_altshul_erikson(ref, query, match_score=10, mismatch_score=-9, gap_open_score=-100, gap_extend_score=-6)
    >>> a.score
    930
    >>> a.cigar.to_string() # 5
    b'15M6D91M'

    >>> aref, aquery = a.gapped_alignment()
    >>> aref
    b'TCCCTCAAGTCCTTCCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAACAGCCGCCACCGCCGCCGCCGCCGCCGCCGCCTCCTC'
    >>> aquery
    b'...............------...........................................................................................'
    '''


if __name__ == '__main__':
    results = doctest.testmod()
    assert not results.failed

## <LICENSE>
## Copyright 2014-2020 uta-align Contributors (https://github.com/biocommons/uta-align)
## 
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
## 
##     http://www.apache.org/licenses/LICENSE-2.0
## 
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
## </LICENSE>

