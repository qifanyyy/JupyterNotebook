# -*- mode:python; coding:utf-8; tab-width:4 -*-

from unittest import TestCase

from hamcrest import assert_that, anything
from doublex import Spy, Stub, called, ANY_ARG

import Ice
Ice.loadSlice('-I {} cannon.ice'.format(Ice.getSliceDir()))
import Cannon

from processor import ProcessorI

from common import M1, M2


class ProcessorServantTests(TestCase):
    """
    These are NOT remote tests. We directly instantiate servants here.
    """
    def test_processors_rings(self):
        # given
        P0 = ProcessorI()
        P1 = Spy()
        P2 = Spy()
        collector = Stub()

        A0 = M1(1)
        B0 = M1(5)

        # when
        P0.init(1, 1, P2, P1, 2, collector)
        P0.injectFirst(A0, 0)
        P0.injectSecond(B0, 0)

        # then
        assert_that(P1.injectFirst, called().async(1).with_args(A0, 1, ANY_ARG))
        assert_that(P2.injectSecond, called().async(1).with_args(B0, 1, ANY_ARG))

    def assert_collector_called(self, collector, *args):
        assert_that(collector.injectSubmatrix,
                    called().with_args(*args))

    def test_2x2_processors_1x1_blocks_with_collector_injection(self):
        '''
        A = (1, 2,
             3, 4)

        B = (5, 6,
             7, 8)
        '''
        nprocs = 4

        # given
        P = [ProcessorI() for i in range(nprocs)]
        collector = Spy(Cannon.Collector)

        # by-hand shift and split
        A0 = M1(1)
        A1 = M1(2)
        A2 = M1(4)
        A3 = M1(3)

        B0 = M1(5)
        B1 = M1(8)
        B2 = M1(7)
        B3 = M1(6)

        # when
        P[0].init(0, 0, P[2], P[1], 2, collector)
        P[1].init(0, 1, P[3], P[0], 2, collector)
        P[2].init(1, 0, P[0], P[3], 2, collector)
        P[3].init(1, 1, P[1], P[2], 2, collector)

        P[0].injectFirst(A0, 0); P[0].injectSecond(B0, 0)
        P[1].injectFirst(A1, 0); P[1].injectSecond(B1, 0)
        P[2].injectFirst(A2, 0); P[2].injectSecond(B2, 0)
        P[3].injectFirst(A3, 0); P[3].injectSecond(B3, 0)

        # then
        C0 = M1(19)
        C1 = M1(22)
        C2 = M1(43)
        C3 = M1(50)

        self.assert_collector_called(collector, C0, 0, 0, anything())
        self.assert_collector_called(collector, C1, 0, 1, anything())
        self.assert_collector_called(collector, C2, 1, 0, anything())
        self.assert_collector_called(collector, C3, 1, 1, anything())

    def test_2x2_processors_2x2_blocks_with_collector_injection(self):
        '''
        A = (1,  2,  3,  4,
             5,  6,  7,  8,
             9, 10, 11, 12,
            13, 14, 15, 16)

        B = (17, 18, 19, 20,
             21, 22, 23, 24,
             25, 26, 27, 28,
             29, 30, 31, 32)
        '''
        nprocs = 4

        # given
        P = [ProcessorI() for i in range(nprocs)]
        collector = Spy(Cannon.Collector)

        # by-hand shift and split
        A0 = M2(1, 2,
                5, 6)

        A1 = M2(3, 4,
                7, 8)

        A2 = M2(11, 12,
                15, 16)

        A3 = M2(9, 10,
               13, 14)

        B0 = M2(17, 18,
                21, 22)

        B1 = M2(27, 28,
                31, 32)

        B2 = M2(25, 26,
                29, 30)

        B3 = M2(19, 20,
                23, 24)

        # when
        P[0].init(0, 0, P[2], P[1], 2, collector)
        P[1].init(0, 1, P[3], P[0], 2, collector)
        P[2].init(1, 0, P[0], P[3], 2, collector)
        P[3].init(1, 1, P[1], P[2], 2, collector)

        P[0].injectFirst(A0, 0); P[0].injectSecond(B0, 0)
        P[1].injectFirst(A1, 0); P[1].injectSecond(B1, 0)
        P[2].injectFirst(A2, 0); P[2].injectSecond(B2, 0)
        P[3].injectFirst(A3, 0); P[3].injectSecond(B3, 0)

        # then
        C0 = M2(250, 260,
                618, 644)

        C1 = M2(270, 280,
                670, 696)

        C2 = M2(986, 1028,
                1354, 1412)

        C3 = M2(1070, 1112,
                1470, 1528)

        self.assert_collector_called(collector, C0, 0, 0, anything())
        self.assert_collector_called(collector, C1, 0, 1, anything())
        self.assert_collector_called(collector, C2, 1, 0, anything())
        self.assert_collector_called(collector, C3, 1, 1, anything())

    def test_3x3_processors_1x1_blocks_with_collector_injection(self):
        '''
        A = (1, 2, 3,
             4, 5, 6,
             7, 8, 9)


        B = (10, 11, 12,
             13, 14, 15,
             16, 17, 18)
        '''
        nprocs = 9

        # given
        P = [ProcessorI() for i in range(nprocs)]
        collector = Spy(Cannon.Collector)

        # by-hand shift and split
        A0 = M1(1)
        A1 = M1(2)
        A2 = M1(3)
        A3 = M1(5)
        A4 = M1(6)
        A5 = M1(4)
        A6 = M1(9)
        A7 = M1(7)
        A8 = M1(8)

        B0 = M1(10)
        B1 = M1(14)
        B2 = M1(18)
        B3 = M1(13)
        B4 = M1(17)
        B5 = M1(12)
        B6 = M1(16)
        B7 = M1(11)
        B8 = M1(15)

        # when
        P[0].init(0, 0, P[6], P[2], 3, collector)
        P[1].init(0, 1, P[7], P[0], 3, collector)
        P[2].init(0, 2, P[8], P[1], 3, collector)
        P[3].init(1, 0, P[0], P[5], 3, collector)
        P[4].init(1, 1, P[1], P[3], 3, collector)
        P[5].init(1, 2, P[2], P[4], 3, collector)
        P[6].init(2, 0, P[3], P[8], 3, collector)
        P[7].init(2, 1, P[4], P[6], 3, collector)
        P[8].init(2, 2, P[5], P[7], 3, collector)

        P[0].injectFirst(A0, 0); P[0].injectSecond(B0, 0)
        P[1].injectFirst(A1, 0); P[1].injectSecond(B1, 0)
        P[2].injectFirst(A2, 0); P[2].injectSecond(B2, 0)
        P[3].injectFirst(A3, 0); P[3].injectSecond(B3, 0)
        P[4].injectFirst(A4, 0); P[4].injectSecond(B4, 0)
        P[5].injectFirst(A5, 0); P[5].injectSecond(B5, 0)
        P[6].injectFirst(A6, 0); P[6].injectSecond(B6, 0)
        P[7].injectFirst(A7, 0); P[7].injectSecond(B7, 0)
        P[8].injectFirst(A8, 0); P[8].injectSecond(B8, 0)

        # then
        C0 = M1(84)
        C1 = M1(90)
        C2 = M1(96)
        C3 = M1(201)
        C4 = M1(216)
        C5 = M1(231)
        C6 = M1(318)
        C7 = M1(342)
        C8 = M1(366)

        self.assert_collector_called(collector, C0, 0, 0, anything())
        self.assert_collector_called(collector, C1, 0, 1, anything())
        self.assert_collector_called(collector, C2, 0, 2, anything())
        self.assert_collector_called(collector, C3, 1, 0, anything())
        self.assert_collector_called(collector, C4, 1, 1, anything())
        self.assert_collector_called(collector, C5, 1, 2, anything())
        self.assert_collector_called(collector, C6, 2, 0, anything())
        self.assert_collector_called(collector, C7, 2, 1, anything())
        self.assert_collector_called(collector, C8, 2, 2, anything())
