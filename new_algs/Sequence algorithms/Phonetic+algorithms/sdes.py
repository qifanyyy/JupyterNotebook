from typing import List

class SDES:


    # 1001001100
    # [True, False, False, False, False, False, True, True, False, False]

    # [False, True, True, True, False, False, True, False]
    # 1 0 1 0 0 0 0 0 1 0
    def __init__(self, key: List[bool] = [True, False, True, False, False, False, False, False, True, False]):
        self.key = key
        self.S0 = {
            '00': {
                '00': '01',
                '01': '00',
                '10': '11',
                '11': '10'
                },
            '01': {
                '00': '11',
                '01': '10',
                '10': '01',
                '11': '00'
                },
            '10': {
                '00': '00',
                '01': '10',
                '10': '01',
                '11': '11'
                },
            '11': {
                '00': '11',
                '01': '01',
                '10': '11',
                '11': '10'
                },
            }
        self.S1 = {
            '00' : {
                '00' : '00',
                '01' : '01',
                '10' : '10',
                '11' : '11'
            },
            '01' : {
                '00' : '10',
                '01' : '00',
                '10' : '01',
                '11' : '11'
            },
            '10' : {
                '00' : '11',
                '01' : '00',
                '10' : '01',
                '11' : '00'
            },
            '11' : {
                '00' : '10',
                '01' : '01',
                '10' : '00',
                '11' : '11'
            }
        }

    # Keys

    def P10(self, key: List[bool]) -> List[bool]:
        p10key = [key[2], key[4], key[1], key[6], key[3], key[9], key[0], key[8], key[7], key[5]]
        return p10key

    def print_key(self, key: List[bool]):
        print(''.join(['1' if bit else '0' for bit in key]))

    def circularLeftShift(self, key: List[bool]) -> List[bool]:
        half1 = key[:len(key) // 2]
        half2 = key[len(key) // 2:]

        first1 = half1.pop(0)
        half1.append(first1)

        first2 = half2.pop(0)
        half2.append(first2)

        concat_key = half1 + half2
        return concat_key

    def P8(self, key: List[bool]) -> List[bool]:
        p8key = [key[5], key[2], key[6], key[3], key[7], key[4], key[9], key[8]]
        return p8key

    def generateKeys(self): 
        p10key = self.P10(self.key)
        ls1 = self.circularLeftShift(p10key)
        p8key1 = self.P8(ls1)
        ls2 = self.circularLeftShift(self.circularLeftShift(ls1))
        p8key2 = self.P8(ls2)

        return p8key1, p8key2

    # Algo

    def IP(self, plain_text: List[bool]) -> List[bool]:
        permuted_text = [plain_text[1], plain_text[5], plain_text[2], plain_text[0], plain_text[3], plain_text[7], plain_text[4], plain_text[6]]
        return permuted_text
    
    def RIP(self, permuted_text: List[bool]) -> List[bool]:
        plain_text = [permuted_text[3], permuted_text[0], permuted_text[2], permuted_text[4], permuted_text[6], permuted_text[1], permuted_text[7], permuted_text[5]]
        return plain_text

    def EPXOR(self, half_text: List[bool], key: List[bool]):
        return [
            half_text[3] ^ key[0],
            half_text[0] ^ key[1],
            half_text[1] ^ key[2],
            half_text[2] ^ key[3],
            half_text[1] ^ key[4],
            half_text[2] ^ key[5],
            half_text[3] ^ key[6],
            half_text[0] ^ key[7],
            ]

    def sandbox0(self, p0: List[bool]):
        line = ''.join(['1' if bit else '0' for bit in [p0[0], p0[3]]])
        column = ''.join(['1' if bit else '0' for bit in [p0[1], p0[2]]])

        bits = self.S0[line][column]
        return [True if bit == '1' else False for bit in [char for char in bits]]

    def sandbox1(self, p1: List[bool]):
        line = ''.join(['1' if bit else '0' for bit in [p1[0], p1[3]]])
        column = ''.join(['1' if bit else '0' for bit in [p1[1], p1[2]]])

        bits = self.S1[line][column]
        return [True if bit == '1' else False for bit in [char for char in bits]]

    def p4(self, part1: List[bool], part2: List[bool]):
        result = [part1[1], part2[1],part2[0], part1[0]]
        return result

    def F(self, right: List[bool], sk: List[bool]):
        resultEPXOR = self.EPXOR(right, sk)
        resultS0 = self.sandbox0(resultEPXOR[:len(resultEPXOR) // 2])
        resultS1 = self.sandbox1(resultEPXOR[len(resultEPXOR) // 2:])
        resultP4 = self.p4(resultS0, resultS1)
        return resultP4

    def fK(self, bits: List[bool], key: List[bool]):
        left = bits[:len(bits) // 2]
        right = bits[len(bits) // 2:]
        resultF = self.F(right, key)
        resultLeft = [left[0] ^ resultF[0], left[1] ^ resultF[1], left[2] ^ resultF[2], left[3] ^ resultF[3]]
        return resultLeft + right

    def SW(self, bits: List[bool]) -> List[bool]:
        left = bits[:len(bits) // 2]
        right = bits[len(bits) // 2:]
        return right + left

    def encrypt(self, char: List[bool]) -> List[bool]:
        key1, key2 = self.generateKeys()
        resultIP = self.IP(char)
        resultFK1 = self.fK(resultIP, key1)
        resultSW = self.SW(resultFK1)
        resultFK2 = self.fK(resultSW, key2)
        resultRIP = self.RIP(resultFK2)
        return resultRIP

    def decrypt(self, char: List[bool]) -> List[bool]:
        key1, key2 = self.generateKeys()
        resultIP = self.IP(char)
        resultFK2 = self.fK(resultIP, key2)
        resultSW = self.SW(resultFK2)
        resultFK1 = self.fK(resultSW, key1)
        resultRIP = self.RIP(resultFK1)
        return resultRIP
    
    def string2bits(self, s=''):
        return [bin(ord(x))[2:].zfill(8) for x in s]

    def bits2string(self, b=None):
        return ''.join([chr(int(x, 2)) for x in b])

    def encrypt_word(self, word: str):
        bits_array = self.string2bits(word)
        encrypted_characters = []
        for bits in bits_array:
            encrypted_bools = self.encrypt([True if bit == '1' else False for bit in bits])
            encrypted_bits_array = ['1' if bit else '0' for bit in encrypted_bools]
            encrypted_bits_string = ''.join(encrypted_bits_array)
            encrypted_char = self.bits2string([encrypted_bits_string])
            encrypted_characters.append(encrypted_char)
        encrypted_word = ''.join(encrypted_characters)
        return encrypted_word

    def decrypt_word(self, word: str):
        decrypted_characters = []
        for bits in self.string2bits(encrypted_word):
            encrypted_bools = [True if bit == '1' else False for bit in bits]
            decrypted_bools = self.decrypt(encrypted_bools)
            decrypted_bits_array = ['1' if bit else '0' for bit in decrypted_bools]
            decrypted_bits_string = ''.join(decrypted_bits_array)
            decrypted_char = self.bits2string([decrypted_bits_string])
            decrypted_characters.append(decrypted_char)
        decrypted_word = ''.join(decrypted_characters)
        return decrypted_word




if __name__ == "__main__":
    sdes = SDES()
    
    encrypted_word = sdes.encrypt_word('hello world!')
    print(encrypted_word)

    decrypted_word = sdes.decrypt_word(encrypted_word)
    print(decrypted_word)
