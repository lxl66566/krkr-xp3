from io import BytesIO
from .encrypt_interface import EncryptInterface
import binascii

try:
    from numpy import frombuffer, uint8, bitwise_and, bitwise_xor, right_shift, concatenate

    numpy = True
except ModuleNotFoundError:
    numpy = False


class AkabeiCrypt(EncryptInterface):
    m_seed: int

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.m_seed = kwargs['m_seed']

    def encrypt(self, buffer: BytesIO, adler32: int, use_numpy=False):
        buffer.seek(0)
        data = buffer.read()
        data = bytearray(data)
        keystream = self.__gen_keystream(adler32)
        keystream = (keystream * (len(data)//len(keystream) + 1))[:len(data)]

        if numpy and use_numpy:
            data = frombuffer(data, dtype=uint8)
            keystream = frombuffer(keystream, dtype=uint8)
            data = bitwise_xor(data, keystream)
            data = data.tobytes()

        else:
            for i in range(len(data)):
                data[i] ^= keystream[i]

        buffer.seek(0)
        buffer.write(data)

    def decrypt(self, buffer: BytesIO, adler32: int, use_numpy=False):
        self.encrypt(buffer, adler32, use_numpy)

    def __str__(self):
        return f'{self.__class__.__name__} ({binascii.hexlify(self.m_seed.to_bytes(4, byteorder="little"))})'

    def __gen_keystream(self, adler32: int) -> bytearray:
        result = bytearray()
        adler32 = (adler32 ^ self.m_seed) & 0x7FFFFFFF
        adler32 = adler32 << 31 | adler32
        for i in range(0x20):
            result.append(adler32 & 0xFF)
            adler32 = (adler32 & 0xFFFFFFFE) << 23 | adler32 >> 8
        return result
