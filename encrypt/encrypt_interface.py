from io import BytesIO


class EncryptInterface:
    """基礎加解密介面，"""

    def __init__(self, **kwargs):
        """初始化介面，比如說傳遞密鑰🔐參數"""
        pass

    def encrypt(self, buffer: BytesIO, adler32: int, use_numpy=False):
        """基礎加密介面，你需要 derive 🔐然後對 buffer 進行加密"""
        pass

    def decrypt(self, buffer: BytesIO, adler32: int, use_numpy=False):
        """基礎解密介面，你需要 derive 🔐然後對 buffer 進行解密"""
        pass

    def __str__(self) -> str:
        """用來描述這個加密算法的字符串"""
        return f'{self.__class__.__name__} 基礎加解密介面'
