from config_card_matching import PROGRAM_ID
from environment_card_matching import ScratchPad

CMP, USUB1, WRITE, LSHIFT, MOVE_PTR = "CMP", "USUB1", "WRITE", "LSHIFT", "MOVE_PTR"
WRITE_OUT, WRITE_CARRY = 0, 1
CARD1_PTR, CARD2_PTR, OUT_PTR = range(3)
LEFT, RIGHT = 0, 1

class Trace(object):

    def __init__(self, card1, card2, debug=False):
        self._card1, self._card2, self._debug = card1, card2, debug
        self._env = ScratchPad(card1, card2)
        self.trace = []

        self._compile()

    def _compile(self):
        # Seed with the starting subroutine call
        self.trace.append(
            ( (CMP, PROGRAM_ID[CMP]), [], False )
        )

        # Execute Trace
        while not self._env.done():
            self._usub1()
            self._lshift()

    def _usub1(self):
        # Call USUB1 subroutine
        self.trace.append(
            ( (USUB1, PROGRAM_ID[USUB1]), [], False )
        )
        out = self._env.usub1()

        # Write to Output
        self.trace.append(
            ( (WRITE, PROGRAM_ID[WRITE]), [WRITE_OUT, out], False )
        )
        out = self._env.write(out, self._debug)

    def _lshift(self):
        self._env.lshift()

        # Move Card1 Pointer Left
        self.trace.append(
            ( (MOVE_PTR, PROGRAM_ID[MOVE_PTR]), [CARD1_PTR, LEFT], False )
        )

        # Move Card2 Pointer Left
        self.trace.append(
            ( (MOVE_PTR, PROGRAM_ID[MOVE_PTR]), [CARD2_PTR, LEFT], False )
        )

        # Move Out Pointer Left (check if done)
        self.trace.append(
            ( (MOVE_PTR, PROGRAM_ID[MOVE_PTR]), [OUT_PTR, LEFT], self._env.done() )
        )


def test():
    trace = Trace(
        card1={'suit': 'diamonds', 'rank': '5'},
        card2={'suit': 'diamonds', 'rank': '5'},
        debug=True
    )

    trace = Trace(
        card1={'suit': 'clubs', 'rank': 'A'},
        card2={'suit': 'clubs', 'rank': '7'},
        debug=True
    )

    trace = Trace(
        card1={'suit': 'diamonds', 'rank': '6'},
        card2={'suit': 'spades', 'rank': '2'},
        debug=True
    )

    print({
        'card1': {'suit': 'diamonds', 'rank': '5'},
        'card2': {'suit': 'diamonds', 'rank': '5'},
        'traces': trace.trace
    })

if __name__ == '__main__':
    test()