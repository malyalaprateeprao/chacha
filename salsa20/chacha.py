from salsa20.word import Word


def qround_chacha(y: list[Word]) -> list[Word]:
    if len(y) != 4:
        raise ValueError('y must have length 4')
    z = [None]*4
    z[0] = y[0] + y[1]; z[3] = y[3] ^ z[0]; z[3] = z[3] << 16;
    z[2] = y[2] + z[3]; z[1] = y[1] ^ z[2]; z[1] = z[1] << 12;
    z[0] = z[0] + z[1]; z[3] = z[3] ^ z[0]; z[3] = z[3] << 8;
    z[2] = z[2] + z[3]; z[1] = z[1] ^ z[2]; z[1] = z[1] << 7;
    return z


def diagonalround(y: list[Word]) -> list[Word]:
    """Do a row-round transformation on the expansion block.

    This implements the rowround function from the Chacha20 specification. It applies the quarterround function to
    shifted versions of each row.

    Keyword arguments:
        y -- a 16-word list

    Returns:
        a 16-word list"""
    if len(y) != 16:
        raise ValueError('y must have length 16')
    z = [None]*16
    z[0], z[5], z[10], z[15] = qround_chacha([y[0], y[5], y[10], y[15]])
    z[1], z[6], z[11], z[12] = qround_chacha([y[1], y[6], y[11], y[12]])
    z[2], z[7], z[8], z[13] = qround_chacha([y[2], y[7], y[8], y[13]])
    z[3], z[4], z[9], z[14] = qround_chacha([y[3], y[4], y[9], y[14]])
    return z


def columnround(x: list[Word]) -> list[Word]:
    """Do a column-round transformation on the expansion block.

    This implements the columnround function from the Chacha20 specification. It applies the quarterround function to
    shifted versions of each column.

    Keyword arguments:
        x -- a 16-word list

    Returns:
        a 16-word list"""
    if len(x) != 16:
        raise ValueError('x must be a 16-word list')
    y = [None]*16
    y[0], y[4], y[8], y[12] = qround_chacha([x[0], x[4], x[8], x[12]])
    y[1], y[5], y[9], y[13] = qround_chacha([x[1], x[5], x[9], x[13]])
    y[2], y[6], y[10], y[14] = qround_chacha([x[2], x[6], x[10], x[14]])
    y[3], y[7], y[11], y[15] = qround_chacha([x[3], x[7], x[11], x[15]])
    return y


def doubleround(x: list[Word]) -> list[Word]:
    """Performs a column round followed by a row round.

    This implements the doubleround function from the Chacha20 specification.

    Keyword arguments:
        x -- a 16-word list

    Returns:
        a 16-word list"""
    if len(x) != 16:
        raise ValueError('x must be a 16-word list')
    return diagonalround(columnround(x))


def hash(x: bytes) -> bytes:
    """Transforms an input expansion block to an output block of the key stream.

    This implements the hash function from the Chacha20 specification. It takes a 64-byte sequence and transforms it
    into 16 words, which are best visualized as a 4x4 array. It performs ten doublerounds on it, then adds it to the
    original input block to create the output block, which it converts back into a 64-byte stream.

    Keyword arguments:
        x -- a bytes object with length 64

    Returns:
        a bytes object with length 64"""
    if len(x) != 64:
        raise ValueError('x must be exactly 64 bytes')
    u = [None]*16
    for i in range(16):
        j = i*4
        u[i] = Word(seq=bytes([x[j], x[j+1], x[j+2], x[j+3]]))
    z = u.copy()
    for i in range(10):
        z = doubleround(z)
    res = [None]*64
    for i in range(16):
        j = 4*i
        res[j:j+4] = (u[i] + z[i]).to_bytes()
    return bytes(res)


def expansion(key: bytes, nonce: bytes, blockcount: int) -> bytes:
    """Creates a 64-byte output block for the key stream.

    This function implements the expansion function from the Chacha20 specification, but with one deviation. The original
    spec called for a 16-byte sequence n, which was intended to be a combination of the nonce and block counter. Here
    they've been broken out separately for ease of use.

    When assembled, the input block can be pictured as a 4x4 input block of words that looks like this before being
    transformed into an output block:

        constant     constant  constant  constant
        key          key       key       key
        key          key       key       key
        blockcount   nonce     nonce     nonce

    Keyword arguments:
        key -- a bytes object with length 32
        nonce -- a bytes object with length 12
        blockcount -- an int in the range [0, 2**64 - 1] (inclusive)

    Returns:
        a bytes object with length 64"""
    if len(key) == 32:
        c = b'expand 32-byte k'
    else:
        raise ValueError('key must be 32 bytes long')
    if len(nonce) != 12:
        raise ValueError('nonce must be 12 bytes long')
    if blockcount < 0 or blockcount > (2**64 - 1):
        raise ValueError('blockcount must be in range [0, 2**64 - 1] (inclusive)')

    x_list = [None]*64
    x_list[0:16] = c[0:16]
    x_list[16:48] = key[0:32]
    x_list[48:52] = blockcount.to_bytes(4, byteorder='little')
    x_list[52:64] = nonce
    return hash(bytes(x_list))


def encrypt(key: bytes, nonce: bytes, msg: bytes, iv: int = 0) -> bytes:
    """Encrypts (or decrypts) a message to create ciphertext (or plaintext).

    This function creates the key stream and xors it with the plaintext (or ciphertext) to create the ciphertext (or
    plaintext). Note that while the key stream is constructed in blocks of 64 bytes, the message can be any length; the
    key stream will be truncated to the same message length before the xor.

    Keyword arguments:
        key -- a private key of length 32
        nonce -- a "number used once" that has never been used with this key before. Must be length 12.
        iv -- starting value of the block counter
        msg -- the message to encrypt (or decrypt)

    Returns:
        ciphertext if msg was plaintext, or plaintext if msg was ciphertext"""
    num_blocks = ((len(msg)-1) % 64) + 1
    expansion_array = bytearray(num_blocks*64)
    for i in range(num_blocks):
        j = i*64
        expansion_array[j:j+64] = expansion(key, nonce, iv + i)
    expansion_array = expansion_array[:len(msg)]
    result = bytearray(len(msg))
    for i in range(len(msg)):
        result[i:i+1] = (expansion_array[i] ^ msg[i]).to_bytes(1, byteorder='big')
    return bytes(result)


def decrypt(key: bytes, nonce: bytes, msg: bytes, iv: int = 0) -> bytes:
    """A wrapper function for the encrypt function, since Chacha20 handles encryption and decryption identically."""
    return encrypt(key, nonce, msg, iv)
