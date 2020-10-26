class Decipher:
    def __init__(self):
        self.message = ''

    @staticmethod
    def get_value(table, pos):
        """
        used to get a cell at a given table position, if the position is outside the range of table,
        return a default cell value

        a cell is defined as a list where:
        [int: length of lcs of str1[:i] and str2[:j],
        list: reference to the cell of previous matched character,
        string: currently matched character, None if not matched,
        bool: allow adding to substring from left,
        bool: allow adding to substring from top ]

        time complexity: O(1)       retrieve from list is constant time
        space complexity: O(1)      return list of length 5, constant
        :param table:   DP table
        :param pos:     tuple of x and y location
        :return:        cell list
        """
        if pos[0] < 0 or pos[1] < 0:
            return [0, None, None, True, True]
        return table[pos[0]][pos[1]]

    def messageFind(self, f_name):
        """
        finds the longest common substring in the two strings found in the file f_name

        n = len(str1)
        m = len(str2)

        time complexity: O(nm)
        creates a DP table with n rows, each m cells. the algorithm iterates through each cell and use constant time to
        calculate the value of the cell.
        reconstructing the string takes maximum of min(n,m).

        space complexity: O(nm)
        the table is n x m and each cell is of constant space complexity
        :param f_name:  path or file
        :return:        None, set self.message
        """

        # cell: [max length, link to previous chr, matched chr, allow horizontal add, allow vertical add]

        with open(f_name, "r") as file:
            str1 = file.readline().strip()
            str2 = file.readline().strip()

        table = []
        for i in range(len(str1)):
            table.append([])
            for j in range(len(str2)):
                left = self.get_value(table, (i,j-1))
                top = self.get_value(table, (i-1,j))
                diagonal = self.get_value(table, (i-1, j-1))

                if str1[i] == str2[j] and (left[3] or top[4] or diagonal[0]+1 > max(left[0], top[0])):
                    cells = [[diagonal[0]+1, diagonal if diagonal[2] else diagonal[1], str1[i], False, False]]
                    if left[3]:
                        cells.append([left[0] + 1, left[1], str1[i], False, False])
                    if top[4]:
                        cells.append([top[0] + 1, top[1], str1[i], False, False])
                    max_cell = cells[0]
                    for cell in cells:
                        if cell[0] > max_cell[0]:
                            max_cell = cell
                    table[i].append(max_cell)
                else:
                    if top[0] > left[0]:
                        table[i].append([top[0], top if top[2] else top[1], None, True, top[4]])
                    else:
                        table[i].append([left[0], left if left[2] else left[1], None, left[3], True])

        current = table[-1][-1]
        chars = [""]*current[0]
        while current:
            if current[2]:
                chars[current[0]-1] = current[2]
            current = current[1]
        self.message = "".join(chars)

    def equal(self, word, i):
        """
        check if the input word is equal to the substring of self.message, generated from message find
        starting at location i

        time complexity: O(M)       worst case have to check the full length of the word
        space complexity: O(M)      for storing the word, auxiliary space complexity is constant
        :param word:    word from dictionary
        :param i:       index of substring
        :return:        True or False
        """

        if len(word) + i > len(self.message):
            return False
        for j in range(len(word)):
            if word[j] != self.message[i+j]:
                return False
        return True

    def wordBreak(self, f_name):
        """
        Finds the best fit for a combination of words from the dictionary to the unspaced message

        each element of the list:
        [length of the current word matched with, index of where the next word begins]

        time complexity: O(kNM)
        for every word in the dictionary (N):
            iterate through letters in the unspaced message twice,
            first pass(k):
                check if the string is equal to the current word (M)
            second pass: combine with the results of previous word(k)

        space complexity: O(k + NM)
        requires NM to store the dictionary words
        requires two lists of length k, each element is a list of size 2. did not use a table as only the previous row
        was required.
        :param f_name:  file name of dictionary (str)
        :return:        None, set self.message
        """
        words = []
        with open(f_name, "r") as file:
            for line in file:
                words.append(line.strip())

        current = [[0, i+1] for i in range(len(self.message))]
        for word in words:
            previous = current
            current = [[0, i+1] for i in range(len(self.message))]

            # populate current with information if match with word
            i = 0
            while i < len(self.message):
                if self.equal(word, i):
                    cell = [len(word), i + len(word)]
                    for j in range(len(word)):
                        current[i+j] = cell
                    i += len(word)
                else:
                    i += 1

            # compare and merge with previous for each section
            i = 0
            while i < len(self.message):
                section_len = 1     # length of the section
                prev_len = 0        # number of matched characters in the previous section
                prev_pos = 0        # next j position to check (where the next word begins in previous)
                prev_words = 0      # number of words in previous
                curr_len = 0
                curr_pos = 0
                curr_words = 0
                j = 0
                while j < section_len:
                    if j == prev_pos:                                           # if start of word in previous
                        prev_len += previous[i+j][0]                            # increment total length of prev section
                        prev_pos = previous[i+j][1] - i                         # set next position to check
                        prev_words += 1                                         # increment word count
                        section_len = max(section_len, previous[i+j][1]-i)      # extend the section if needed
                    if j == curr_pos:
                        curr_len += current[i+j][0]
                        curr_pos = current[i+j][1] - i
                        prev_words += 1
                        section_len = max(section_len, current[i+j][1]-i)
                    j = min(prev_pos, curr_pos)                                 # increment j to next required position
                # if the previous section is better than the current section
                if prev_len > curr_len or (prev_len == curr_len and prev_words < curr_words):
                    for k in range(section_len):
                        current[i+k] = previous[i+k]
                i += j              # set i to start of next section

        # concatenate the words
        chars = []
        last = 0
        i = 0
        while i < len(current):
            if (last != 0 or current[i][0] != 0) and i:
                chars.append(" ")
            for j in range(i, current[i][1]):
                chars.append(self.message[j])
            last = current[i][0]
            i = current[i][1]
        self.message = "".join(chars)

    def getMessage(self):
        return self.message


if __name__ == "__main__":
    encr = input("The name of the file, contains two encrypted texts : ")
    dict = input("The name of the dictionary file : ")
    print("---------------------------------------------------------------------")
    d = Decipher()
    d.messageFind(encr)
    print("Deciphered message is " + d.getMessage())
    d.wordBreak(dict)
    print("True message is " + d.getMessage())

    print("---------------------------------------------------------------------")
    print("Program end")
