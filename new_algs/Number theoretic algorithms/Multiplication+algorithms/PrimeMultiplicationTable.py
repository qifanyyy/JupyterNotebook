import math

class PrimeMultiplicationTable(object):

    def get_primes_3(self, num):
        """
        Time Complexity = O(N) Space = O(N)
        """
        if num <= 0:
            return []

        if num == 1:
            return [2]

        size = self.prime_bound(num)

        res = []
        count = 0
        is_prime = [True]*size
        is_prime[0] = False
        is_prime[1] = False

        for i in xrange(2, size):
            if is_prime[i]:
                res.append(i)
                count += 1
                if count == num:
                    break
            
            for j in xrange(0, count):
                if i*res[j] >= size:
                    break
                is_prime[i*res[j]] = False

                if i%res[j] == 0:
                    break

        return res

    def get_primes_2(self, num):
        """
        Time Complexity = O(NloglogN) Space = O(N)
        """
        if num <= 0:
            return []

        if num == 1:
            return [2]

        size = self.prime_bound(num)
        is_prime = [True]*size
        is_prime[0] = False
        is_prime[1] = False
        sqrt_size = int(math.sqrt(size))+1

        for i in range(2, sqrt_size):
            if is_prime[i]:
                for j in range(i*i, size, i):
                    is_prime[j] = False

        res = []
        count = 0
        for j in xrange(0, size):
            if is_prime[j]:
                res.append(j)
                count += 1
                if count == num:
                    break

        return res

    def get_primes_1(self, num):
        """
        Time Complexity < O(n^1.5) Space = O(1)
        """
        if num <= 0:
            return []

        if num == 1:
            return [2]

        res = [2]
        count = 1
        target = 3
        while count < num:
            is_prime = True
            for prime in res:
                if prime > int(math.sqrt(target)):
                    break
                if target % prime == 0:
                    is_prime = False
                    break
            if is_prime:
                res.append(target)
                count += 1
            target += 2

        return res

    def prime_bound(self, num):
        """
        Approximate upper bound of the value of the nth prime
        """
        if num <= 10:
            size = 30
        else:
            factor = 1.3
            size = int(num*math.log(num, math.e)*factor)

        return size        

    def get_primes(self, num):
        return self.get_primes_3(num)

    def print_row(self, nums, name, width):
        items = map(str, nums)
        row = '{0: >{width}}  |'.format(name, width = width + 1)
        for item in items:
            row += '{0: >{width}}'.format(item, width = width + 1)
        print row

    def print_cutting_line(self, length, width):
        print "-"*(length+2)*(width + 1)

    def generate_prime_table(self, num):
        """
        Generate the prime table with dynamic col widths
        """
        if num <= 0 or num is None:
            print "the table is empty"
            return

        primes = self.get_primes(num)

        # Dynamically calculate the maximum col width
        size = self.prime_bound(num)
        max_digits = len(str(size)) * 2

        # Print the header row
        self.print_row(primes, " "*max_digits, max_digits)
        self.print_cutting_line(len(primes), max_digits)

        # Print the muplication table
        for x in primes:
            row = []
            for y in primes:
                row.append(x*y)
            self.print_row(row, x, max_digits) 

if __name__ == "__main__": 
    prime_muplication = PrimeMultiplicationTable()
    prime_muplication.generate_prime_table(10)
