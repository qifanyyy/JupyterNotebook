# -*- mode:python; coding:utf-8; tab-width:4 -*-

from unittest import TestCase

from hamcrest import assert_that, anything, is_
import Ice
from doublex import Mimic, Spy, called, wait_that

from processor import ProcessorI
from loader import OperationsI
import Cannon

from matrix_utils import matrix_multiply

from common import M1, M2, M3, M4


class Broker(object):
    def __init__(self, properties=None):
        properties = properties or []

        data = Ice.InitializationData()
        data.properties = Ice.createProperties()
        for p in properties:
            data.properties.setProperty(p[0], p[1])

        self.communicator = Ice.initialize(data)
        self.adapter = self.communicator.createObjectAdapterWithEndpoints('Adapter', 'tcp')
        self.adapter.activate()

    def add_servant(self, servant, iface):
        proxy = self.adapter.addWithUUID(servant)
        return iface.uncheckedCast(proxy)

    def shutdown(self):
        self.adapter.deactivate()
        self.communicator.shutdown()


class ProcessorObjectTests(TestCase):
    def setUp(self):
        self.broker = Broker([
            ["Ice.ThreadPool.Server.Size", "10"],
            ["Ice.ThreadPool.Client.Size", "10"]])

    def tearDown(self):
        self.broker.shutdown()

    def test_collector_called(self):
        # given
        processor = self.broker.add_servant(ProcessorI(), Cannon.ProcessorPrx)

        collector_servant = Mimic(Spy, Cannon.Collector)
        collector = self.broker.add_servant(collector_servant, Cannon.CollectorPrx)

        A = M2(1, 2, 3, 4)
        B = M2(5, 6, 7, 8)

        # when
        processor.init(1, 1, None, None, 1, collector)
        processor.injectFirst(A, 0)
        processor.injectSecond(B, 0)

        # then
        C = M2(19, 22, 43, 50)
        assert_that(collector_servant.injectSubmatrix,
                    called().asyncio(1).with_args(C, 1, 1, anything()))

    def test_linked_processors(self):
        P0 = self.broker.add_servant(ProcessorI(), Cannon.ProcessorPrx)

        P1_servant = Mimic(Spy, Cannon.Processor)
        P1 = self.broker.add_servant(P1_servant, Cannon.ProcessorPrx)

        P2_servant = Mimic(Spy, Cannon.Processor)
        P2 = self.broker.add_servant(P2_servant, Cannon.ProcessorPrx)

        collector_servant = Mimic(Spy, Cannon.Collector)
        collector = self.broker.add_servant(collector_servant, Cannon.CollectorPrx)

        A00 = M1(1)
        B00 = M1(5)

        P0.init(1, 1, P2, P1, 2, collector)
        P0.injectFirst(A00, 0)
        P0.injectSecond(B00, 0)

        assert_that(P1_servant.injectFirst, called().asyncio(1).with_args(A00, 1, anything()))
        assert_that(P2_servant.injectSecond, called().asyncio(1).with_args(B00, 1, anything()))

    def test_2x2_processors_2x2_operands(self):
        '''
        initial shift:
        1 2     1 2      5 6    5 8
        3 4   < 4 3      7 8    7 6
                                  ^

        processors and collector are distributed objects
        '''
        P = [self.broker.add_servant(ProcessorI(), Cannon.ProcessorPrx) for i in range(4)]

        collector_servant = Mimic(Spy, Cannon.Collector)
        collector = self.broker.add_servant(collector_servant, Cannon.CollectorPrx)

        # by-hand shifted submatrices
        A00 = M1(1)
        A01 = M1(2)
        A10 = M1(4)
        A11 = M1(3)

        B00 = M1(5)
        B01 = M1(8)
        B10 = M1(7)
        B11 = M1(6)

        # by-hand processor initialization
        P[0].init(0, 0, P[2], P[1], 2, collector)
        P[1].init(0, 1, P[3], P[0], 2, collector)
        P[2].init(1, 0, P[0], P[3], 2, collector)
        P[3].init(1, 1, P[1], P[2], 2, collector)

        # by-hand processor loading
        P[0].injectFirst(A00, 0); P[0].injectSecond(B00, 0)
        P[1].injectFirst(A01, 0); P[1].injectSecond(B01, 0)
        P[2].injectFirst(A10, 0); P[2].injectSecond(B10, 0)
        P[3].injectFirst(A11, 0); P[3].injectSecond(B11, 0)

        wait_that(collector_servant.injectSubmatrix,
                  called().times(4))

        # expected result blocks
        C00 = M1(19)
        C01 = M1(22)
        C10 = M1(43)
        C11 = M1(50)

        assert_that(collector_servant.injectSubmatrix, called().with_args(C00, 0, 0, anything()))
        assert_that(collector_servant.injectSubmatrix, called().with_args(C01, 0, 1, anything()))
        assert_that(collector_servant.injectSubmatrix, called().with_args(C10, 1, 0, anything()))
        assert_that(collector_servant.injectSubmatrix, called().with_args(C11, 1, 1, anything()))


