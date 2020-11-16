# Generated from /home/zetsubou/Projects/Python/Simplex method/m.g4 by ANTLR 4.7
# encoding: utf-8
import sys
from io import StringIO

from antlr4 import *
from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\17")
        buf.write("C\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\3\2")
        buf.write("\3\2\3\2\7\2\22\n\2\f\2\16\2\25\13\2\3\3\3\3\3\3\7\3\32")
        buf.write("\n\3\f\3\16\3\35\13\3\3\4\3\4\3\4\7\4\"\n\4\f\4\16\4%")
        buf.write("\13\4\3\5\7\5(\n\5\f\5\16\5+\13\5\3\6\3\6\3\6\3\6\3\6")
        buf.write("\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\5")
        buf.write("\6?\n\6\3\7\3\7\3\7\2\2\b\2\4\6\b\n\f\2\5\3\2\7\n\3\2")
        buf.write("\f\r\3\2\5\6\2D\2\16\3\2\2\2\4\26\3\2\2\2\6\36\3\2\2\2")
        buf.write("\b)\3\2\2\2\n>\3\2\2\2\f@\3\2\2\2\16\23\5\4\3\2\17\20")
        buf.write("\t\2\2\2\20\22\5\4\3\2\21\17\3\2\2\2\22\25\3\2\2\2\23")
        buf.write("\21\3\2\2\2\23\24\3\2\2\2\24\3\3\2\2\2\25\23\3\2\2\2\26")
        buf.write("\33\5\6\4\2\27\30\t\3\2\2\30\32\5\6\4\2\31\27\3\2\2\2")
        buf.write("\32\35\3\2\2\2\33\31\3\2\2\2\33\34\3\2\2\2\34\5\3\2\2")
        buf.write("\2\35\33\3\2\2\2\36#\5\n\6\2\37 \7\16\2\2 \"\5\n\6\2!")
        buf.write("\37\3\2\2\2\"%\3\2\2\2#!\3\2\2\2#$\3\2\2\2$\7\3\2\2\2")
        buf.write("%#\3\2\2\2&(\t\3\2\2\'&\3\2\2\2(+\3\2\2\2)\'\3\2\2\2)")
        buf.write("*\3\2\2\2*\t\3\2\2\2+)\3\2\2\2,-\5\b\5\2-.\7\5\2\2.?\3")
        buf.write("\2\2\2/\60\5\b\5\2\60\61\7\6\2\2\61?\3\2\2\2\62\63\5\b")
        buf.write("\5\2\63\64\7\13\2\2\64?\3\2\2\2\65\66\5\b\5\2\66\67\7")
        buf.write("\3\2\2\678\5\2\2\289\7\4\2\29?\3\2\2\2:;\5\b\5\2;<\t\4")
        buf.write("\2\2<=\7\13\2\2=?\3\2\2\2>,\3\2\2\2>/\3\2\2\2>\62\3\2")
        buf.write("\2\2>\65\3\2\2\2>:\3\2\2\2?\13\3\2\2\2@A\5\2\2\2A\r\3")
        buf.write("\2\2\2\7\23\33#)>")
        return buf.getvalue()


