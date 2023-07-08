from io import BytesIO

from .encrypt_interface import EncryptInterface


class NoCrypt(EncryptInterface):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def encrypt(self, buffer: BytesIO, adler32: int, use_numpy=False):
        return

    def decrypt(self, buffer: BytesIO, adler32: int, use_numpy=False):
        return

    def __str__(self):
        return 'NoCrypt'
