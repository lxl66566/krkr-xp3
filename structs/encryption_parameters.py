from typing import Type

from encrypt import NoCrypt, NekoCrypt, EncryptInterface, AkabeiCrypt

encryption_parameters: dict[str: tuple[tuple[Type[EncryptInterface], dict[str, int | bool], bytes]]] = {
    # Master key, secondary key, XOR the first byte, segment name (for packing)
    # 👇 加密算法，加密參數的 dict，遺留的臭大糞 chunk 名
    'none': (NoCrypt, {}, False, b'eliF'),
    'neko_vol1': (NekoCrypt, {'master_key': 0x1548E29C, 'sub_key': 0xD7, 'xor_first_byte': False}, b'eliF'),
    'neko_vol1_steam': (NekoCrypt, {'master_key': 0x44528B87, 'sub_key': 0x23, 'xor_first_byte': False}, b'eliF'),
    'neko_vol0': (NekoCrypt, {'master_key': 0x1548E29C, 'sub_key': 0xD7, 'xor_first_byte': True}, b'neko'),
    'neko_vol0_steam': (NekoCrypt, {'master_key': 0x44528B87, 'sub_key': 0x23, 'xor_first_byte': True}, b'neko'),
    'sousaku_kanojo': (AkabeiCrypt, {'m_seed': 0x2F91DE55}, b''),
}
