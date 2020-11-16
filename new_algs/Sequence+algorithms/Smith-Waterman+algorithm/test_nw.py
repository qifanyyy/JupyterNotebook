import re
import unittest

from   itertools import zip_longest
from   functools import partial
from collections import namedtuple

from   uta_align.align.cigar_utils import CigarSequence
from   uta_align.align.algorithms  import align, needleman_wunsch_altshul_erikson


cigar_re = re.compile('([0-9]*)([MIDNSHP=X])')


def grouper(n, iterable, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


def seq_attributes(seq):
    attrs = (a for a in seq.description.split(' ') if '=' in a)
    return dict( tuple(a.split('=',1)) for a in attrs )

FASTARecord = namedtuple('FASTQRecord', 'name sequence')

def simple_fasta_reader(fasta_file):
    name, seq = None, []

    for line in fasta_file:
        line = line.rstrip()

        if line.startswith('>'):
            if name is not None:
                yield FASTARecord(name, ''.join(seq))
            name, seq = line, []
        else:
            seq.append(line)

    if name is not None:
        yield FASTARecord(name, ''.join(seq))

def score_cigar(cigar,  match_score=10, mismatch_score=-8,
                        gap_open_score=-20, gap_extend_score=-1, **extra):

    score = 0
    for op,n in cigar:
        codestr = op.codestr
        if codestr=='M':
            raise ValueError('cannot compute score from generic match operations')
        elif codestr=='=':
            score += n * match_score
        elif codestr=='X':
            score += n * mismatch_score
        elif codestr in 'ID':
            score += gap_open_score + (n-1)*gap_extend_score
        else:
            raise ValueError('unknown op=%s' % codestr)

    return score                        


class TestNeedlemanWunsch(unittest.TestCase):
    methods = [partial(align, mode='global'), needleman_wunsch_altshul_erikson]
    score_params = dict(match_score=10, mismatch_score=-8, gap_open_score=-20, gap_extend_score=-1, extended_cigar=True)

    def setUp(self):
        self.fa = list(simple_fasta_reader('tests/test_nw.fa'))

    def test_needleman_wunsch(self):
        for align_func in self.methods:
            for ref,query in grouper(2, self.fa):
                attrs = seq_attributes(ref)
                attrs.update(seq_attributes(query))

                expected_cigar = attrs['cigar'].replace('M','=')
                ref_seq        = str(ref.seq)
                query_seq      = str(query.seq)
                a              = align_func(ref_seq, query_seq, **self.score_params)
                score2         = align(ref_seq, query_seq, mode='global', score_only=True, **self.score_params).score
                observed_cigar = a.cigar.to_string()
                expected_score = score_cigar(CigarSequence(expected_cigar), **self.score_params)
                observed_score = score_cigar(a.cigar, **self.score_params)

                self.assertEqual( (observed_score, observed_cigar), (expected_score, expected_cigar) )

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

