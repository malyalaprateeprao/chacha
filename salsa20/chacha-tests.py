import unittest
from salsa20.chacha import *


class TestChachaMethods(unittest.TestCase):

    def test_word_from_bytes(self):
        u = Word(0x00_ab_00_ef) # val is an int, so the hex representation is big-endian
        v = Word(seq=bytes.fromhex('ef 00 ab 00'))  #seq is a byte stream, which Words interpret as little-endian
        self.assertEqual(u, v)

    def test_word_example1(self):
        u = Word(seq=bytes([0, 0, 0, 0]))
        v = Word(0)
        self.assertEqual(u, v)

    def test_word_example2(self):
        u = Word(seq=bytes([86, 75, 30, 9]))
        v = Word(0x091e4b56)
        self.assertEqual(u, v)

    def test_word_example3(self):
        u = Word(seq=bytes([255, 255, 255, 250]))
        v = Word(0xfaffffff)
        self.assertEqual(u, v)

    def test_word_to_bytes_example1(self):
        v = Word(0x000000000).to_bytes()
        u = bytes([0, 0, 0, 0])
        self.assertEqual(v, u)

    def test_word_to_bytes_example2(self):
        v = Word(0x091e4b56).to_bytes()
        u = bytes([86, 75, 30, 9])
        self.assertEqual(v, u)

    def test_word_to_bytes_example3(self):
        v = Word(0xfaffffff).to_bytes()
        u = bytes([255, 255, 255, 250])
        self.assertEqual(v, u)

    def test_neq(self):
        u = Word(0xc0a8787e)
        v = Word(0x9fd1161d)
        self.assertNotEqual(u, v)

    def test_eq(self):
        u = Word(0xc0a8787e)
        v = Word(0xc0a8787e)
        self.assertEqual(u, v)

    def test_sum_pass(self):
        u = Word(0xc0a8787e)
        v = Word(0x9fd1161d)
        w = Word(0x60798e9b)
        self.assertEqual(u+v, w)

    def test_sum_fail(self):
        u = Word(0x00000002)
        v = Word(0x00000004)
        w = Word(0xffffffff)
        self.assertNotEqual(u+v, w)

    def test_xor_pass(self):
        u = Word(0xc0a8787e)
        v = Word(0x9fd1161d)
        self.assertEqual(u ^ v, Word(0x5f796e63))

    def test_xor_fail(self):
        u = Word(0x0000)
        v = Word(0x0101)
        self.assertNotEqual(u ^ v, Word(0x0000))

    def test_lrot_pass(self):
        u = Word(0xc0a8787e)
        c = 5
        self.assertEqual(u << 5, Word(0x150f0fd8))

    def test_lrot_pass_rollover(self):
        u = Word(0xffffffff)
        c = 4
        self.assertEqual(u << c, u)

    def test_lrot_fail(self):
        u = Word(0x000000ff)
        c = 8
        self.assertEqual(u << c, Word(0x0000ff00))

    def test_qround_ietf(self):
        # from section 2.2.1 of https://datatracker.ietf.org/doc/html/draft-irtf-cfrg-chacha20-poly1305-10
        y = [Word(0x516461b1), Word(0x2a5f714c), Word(0x53372767), Word(0x3d631689)]
        expected_output = [Word(0xbdb886dc), Word(0xcfacafd2), Word(0xe46bea80), Word(0xccc07c79)]
        self.assertEqual(qround_chacha(y), expected_output)

    def test_qround_example1(self):
        y = [Word(0), Word(0), Word(0), Word(0)]
        self.assertEqual(qround_chacha(y), y)

    def test_qround_invalid_length(self):
        y = [Word(0xd3917c5b),
             Word(0x55f1c407),
             Word(0x52a58a7a)]
        with self.assertRaises(ValueError):
            qround_chacha(y)

    def test_rowround_wrong_length(self):
        y = [Word(0x08521bd6), Word(0x1fe88837), Word(0xbb2aa576), Word(0x3aa26365),
             Word(0xc54c6a5b), Word(0x2fc74c2f), Word(0x6dd39cc3), Word(0xda0a64f6),
             Word(0x90a2f23d), Word(0x067f95a6), Word(0x06b35f61), Word(0x41e4732e),
             Word(0xe859c100), Word(0xea4d84b7), Word(0x0f619bff)]
        with self.assertRaises(ValueError):
            diagonalround(y)

    def test_columnround_wrong_length(self):
        x = [Word(0x08521bd6), Word(0x1fe88837), Word(0xbb2aa576), Word(0x3aa26365),
             Word(0xc54c6a5b), Word(0x2fc74c2f), Word(0x6dd39cc3), Word(0xda0a64f6),
             Word(0x90a2f23d), Word(0x067f95a6), Word(0x06b35f61), Word(0x41e4732e),
             Word(0xe859c100), Word(0xea4d84b7), Word(0x0f619bff)]
        with self.assertRaises(ValueError):
            columnround(x)

    def test_doubleround_wrong_length(self):
        x = [Word(0xde501066), Word(0x6f9eb8f7), Word(0xe4fbbd9b), Word(0x454e3f57),
             Word(0xb75540d3), Word(0x43e93a4c), Word(0x3a6f2aa0), Word(0x726d6b36),
             Word(0x9243f484), Word(0x9145d1e8), Word(0x4fa9d247), Word(0xdc8dee11)]
        with self.assertRaises(ValueError):
            doubleround(x)

    def test_hash_wrong_number_bytes(self):
        x = bytes([0, 0, 0, 0, 0])
        with self.assertRaises(ValueError):
            hash(x)

    def test_hash_example1(self):
        x = bytes([  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0])
        y = bytes([  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0])
        self.assertEqual(hash(x), y)

    def test_block_ietf(self):
        # from section 2.3.2 of https://datatracker.ietf.org/doc/html/draft-irtf-cfrg-chacha20-poly1305-10
        key = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'\
              b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f'
        nonce = b'\x00\x00\x00\x09\x00\x00\x00\x4a\x00\x00\x00\x00'
        expected = b'\x10\xf1\xe7\xe4\xd1\x3b\x59\x15\x50\x0f\xdd\x1f\xa3\x20\x71\xc4'\
                   b'\xc7\xd1\xf4\xc7\x33\xc0\x68\x03\x04\x22\xaa\x9a\xc3\xd4\x6c\x4e'\
                   b'\xd2\x82\x64\x46\x07\x9f\xaa\x09\x14\xc2\xd7\x05\xd9\x8b\x02\xa2'\
                   b'\xb5\x12\x9c\xd1\xde\x16\x4e\xb9\xcb\xd0\x83\xe8\xa2\x50\x3c\x4e'
        self.assertEqual(expansion(key, nonce, 1), expected)

    def test_encrypt_round_trip(self):
        key = b'*secret**secret**secret**secret*'
        nonce = b'jurassicmaly'
        plaintext = b'We kill Caesar at dawn'
        roundtrip = encrypt(key, nonce, encrypt(key, nonce, plaintext))
        self.assertEqual(plaintext, roundtrip)

    def test_sunscreen(self):
        # This example comes from section 2.4.2 of
        # https://datatracker.ietf.org/doc/html/draft-irtf-cfrg-chacha20-poly1305-10
        key = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'\
              b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f'
        nonce = b'\x00\x00\x00\x00\x00\x00\x00\x4a\x00\x00\x00\x00'
        iv = 1
        plaintext = b"Ladies and Gentlemen of the class of '99: If I could offer you only one tip for the future, "\
                    b"sunscreen would be it."
        actual_ciphertext = encrypt(key, nonce, plaintext, iv)
        expected_ciphertext = b'\x6e\x2e\x35\x9a\x25\x68\xf9\x80\x41\xba\x07\x28\xdd\x0d\x69\x81'\
                              b'\xe9\x7e\x7a\xec\x1d\x43\x60\xc2\x0a\x27\xaf\xcc\xfd\x9f\xae\x0b'\
                              b'\xf9\x1b\x65\xc5\x52\x47\x33\xab\x8f\x59\x3d\xab\xcd\x62\xb3\x57'\
                              b'\x16\x39\xd6\x24\xe6\x51\x52\xab\x8f\x53\x0c\x35\x9f\x08\x61\xd8'\
                              b'\x07\xca\x0d\xbf\x50\x0d\x6a\x61\x56\xa3\x8e\x08\x8a\x22\xb6\x5e'\
                              b'\x52\xbc\x51\x4d\x16\xcc\xf8\x06\x81\x8c\xe9\x1a\xb7\x79\x37\x36'\
                              b'\x5a\xf9\x0b\xbf\x74\xa3\x5b\xe6\xb4\x0b\x8e\xed\xf2\x78\x5e\x42'\
                              b'\x87\x4d'
        self.assertEqual(actual_ciphertext, expected_ciphertext)

    def test_sunscreen_decrypt(self):
        # This example comes from section 2.4.2 of
        # https://datatracker.ietf.org/doc/html/draft-irtf-cfrg-chacha20-poly1305-10
        key = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f' \
              b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f'
        nonce = b'\x00\x00\x00\x00\x00\x00\x00\x4a\x00\x00\x00\x00'
        iv = 1
        ciphertext = b'\x6e\x2e\x35\x9a\x25\x68\xf9\x80\x41\xba\x07\x28\xdd\x0d\x69\x81' \
                     b'\xe9\x7e\x7a\xec\x1d\x43\x60\xc2\x0a\x27\xaf\xcc\xfd\x9f\xae\x0b' \
                     b'\xf9\x1b\x65\xc5\x52\x47\x33\xab\x8f\x59\x3d\xab\xcd\x62\xb3\x57' \
                     b'\x16\x39\xd6\x24\xe6\x51\x52\xab\x8f\x53\x0c\x35\x9f\x08\x61\xd8' \
                     b'\x07\xca\x0d\xbf\x50\x0d\x6a\x61\x56\xa3\x8e\x08\x8a\x22\xb6\x5e' \
                     b'\x52\xbc\x51\x4d\x16\xcc\xf8\x06\x81\x8c\xe9\x1a\xb7\x79\x37\x36' \
                     b'\x5a\xf9\x0b\xbf\x74\xa3\x5b\xe6\xb4\x0b\x8e\xed\xf2\x78\x5e\x42' \
                     b'\x87\x4d'
        expected_plaintext = b"Ladies and Gentlemen of the class of '99: If I could offer you only one tip for the "\
                             b"future, sunscreen would be it."
        actual_plaintext = decrypt(key, nonce, ciphertext, iv)
        self.assertEqual(actual_plaintext, expected_plaintext)


if __name__ == "__main__":
    unittest.main()