class EndToEndTests(TestCase):
    def setUp(self):
        self.broker = Broker([
            ["Ice.ThreadPool.Server.Size", "20"],
            ["Ice.ThreadPool.Client.Size", "20"]])

    def tearDown(self):
        self.broker.shutdown()

    def test_2x2_processors_2x2_operands(self):
        nprocs = 4

        # given
        P = [self.broker.add_servant(ProcessorI(), Cannon.ProcessorPrx) for i in range(nprocs)]
        loader = self.broker.add_servant(OperationsI(P), Cannon.OperationsPrx)

        A = M2(1, 2,
               3, 4)
        B = M2(3, 5,
               1, 0)

        # when
        C = loader.matrixMultiply(A, B)

        # then
        expected = M2(5,  5,
                      13, 15)

        assert_that(C, is_(expected))

    def test_3x3_processors_3x3_operands(self):
        nprocs = 9

        # given
        P = [self.broker.add_servant(ProcessorI(), Cannon.ProcessorPrx) for i in range(nprocs)]
        loader = self.broker.add_servant(OperationsI(P), Cannon.OperationsPrx)

        A = M3(1, 2, 3,
               4, 5, 6,
               7, 8, 9)
        B = M3(10, 11, 12,
               13, 14, 15,
               16, 17, 18)

        # when
        C = loader.matrixMultiply(A, B)

        # then
        expected = M3(84,  90,  96,
                     201, 216, 231,
                     318, 342, 366)

        assert_that(C, is_(expected))

    def test_2x2_processors_4x4_operands(self):
        nprocs = 4

        # given
        P = [self.broker.add_servant(ProcessorI(), Cannon.ProcessorPrx) for i in range(nprocs)]
        loader = self.broker.add_servant(OperationsI(P), Cannon.OperationsPrx)

        A = M4(1,  2,  3,  4,
               5,  6,  7,  8,
               9, 10, 11, 12,
              13, 14, 15, 16)

        B = M4(17, 18, 19, 20,
               21, 22, 23, 24,
               25, 26, 27, 28,
               29, 30, 31, 32)

        # when
        C = loader.matrixMultiply(A, B)

        # then
        expected = M4(250,  260,  270,  280,
                      618,  644,  670,  696,
                      986, 1028, 1070, 1112,
                     1354, 1412, 1470, 1528)

        assert_that(C, is_(expected))

    def test_5x5_processors_200x200_operands(self):
        nprocs = 25

        # given
        P = [self.broker.add_servant(ProcessorI(), Cannon.ProcessorPrx) for i in range(nprocs)]
        loader = self.broker.add_servant(OperationsI(P), Cannon.OperationsPrx)

        A_last = 200 * 200
        A = Cannon.Matrix(200, range(1, 1 + A_last))
        B = Cannon.Matrix(200, range(1 + A_last, 1 + A_last * 2))

        # when
        C = loader.matrixMultiply(A, B)

        # then
        expected = matrix_multiply(A, B)
        assert_that(C, is_(expected))
