from io import BytesIO

from .encrypt_interface import EncryptInterface

try:
    from numpy import frombuffer, uint8, bitwise_and, bitwise_xor, right_shift, concatenate

    numpy = True
except ModuleNotFoundError:
    numpy = False

class HashCrypt(EncryptInterface):
    """
    Only encrypt by XORing the first byte of the adler32 checksum
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def encrypt(self, buffer: BytesIO, adler32: int, use_numpy=False):
        buffer.seek(0)
        data = buffer.read()
        data = bytearray(data)

        key = adler32 & 0xFF

        if numpy and use_numpy:
            keystream = frombuffer(bytes([key] * len(data)), dtype=uint8)
            data = frombuffer(data, dtype=uint8)
            keystream = frombuffer(keystream, dtype=uint8)
            data = bitwise_xor(data, keystream)
            data = data.tobytes()

        else:
            for i in range(len(data)):
                data[i] ^= key

        buffer.seek(0)
        buffer.write(data)

    def decrypt(self, buffer: BytesIO, adler32: int, use_numpy=False):
        self.encrypt(buffer, adler32, use_numpy)


    def __str__(self):
        return self.__class__.__name__
