from typing import MutableSequence

from quickselect.hints import (Domain,
                               Key)


class SequenceKeyView:
    def __init__(self, sequence: MutableSequence[Domain], key: Key) -> None:
        self.sequence = sequence
        self.key = key

    def __getitem__(self, index: int) -> Domain:
        return self.key(self.sequence[index])