class mParser(Parser):
    grammarFileName = "m.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [DFA(ds, i) for i, ds in enumerate(atn.decisionToState)]

    sharedContextCache = PredictionContextCache()

    literalNames = ["<INVALID>", "'('", "')'", "<INVALID>", "<INVALID>",
                    "'>'", "'>='", "'<'", "'<='", "'m'", "'+'", "'-'",
                    "'*'"]

    symbolicNames = ["<INVALID>", "<INVALID>", "<INVALID>", "INT", "FLOAT",
                     "GT", "GE", "LT", "LE", "M", "ADD", "SUB", "MUL",
                     "WS"]

    RULE_expression = 0
    RULE_op_add = 1
    RULE_op_mul = 2
    RULE_dummy_unary_add = 3
    RULE_atom = 4
    RULE_start_rule = 5

    ruleNames = ["expression", "op_add", "op_mul", "dummy_unary_add",
                 "atom", "start_rule"]

    EOF = Token.EOF
    T__0 = 1
    T__1 = 2
    INT = 3
    FLOAT = 4
    GT = 5
    GE = 6
    LT = 7
    LE = 8
    M = 9
    ADD = 10
    SUB = 11
    MUL = 12
    WS = 13

    def __init__(self, input: TokenStream, output: TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None

    class ExpressionContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def op_add(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(mParser.Op_addContext)
            else:
                return self.getTypedRuleContext(mParser.Op_addContext, i)

        def GT(self, i: int = None):
            if i is None:
                return self.getTokens(mParser.GT)
            else:
                return self.getToken(mParser.GT, i)

        def LT(self, i: int = None):
            if i is None:
                return self.getTokens(mParser.LT)
            else:
                return self.getToken(mParser.LT, i)

        def GE(self, i: int = None):
            if i is None:
                return self.getTokens(mParser.GE)
            else:
                return self.getToken(mParser.GE, i)

        def LE(self, i: int = None):
            if i is None:
                return self.getTokens(mParser.LE)
            else:
                return self.getToken(mParser.LE, i)

        def getRuleIndex(self):
            return mParser.RULE_expression

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitExpression"):
                return visitor.visitExpression(self)
            else:
                return visitor.visitChildren(self)

    def expression(self):

        localctx = mParser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_expression)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 12
            self.op_add()
            self.state = 17
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and (
                (1 << _la) & ((1 << mParser.GT) | (1 << mParser.GE) | (1 << mParser.LT) | (1 << mParser.LE))) != 0):
                self.state = 13
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & (
                            (1 << mParser.GT) | (1 << mParser.GE) | (1 << mParser.LT) | (1 << mParser.LE))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 14
                self.op_add()
                self.state = 19
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Op_addContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def op_mul(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(mParser.Op_mulContext)
            else:
                return self.getTypedRuleContext(mParser.Op_mulContext, i)

        def ADD(self, i: int = None):
            if i is None:
                return self.getTokens(mParser.ADD)
            else:
                return self.getToken(mParser.ADD, i)

        def SUB(self, i: int = None):
            if i is None:
                return self.getTokens(mParser.SUB)
            else:
                return self.getToken(mParser.SUB, i)

        def getRuleIndex(self):
            return mParser.RULE_op_add

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitOp_add"):
                return visitor.visitOp_add(self)
            else:
                return visitor.visitChildren(self)

    def op_add(self):

        localctx = mParser.Op_addContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_op_add)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 20
            self.op_mul()
            self.state = 25
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == mParser.ADD or _la == mParser.SUB:
                self.state = 21
                _la = self._input.LA(1)
                if not (_la == mParser.ADD or _la == mParser.SUB):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 22
                self.op_mul()
                self.state = 27
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Op_mulContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def atom(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(mParser.AtomContext)
            else:
                return self.getTypedRuleContext(mParser.AtomContext, i)

        def MUL(self, i: int = None):
            if i is None:
                return self.getTokens(mParser.MUL)
            else:
                return self.getToken(mParser.MUL, i)

        def getRuleIndex(self):
            return mParser.RULE_op_mul

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitOp_mul"):
                return visitor.visitOp_mul(self)
            else:
                return visitor.visitChildren(self)

    def op_mul(self):

        localctx = mParser.Op_mulContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_op_mul)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 28
            self.atom()
            self.state = 33
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == mParser.MUL:
                self.state = 29
                self.match(mParser.MUL)
                self.state = 30
                self.atom()
                self.state = 35
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Dummy_unary_addContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ADD(self, i: int = None):
            if i is None:
                return self.getTokens(mParser.ADD)
            else:
                return self.getToken(mParser.ADD, i)

        def SUB(self, i: int = None):
            if i is None:
                return self.getTokens(mParser.SUB)
            else:
                return self.getToken(mParser.SUB, i)

        def getRuleIndex(self):
            return mParser.RULE_dummy_unary_add

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitDummy_unary_add"):
                return visitor.visitDummy_unary_add(self)
            else:
                return visitor.visitChildren(self)

    def dummy_unary_add(self):

        localctx = mParser.Dummy_unary_addContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_dummy_unary_add)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 39
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == mParser.ADD or _la == mParser.SUB:
                self.state = 36
                _la = self._input.LA(1)
                if not (_la == mParser.ADD or _la == mParser.SUB):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 41
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class AtomContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.p = None  # Dummy_unary_addContext
            self.i = None  # Token
            self.f = None  # Token
            self.m = None  # Token
            self.e = None  # ExpressionContext
            self.c = None  # Token
            self.m2 = None  # Token

        def dummy_unary_add(self):
            return self.getTypedRuleContext(mParser.Dummy_unary_addContext, 0)

        def INT(self):
            return self.getToken(mParser.INT, 0)

        def FLOAT(self):
            return self.getToken(mParser.FLOAT, 0)

        def M(self):
            return self.getToken(mParser.M, 0)

        def expression(self):
            return self.getTypedRuleContext(mParser.ExpressionContext, 0)

        def getRuleIndex(self):
            return mParser.RULE_atom

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitAtom"):
                return visitor.visitAtom(self)
            else:
                return visitor.visitChildren(self)

    def atom(self):

        localctx = mParser.AtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_atom)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 60
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 4, self._ctx)
            if la_ == 1:
                self.state = 42
                localctx.p = self.dummy_unary_add()
                self.state = 43
                localctx.i = self.match(mParser.INT)
                pass

            elif la_ == 2:
                self.state = 45
                localctx.p = self.dummy_unary_add()
                self.state = 46
                localctx.f = self.match(mParser.FLOAT)
                pass

            elif la_ == 3:
                self.state = 48
                localctx.p = self.dummy_unary_add()
                self.state = 49
                localctx.m = self.match(mParser.M)
                pass

            elif la_ == 4:
                self.state = 51
                localctx.p = self.dummy_unary_add()
                self.state = 52
                self.match(mParser.T__0)
                self.state = 53
                localctx.e = self.expression()
                self.state = 54
                self.match(mParser.T__1)
                pass

            elif la_ == 5:
                self.state = 56
                localctx.p = self.dummy_unary_add()
                self.state = 57
                localctx.c = self._input.LT(1)
                _la = self._input.LA(1)
                if not (_la == mParser.INT or _la == mParser.FLOAT):
                    localctx.c = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 58
                localctx.m2 = self.match(mParser.M)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Start_ruleContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(mParser.ExpressionContext, 0)

        def getRuleIndex(self):
            return mParser.RULE_start_rule

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitStart_rule"):
                return visitor.visitStart_rule(self)
            else:
                return visitor.visitChildren(self)

    def start_rule(self):
        localctx = mParser.Start_ruleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_start_rule)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 62
            self.expression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx
