import unittest

from phonetisch import soundex, caverphone, cologne_phonetics


class TestSoundex(unittest.TestCase):

    def test_encode(self):
        assert soundex.encode_word("Example") == soundex.encode_word("Ekzampul")


class TestCaverphone(unittest.TestCase):
    def test_encode(self):
        assert caverphone.encode_word("Lee") == 'L11111'
        assert caverphone.encode_word("Thompson") == 'TMPSN1'


class TestColognePhonetics(unittest.TestCase):

    def test_algorithm(self):
        word = 'MüllerLüdenscheidt'.upper()
        assert '65752682' == cologne_phonetics.encode_word(word)
