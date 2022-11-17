import unittest
from salsa20.salsa import *

class TestChachaMethods(unittest.TestCase):

    def test_word_from_bytes(self):
        u = Word(0x00_ab_00_ef) # val is an int, so the hex representation is big-endian
        v = Word(seq=bytes.fromhex('ef 00 ab 00')) #seq is a byte stream, which Words interpret as little-endian
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

    def test_qround_example1(self):
        y = [Word(0), Word(0), Word(0), Word(0)]
        self.assertEqual(qround_salsa(y), y)

    def test_qround_example2(self):
        y = [Word(1), Word(0), Word(0), Word(0)]
        z = [Word(0x08008145),
             Word(0x00000080),
             Word(0x00010200),
             Word(0x20500000)]
        self.assertEqual(qround_salsa(y), z)

    def test_qround_example3(self):
        y = [Word(0), Word(1), Word(0), Word(0)]
        z = [Word(0x88000100),
             Word(0x00000001),
             Word(0x00000200),
             Word(0x00402000)]
        self.assertEqual(qround_salsa(y), z)

    def test_qround_example4(self):
        y = [Word(0), Word(0), Word(1), Word(0)]
        z = [Word(0x80040000),
             Word(0x00000000),
             Word(0x00000001),
             Word(0x00002000)]

    def test_qround_example5(self):
        y = [Word(0), Word(0), Word(0), Word(1)]
        z = [Word(0x00048044),
             Word(0x00000080),
             Word(0x00010000),
             Word(0x20100001)]
        self.assertEqual(qround_salsa(y), z)

    def test_qround_example6(self):
        y = [Word(0xe7e8c006),
             Word(0xc4f9417d),
             Word(0x6479b4b2),
             Word(0x68c67137)]
        z = [Word(0xe876d72b),
             Word(0x9361dfd5),
             Word(0xf1460244),
             Word(0x948541a3)]
        self.assertEqual(qround_salsa(y), z)

    def test_qround_example7(self):
        y = [Word(0xd3917c5b),
             Word(0x55f1c407),
             Word(0x52a58a7a),
             Word(0x8f887a3b)]

        z = [Word(0x3e2f308c),
             Word(0xd90a8f36),
             Word(0x6ab2a923),
             Word(0x2883524c)]
        self.assertEqual(qround_salsa(y), z)

    def test_qround_invalid_length(self):
        y = [Word(0xd3917c5b),
             Word(0x55f1c407),
             Word(0x52a58a7a)]
        with self.assertRaises(ValueError):
            qround_salsa(y)

    def test_rowround_example1(self):
        y = [Word(1), Word(0), Word(0), Word(0),
             Word(1), Word(0), Word(0), Word(0),
             Word(1), Word(0), Word(0), Word(0),
             Word(1), Word(0), Word(0), Word(0)]
        z = [Word(0x08008145), Word(0x00000080), Word(0x00010200), Word(0x20500000),
             Word(0x20100001), Word(0x00048044), Word(0x00000080), Word(0x00010000),
             Word(0x00000001), Word(0x00002000), Word(0x80040000), Word(0x00000000),
             Word(0x00000001), Word(0x00000200), Word(0x00402000), Word(0x88000100)]
        self.assertEqual(rowround(y), z)

    def test_rowround_example2(self):
        y = [Word(0x08521bd6), Word(0x1fe88837), Word(0xbb2aa576), Word(0x3aa26365),
             Word(0xc54c6a5b), Word(0x2fc74c2f), Word(0x6dd39cc3), Word(0xda0a64f6),
             Word(0x90a2f23d), Word(0x067f95a6), Word(0x06b35f61), Word(0x41e4732e),
             Word(0xe859c100), Word(0xea4d84b7), Word(0x0f619bff), Word(0xbc6e965a)]
        z = [Word(0xa890d39d), Word(0x65d71596), Word(0xe9487daa), Word(0xc8ca6a86),
             Word(0x949d2192), Word(0x764b7754), Word(0xe408d9b9), Word(0x7a41b4d1),
             Word(0x3402e183), Word(0x3c3af432), Word(0x50669f96), Word(0xd89ef0a8),
             Word(0x0040ede5), Word(0xb545fbce), Word(0xd257ed4f), Word(0x1818882d)]
        self.assertEqual(rowround(y), z)

    def test_rowround_wrong_length(self):
        y = [Word(0x08521bd6), Word(0x1fe88837), Word(0xbb2aa576), Word(0x3aa26365),
             Word(0xc54c6a5b), Word(0x2fc74c2f), Word(0x6dd39cc3), Word(0xda0a64f6),
             Word(0x90a2f23d), Word(0x067f95a6), Word(0x06b35f61), Word(0x41e4732e),
             Word(0xe859c100), Word(0xea4d84b7), Word(0x0f619bff)]
        with self.assertRaises(ValueError):
            rowround(y)

    def test_columnround_example1(self):
        x = [Word(1), Word(0), Word(0), Word(0),
             Word(1), Word(0), Word(0), Word(0),
             Word(1), Word(0), Word(0), Word(0),
             Word(1), Word(0), Word(0), Word(0)]
        y = [Word(0x10090288), Word(0x00000000), Word(0x00000000), Word(0x00000000),
             Word(0x00000101), Word(0x00000000), Word(0x00000000), Word(0x00000000),
             Word(0x00020401), Word(0x00000000), Word(0x00000000), Word(0x00000000),
             Word(0x40a04001), Word(0x00000000), Word(0x00000000), Word(0x00000000)]
        self.assertEqual(columnround(x), y)

    def test_columnround_example2(self):
        x = [Word(0x08521bd6), Word(0x1fe88837), Word(0xbb2aa576), Word(0x3aa26365),
             Word(0xc54c6a5b), Word(0x2fc74c2f), Word(0x6dd39cc3), Word(0xda0a64f6),
             Word(0x90a2f23d), Word(0x067f95a6), Word(0x06b35f61), Word(0x41e4732e),
             Word(0xe859c100), Word(0xea4d84b7), Word(0x0f619bff), Word(0xbc6e965a)]
        y = [Word(0x8c9d190a), Word(0xce8e4c90), Word(0x1ef8e9d3), Word(0x1326a71a),
             Word(0x90a20123), Word(0xead3c4f3), Word(0x63a091a0), Word(0xf0708d69),
             Word(0x789b010c), Word(0xd195a681), Word(0xeb7d5504), Word(0xa774135c),
             Word(0x481c2027), Word(0x53a8e4b5), Word(0x4c1f89c5), Word(0x3f78c9c8)]
        self.assertEqual(columnround(x), y)

    def test_columnround_wrong_length(self):
        x = [Word(0x08521bd6), Word(0x1fe88837), Word(0xbb2aa576), Word(0x3aa26365),
             Word(0xc54c6a5b), Word(0x2fc74c2f), Word(0x6dd39cc3), Word(0xda0a64f6),
             Word(0x90a2f23d), Word(0x067f95a6), Word(0x06b35f61), Word(0x41e4732e),
             Word(0xe859c100), Word(0xea4d84b7), Word(0x0f619bff)]
        with self.assertRaises(ValueError):
            columnround(x)

    def test_doubleround_example1(self):
        x = [Word(1), Word(0), Word(0), Word(0),
             Word(0), Word(0), Word(0), Word(0),
             Word(0), Word(0), Word(0), Word(0),
             Word(0), Word(0), Word(0), Word(0)]
        y = [Word(0x8186a22d), Word(0x0040a284), Word(0x82479210), Word(0x06929051),
             Word(0x08000090), Word(0x02402200), Word(0x00004000), Word(0x00800000),
             Word(0x00010200), Word(0x20400000), Word(0x08008104), Word(0x00000000),
             Word(0x20500000), Word(0xa0000040), Word(0x0008180a), Word(0x612a8020)]
        self.assertEqual(doubleround(x), y)

    def test_doubleround_example2(self):
        x = [Word(0xde501066), Word(0x6f9eb8f7), Word(0xe4fbbd9b), Word(0x454e3f57),
             Word(0xb75540d3), Word(0x43e93a4c), Word(0x3a6f2aa0), Word(0x726d6b36),
             Word(0x9243f484), Word(0x9145d1e8), Word(0x4fa9d247), Word(0xdc8dee11),
             Word(0x054bf545), Word(0x254dd653), Word(0xd9421b6d), Word(0x67b276c1)]
        y = [Word(0xccaaf672), Word(0x23d960f7), Word(0x9153e63a), Word(0xcd9a60d0),
             Word(0x50440492), Word(0xf07cad19), Word(0xae344aa0), Word(0xdf4cfdfc),
             Word(0xca531c29), Word(0x8e7943db), Word(0xac1680cd), Word(0xd503ca00),
             Word(0xa74b2ad6), Word(0xbc331c5c), Word(0x1dda24c7), Word(0xee928277)]
        self.assertEqual(doubleround(x), y)

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

    def test_hash_example2(self):
        x = bytes([211,159, 13,115, 76, 55, 82,183,  3,117,222, 37,191,187,234,136,
                    49,237,179, 48,  1,106,178,219,175,199,166, 48, 86, 16,179,207,
                    31,240, 32, 63, 15, 83, 93,161,116,147, 48,113,238, 55,204, 36,
                    79,201,235, 79,  3, 81,156, 47,203, 26,244,243, 88,118,104, 54])
        y = bytes([109, 42,178,168,156,240,248,238,168,196,190,203, 26,110,170,154,
                    29, 29,150, 26,150, 30,235,249,190,163,251, 48, 69,144, 51, 57,
                   118, 40,152,157,180, 57, 27, 94,107, 42,236, 35, 27,111,114,114,
                   219,236,232,135,111,155,110, 18, 24,232, 95,158,179, 19, 48,202])
        self.assertEqual(hash(x), y)

    def test_hash_example3(self):
        x = bytes([ 88,118,104, 54, 79,201,235, 79,  3, 81,156, 47,203, 26,244,243,
                   191,187,234,136,211,159, 13,115, 76, 55, 82,183,  3,117,222, 37,
                    86, 16,179,207, 49,237,179, 48,  1,106,178,219,175,199,166, 48,
                   238, 55,204, 36, 31,240, 32, 63, 15, 83, 93,161,116,147, 48,113])
        y = bytes([179, 19, 48,202,219,236,232,135,111,155,110, 18, 24,232, 95,158,
                    26,110,170,154,109, 42,178,168,156,240,248,238,168,196,190,203,
                    69,144, 51, 57, 29, 29,150, 26,150, 30,235,249,190,163,251, 48,
                    27,111,114,114,118, 40,152,157,180, 57, 27, 94,107, 42,236, 35])
        self.assertEqual(hash(x), y)

    ## Takes 7 minutes to run, but it passed
    # def test_hash_example4(self):
    #     x = bytes([  6,124, 83,146, 38,191,  9, 50,  4,161, 47,222,122,182,223,185,
    #                 75, 27,  0,216, 16,122,  7, 89,162,104,101,147,213, 21, 54, 95,
    #                225,253,139,176,105,132, 23,116, 76, 41,176,207,221, 34,157,108,
    #                 94, 94, 99, 52, 90,117, 91,220,146,190,239,143,196,176,130,186])
    #     y = bytes([  8, 18, 38,199,119, 76,215, 67,173,127,144,162,103,212,176,217,
    #                192, 19,233, 33,159,197,154,160,128,243,219, 65,171,136,135,225,
    #                123, 11, 68, 86,237, 82, 20,155,133,189,  9, 83,167,116,194, 78,
    #                122,127,195,185,185,204,188, 90,245,  9,183,248,226, 85,245,104])
    #     for i in range(1000000):
    #         x = hash(x)
    #     self.assertEqual(x, y)

    def test_expansion_example1(self):
        key = [i for i in range(1, 17)] + [i for i in range(201, 217)]
        nonce = [i for i in range(101, 109)]
        count_bytes = bytes([i for i in range(109, 117)])
        blockcount = int.from_bytes(count_bytes, byteorder='little')
        x = expansion(key, nonce, blockcount)
        y = bytes([ 69, 37, 68, 39, 41, 15,107,193,255,139,122,  6,170,233,217, 98,
                    89,144,182,106, 21, 51,200, 65,239, 49,222, 34,215,114, 40,126,
                   104,197,  7,225,197,153, 31,  2,102, 78, 76,176, 84,245,246,184,
                   177,160,133,130,  6, 72,149,119,192,195,132,236,234,103,246, 74])
        self.assertEqual(x, y)

    def test_expansion_example2(self):
        key = [i for i in range(1, 17)]
        nonce = [i for i in range(101, 109)]
        count_bytes = bytes([i for i in range(109, 117)])
        blockcount = int.from_bytes(count_bytes, byteorder='little')
        x = expansion(key, nonce, blockcount)
        y = bytes([ 39,173, 46,248, 30,200, 82, 17, 48, 67,254,239, 37, 18, 13,247,
                   241,200, 61,144, 10, 55, 50,185,  6, 47,246,253,143, 86,187,225,
                   134, 85,110,246,161,163, 43,235,231, 94,171, 51,145,214,112, 29,
                    14,232,  5, 16,151,140,183,141,171,  9,122,181,104,182,177,193])
        self.assertEqual(x, y)

    def test_encrypt_round_trip(self):
        key = b'*secret**secret**secret**secret*'
        nonce = b'jurassic'
        plaintext = b'We kill Caesar at dawn'
        roundtrip = encrypt(key, nonce, encrypt(key, nonce, plaintext))
        self.assertEqual(plaintext, roundtrip)

    def test_encrypt_small_message_matches_other_library(self):
        # check against results from the salsa20 package in PyPI
        key = b'*secret**secret**secret**secret*'
        nonce = b'jurassic'
        plaintext = b'We kill Caesar at dawn'
        actual_ciphertext = encrypt(key, nonce, plaintext)
        expected_ciphertext = b'Q~O3"\xae\x08\x0e\x16\xba\x012\x86\xe0I\xd5\x8f\xa2\xd4+M\x80'
        self.assertEqual(actual_ciphertext, expected_ciphertext)

    def test_encrypt_long_message_matches_other_library(self):
        # check against results from the salsa20 package in PyPI
        key = b'*secret**secret**secret**secret*'
        nonce = b'jurassic'
        plaintext = (
            b"Call me Ishmael. Some years ago-never mind how long precisely-having little or no money in my purse, "
            b"and nothing particular to interest me on shore, I thought I would sail about a little and see the watery "
            b"part of the world. It is a way I have of driving off the spleen and regulating the circulation. Whenever "
            b"I find myself growing grim about the mouth; whenever it is a damp, drizzly November in my soul; whenever "
            b"I find myself involuntarily pausing before coffin warehouses, and bringing up the rear of every funeral "
            b"I meet; and especially whenever my hypos get such an upper hand of me, that it requires a strong moral "
            b"principle to prevent me from deliberately stepping into the street, and methodically knocking people's "
            b"hats off-then, I account it high time to get to sea as soon as I can. This is my substitute for pistol "
            b"and ball. With a philosophical flourish Cato throws himself upon his sword; I quietly take to the ship. "
            b"There is nothing surprising in this. If they but knew it, almost all men in their degree, some time or "
            b"other, cherish very nearly the same feelings towards the ocean with me."
        )
        expected_ciphertext = (
            bytes.fromhex(
                '457a03346baf010e1ca80c2c86f7059adbd1df275fce12281b2989016403b5d8152452655beae8dc55d6b30b0f7a571b20d6d5'
                '9beb06747a51943e5f65012a8d40a5025a96b7b850665f37d359666eccee8be6ee6977408521cb17556a3838dfbbd1921025c3'
                '8da5d65415181b1eddce3d94f06617ae542d7e8f8867904bf24b78db2ccf0226cb3755f4a93b2f8188ce07cb177d25479868c2'
                'b160e078f8f1fe1f34a575fd600533138a3b56f1e54219e459902501e7aaec0b6279c91176da4af5373b4cd0fd7f054340a039'
                'c7fb2382e2c5d098e96379bda6f3c9d1bb944bb1de43b997af62d60e6fc1afbdd09206cee8b0739e186fcd73dfea39b552351e'
                '615c965d8e8c164775160fee9f0ae5db047f4dd5030c9f371659ec63cf74ed988825d921b87834553e24c15e8ecca982fa6d6c'
                'd92dcea676fdc24587edf8b7e93ebd15b25f2bd7a4b94a55c26e11c2917a5aeb8d648dbc4e6210ff0e42a674052c89c1eb1255'
                '05abcbc2e952f2ba57090b9ab91aea7bf8bd6d062441a5cc24be451621fb3fb7c23571a646a4a2dc9856efbfeac6e92832873a'
                'b4d419dfe2e8dd74ab873a9c289a861fdcd92708f3e5f45d2eed9f63fc8a8f3fe1a0e564838cd4c774397c01a8f8017c6230f6'
                '8ae540a39576cc11fd8f847f359544c8024bc83b9455a41b15d249fe0e4c04c2c3537c73d0bd12227ce418e78ec01d77c25def'
                '24ed7c624bfe512067f75225163531ef1e8b89ee5e930aebaa154f48d1c3ffd2c5e23ae9c391e54aa6f9da66e771783a351c33'
                '59d0cf31c1529d98fcf91769aee13bc640d46e59653c709c5b98bd0c52fb1446b8756afacb1ab544b9e6d6585eaa2d52259fcb'
                'b4f76abca69aae91aaa69b299d6dfe8c0ff45826fec6a3bdc541d3102e7e1277c48d7b0a9cf51cb87faef22521efa055cb53f3'
                '34ddd62cf978d90e76475311bbcab84b6a6423794a135f8a81351a12a5abaa9960bd4c4c1382db1eefe487a17c524e8a9d43ff'
                'c7cf71e32abe33965f61316ab05317e0db4de6de1b526a3ea3edba5b02a1b37b7f6ae3b30c89e9a75f1ee7a45438982290291a'
                'a05ed72a0ea31b8b52a79f0835035ef3502f10d076d0339fc6ac5228cdcafe176c0a3cfecb024321ba63a4f0c707542eff3d44'
                '87332368232482b56d71a084d5b21d4bb96b896d41eef286d360a2200025606837b3af5d92df166d6e775638c7eaa19722c382'
                '831f43230dc8862ad14af9a34b74ac6258c3bea46203635a22e319751095780014d0953469da2e44ea20325d27ba8ab449b233'
                'eadc2db081fadf7923236dc766ddc7259c26b7dddf1b12453f55b69e756febf4a3e28d67a592041bc5ba88d31eb2b7ed29c90e'
                '2a5326920afad98a57d487a6857911328c9afbc9a0c3313e33e03242376123c5f3406a891c3a43214fc0eedbeecdf70c935180'
                '87900af16b45b1e91566c747ed91fcd1919233218a812f70190e1ef809981c95a18c503c2fa5cacc2e627e84a49604861141e5'
                'f3d17b891b47b2f75f73ac8c92bd2677be33f2fb4dff6a2347f5f81a88b24dc937d35c21'
            )
        )
        actual_ciphertext = encrypt(key, nonce, plaintext)
        self.assertEqual(actual_ciphertext, expected_ciphertext)


if __name__ == "__main__":
    unittest.main()