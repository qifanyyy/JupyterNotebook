# -*- mode:python; coding:utf-8; tab-width:4 -*-

from unittest import TestCase
from hamcrest import assert_that, is_
from loader import CollectorI
from common import M1, M2, M4


class CollectorServantTests(TestCase):
    """
    These are NOT remote tests. We directly instantiate servants here.
    """
    def test_order_1_block_1x1(self):
        # given
        collector = CollectorI(order=1)

        # when
        M = M1(1)
        collector.injectSubmatrix(M, 0, 0)

        # then
        assert_that(collector.get_result(), is_(M))

    def test_order_4_blocks_1x1(self):
        # given
        collector = CollectorI(order=2)
        collector.injectSubmatrix(M1(1), 0, 0)
        collector.injectSubmatrix(M1(2), 0, 1)
        collector.injectSubmatrix(M1(3), 1, 0)

        # when
        collector.injectSubmatrix(M1(4), 1, 1)

        # then
        assert_that(collector.get_result(), is_(M2(1, 2,
                                                   3, 4)))

    def test_order_4_blocks_2x2(self):
        # given
        collector = CollectorI(order=2)
        collector.injectSubmatrix(M2(1, 2,
                                     5, 6), 0, 0)
        collector.injectSubmatrix(M2(3, 4,
                                     7, 8), 0, 1)
        collector.injectSubmatrix(M2(9, 10,
                                    13, 14), 1, 0)

        # when
        collector.injectSubmatrix(M2(11, 12,
                                     15, 16), 1, 1)

        # then
        expected = M4(1,  2,  3,  4,
                      5,  6,  7,  8,
                      9, 10, 11, 12,
                     13, 14, 15, 16)

        assert_that(collector.get_result(), is_(expected))

    def test_order_4_blocks_1x1_with_missing_blocks(self):
        # given
        collector = CollectorI(order=2)
        collector.injectSubmatrix(M1(1), 0, 0)
        collector.injectSubmatrix(M1(2), 0, 1)
        # block (1,0) never injected

        # when
        collector.injectSubmatrix(M1(4), 1, 1)

        # then
        assert_that(collector.get_result(), is_(None))
