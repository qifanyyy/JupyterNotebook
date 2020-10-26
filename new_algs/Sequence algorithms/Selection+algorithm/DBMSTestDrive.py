from Database import *


class DBMSTestDrive:
    def __init__(self):
        self.db_system = DBMS()

    def make_relation_r(self):
        self.db_system.make_relation('R', 16 * 8, (1, 40), (1, 1000), 40)

    def make_relation_s(self):
        self.db_system.make_relation('S', 32 * 8, (20, 60), (1, 1000), 60)

    def external_merge_sort(self, rname):
        self.db_system.two_pass_multiway_external_merge_sort(rname)

    def test_indexed_select(self, rname):
        return self.db_system.select(relation=rname, value=40, algorithm='indexed')

    def test_projection(self, rname):
        return self.db_system.do_projection(rname)

    def test_nested_loop_join(self, times):
        true, false = 0, 0
        for i in range(times):
            query_result = self.db_system.join('R', 'S', 'nested_loop_join')
            if self.db_system.check_join('R', 'S', query_result):
                true += 1
            else:
                false += 1
        print("Correct: ", true, "\tWrong: ", false)

    def test_hash_join(self, times):
        true, false = 0, 0
        for i in range(times):
            query_result = self.db_system.join('R', 'S', 'hash_join')
            if self.db_system.check_join('R', 'S', query_result):
                true += 1
            else:
                false += 1
        print("Correct: ", true, "\tWrong: ", false)

    def test_sort_merge_join(self, times):
        true, false = 0, 0
        for i in range(times):
            query_result = self.db_system.join('R', 'S', 'hash_join')
            if self.db_system.check_join('R', 'S', query_result):
                true += 1
            else:
                false += 1
        print("Correct: ", true, "\tWrong: ", false)

    def test(self):
        self.make_relation_r()
        self.make_relation_s()
        self.external_merge_sort('R')
        self.external_merge_sort('S')
        self.test_nested_loop_join(1)
        self.test_hash_join(1)
        self.test_sort_merge_join(1)

if __name__ == '__main__':
    drive = DBMSTestDrive()
    drive.test()
