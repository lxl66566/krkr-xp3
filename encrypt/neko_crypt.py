from io import BytesIO
from .encrypt_interface import EncryptInterface
from array import array

try:
    from numpy import frombuffer, uint8, bitwise_and, bitwise_xor, right_shift, concatenate
    numpy = True
except ModuleNotFoundError:
    numpy = False


class NekoCrypt(EncryptInterface):
    master_key: str
    sub_key: str
    xor_first_byte = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.master_key = kwargs['master_key']
        self.sub_key = kwargs['sub_key']
        self.xor_first_byte = kwargs['xor_first_byte']

    def encrypt(self, buffer: BytesIO, adler32: int, use_numpy=False):
        self.__xor(buffer, adler32, use_numpy)

    def decrypt(self, buffer: BytesIO, adler32: int, use_numpy=False):
        self.__xor(buffer, adler32, use_numpy)

    def __str__(self):
        return f'{self.__class__.__name__} ({self.master_key}, {self.sub_key}, {"xor first byte" if self.xor_first_byte else ""})'

    def __xor(self, output_buffer, adler32: int, use_numpy: bool = True):
        """XOR the data, uses numpy if available"""
        master_key, secondary_key, xor_the_first_byte = self.master_key, self.sub_key, self.xor_first_byte
        # Read the encrypted data from buffer
        output_buffer.seek(0)
        data = output_buffer.read()

        # Use numpy if available
        if numpy and use_numpy:
            # Calculate the XOR key
            adler_key = bitwise_xor(adler32, master_key)
            xor_key = bitwise_and(bitwise_xor(
                bitwise_xor(bitwise_xor(right_shift(adler_key, 24), right_shift(adler_key, 16)),
                            right_shift(adler_key, 8)), adler_key), 0xFF)
            if not xor_key:
                xor_key = secondary_key

            data = frombuffer(data, dtype=uint8)

            if xor_the_first_byte:
                first_byte_key = bitwise_and(adler_key, 0xFF)
                if not first_byte_key:
                    first_byte_key = bitwise_and(master_key, 0xFF)
                # Split the first byte into separate array
                first = frombuffer(data[:1], dtype=uint8)
                rest = frombuffer(data[1:], dtype=uint8)
                # XOR the first byte
                first = bitwise_xor(first, first_byte_key)
                # Concatenate the array back
                data = concatenate((first, rest))

            data = bitwise_xor(data, xor_key)
        else:
            adler_key = adler32 ^ master_key
            xor_key = (adler_key >> 24 ^ adler_key >> 16 ^ adler_key >> 8 ^ adler_key) & 0xFF
            if not xor_key:
                xor_key = secondary_key

            data = array('B', data)

            if xor_the_first_byte:
                first_byte_key = adler_key & 0xFF
                if not first_byte_key:
                    first_byte_key = master_key & 0xFF
                data[0] ^= first_byte_key

            # XOR the data
            for index in range(len(data)):
                data[index] ^= xor_key

        # Overwrite the buffer with decrypted/encrypted data
        output_buffer.seek(0)
        output_buffer.write(data.tobytes())