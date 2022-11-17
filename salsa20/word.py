from __future__ import annotations

class Word:
    """A 4-byte word as defined in the Salsa20 specification.

    There are two ways to instantiate a Word. The first is to use its decimal representation:
        word = Word(101)

    The second is to use a sequence of four bytes, which is equivalent to the littleendian function from the
    Salsa20 specification:
        word1 = Word(seq=bytes.fromhex('ef 00 ab 00')
        word2 = Word(seq=bytes([101, 110, 200, 250]))

    Several operators have been overridden for convenience:
        + is now addition modulo 2**32
        ^ is still xor
        << is left-rotate instead of left-shift"""

    def __init__(self, val:int=-1, /, *, seq:bytes=None):
        if val != -1 and seq is not None:
            raise ValueError('must not specify both val or seq')
        elif val != -1:
            self.val = val
        elif seq is not None:
            if len(seq) != 4:
                raise ValueError('seq must be exactly 4 bytes')
            self.val = int.from_bytes(seq, byteorder='little')
        else:
            raise ValueError('must specify either val or seq')

    def to_bytes(self) -> bytes:
        return self.val.to_bytes(4, 'little')

    def __eq__(self, v:Word) -> bool:
        return self.val == v.val

    def __add__(self, v:Word) -> Word:
        w = (self.val + v.val) % (2 ** 32)
        return Word(w)

    def __xor__(self, v:Word) -> Word:
        return Word(self.val ^ v.val)

    def __lshift__(self, c:int) -> Word:
        new_val = ((self.val << c) + (self.val >> (32 - c))) % (2 ** 32)
        return Word(new_val)

    def __repr__(self) -> str:
        return 'Word(0x{:08x})'.format(self.val)

    def __str__(self) -> str:
        return '0x{:08x}'.format(self.val)
