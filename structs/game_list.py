from typing import Type

from encrypt import NoCrypt, NekoCrypt, EncryptInterface, AkabeiCrypt, HashCrypt

game_list: dict[str: tuple[tuple[Type[EncryptInterface], dict[str, int | bool], bytes]]] = {
    # Master key, secondary key, XOR the first byte, segment name (for packing)
    # 👇 加密算法，加密參數的 dict，遺留的臭大糞 chunk 名

    'none': (NoCrypt, {}, b''),  
    # General none encrypted game

    'neko_vol1': (NekoCrypt, {'master_key': 0x1548E29C, 'sub_key': 0xD7, 'xor_first_byte': False}, b'eliF'),
    # Nekopara Vol.1

    'neko_vol1_steam': (NekoCrypt, {'master_key': 0x44528B87, 'sub_key': 0x23, 'xor_first_byte': False}, b'eliF'),
    # Nekopara Vol.1 Steam

    'neko_vol0': (NekoCrypt, {'master_key': 0x1548E29C, 'sub_key': 0xD7, 'xor_first_byte': True}, b'neko'),
    # Nekopara Vol.0

    'neko_vol0_steam': (NekoCrypt, {'master_key': 0x44528B87, 'sub_key': 0x23, 'xor_first_byte': True}, b'neko'),
    # Nekopara Vol.0 Steam
    
    'sousaku_kanojo': (AkabeiCrypt, {'m_seed': 0x2F91DE55}, b''),
    'suiren_to_shion': (AkabeiCrypt, {'m_seed': 0x2F91DE55}, b''),
    # 創作彼女的戀愛方程式
    # 水蓮と紫苑

    'onenuki': (HashCrypt, {}, b''),
    # お姉様の代わりに抜いてあげます
}
