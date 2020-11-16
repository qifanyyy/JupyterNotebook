"""Python implementation of lossless, prefix Huffman coding."""

import heapq


class Huffman:
    """Public instance methods: compress, decompress."""

    def __init__(self, items):
        """Takes a list of items with frequencies and names given. [(f1, n1), (f2, n2)].
        Builds tree according to frequencies and creates Huffman's codes dictionary.
        """
        self.min_heap = items  # [(f1, n1), (f2, n2)]
        heapq.heapify(self.min_heap)

        self.tree = {}  # {parent: [left_child, right_child]}
        self.codes = {}  # {item_name: code}

        self._build_tree()

        # After building a tree, there's only one value left in the min_heap.
        # It's the root, we start extracting codes from.
        self._extract_codes(self.min_heap.pop()[1])

    @staticmethod
    def merge(node_a, node_b):
        """Node object: (frequency, name)"""
        return node_a[0] + node_b[0], node_a[1] + node_b[1]

    def _build_tree(self):
        """Builds tree from leaves to root."""
        while len(self.min_heap) > 1:
            left = heapq.heappop(self.min_heap)
            right = heapq.heappop(self.min_heap)
            parent = self.merge(left, right)

            heapq.heappush(self.min_heap, parent)

            # No need for frequencies in a tree, thus only names are being added.
            self.tree[parent[1]] = [left[1], right[1]]

    def _extract_codes(self, root, code=''):
        """Traverses the tree until all leaves are reached.
        If it heads to a left child, then 0 is added to a code.
        Otherwise 1 is added.
        """
        if root not in self.tree:
            self.codes[root] = code
            return
        for idx, child in enumerate(self.tree[root]):
            self._extract_codes(child, code + str(idx))

    def compress(self, message):
        """Prepends 1 to a bitstring to prevent int from truncating leading zero bits.
        Converts and returns bytes.
        """
        bitstring = '1' + ''.join(map(lambda x: self.codes[x], list(message)))

        num = int(bitstring, 2)
        bit_len = num.bit_length()
        bytes_len = bit_len // 8 if bit_len % 8 == 0 else bit_len // 8 + 1

        return num.to_bytes(bytes_len, byteorder='big')

    def decompress(self, byte_message):
        """Ignores first 3 characters, '0b' and '1', that was prepended during compression.
        Returns an original message.
        """
        bitstring = bin(int.from_bytes(byte_message, byteorder='big'))[3:]

        codes = {v: k for k, v in self.codes.items()}
        message, code = '', ''
        for i in bitstring:
            code += i
            try:
                message += codes[code]
                code = ''
            except KeyError:
                continue

        return message


if __name__ == "__main__":
    from sys import getsizeof

    letters = [(20, ' '), (9, 'e'), (12, 'c'), (13, 'b'), (16, 'd'), (45, 'a'), (5, 'f')]
    huffman = Huffman(letters)

    mes = 'aecd afdcbe fadeb aaaaaaa bbbbbbbbb cccccccc ddddddddd eeeeeeeeee fffffffff' * 10000
    compressed = huffman.compress(mes)

    print("Original message size: {} bytes.".format(getsizeof(mes)))
    print("Compressed message size: {} bytes.".format(getsizeof(compressed)))

    decompressed = huffman.decompress(compressed)
    assert decompressed == mes, 'Original and decompressed messages are not the same.'
