#!/usr/bin/env python3

from hdwallet import HDWallet
from hdwallet.utils import generate_entropy
from hdwallet.symbols import BTC as SYMBOL
from typing import Optional

import json

# 以下的`位`没有特殊说明都是指的bit
# 选择`熵`长度, 默认128位，最长256位，必须是32的倍数
# 校验和 = sha256(`熵`)的哈希值 的 前(`熵`的位数 / 32)位 -- 如果128位的熵，那么就是取前4位
# 助记词的数量 = (`熵`的位数 + 校验和的位数) / 11 -- 这里的 + 表示拼接的意思，每11位bit就是从 0-2047 中的一个数字，这个数字就是词本中的具体哪个单词
STRENGTH: int = 128
# language english, french, italian, spanish, chinese_simplified, chinese_traditional, japanese or korean
# 这里使用英文词本
LANGUAGE: str = "english"  # Default is english
# 用16进制的字符串表示`熵`
ENTROPY: str = generate_entropy(strength=STRENGTH)
# 这里可以选择一个密码，我们暂时不用
PASSPHRASE: Optional[str] = None  # "meherett"
# 初始化
hdwallet: HDWallet = HDWallet(symbol=SYMBOL, use_default_path=False)
# 生成助记词
hdwallet.from_entropy(
    entropy=ENTROPY, language=LANGUAGE, passphrase=PASSPHRASE
)

# Derivation from path
# hdwallet.from_path("m/44'/0'/0'/0/0")
# Or derivation from index
# 确定私钥的生成规则
hdwallet.from_index(44, hardened=True)
hdwallet.from_index(0, hardened=True)
hdwallet.from_index(0, hardened=True)
hdwallet.from_index(0)
hdwallet.from_index(0)

# 输出生成的结果
print(json.dumps(hdwallet.dumps(), indent=4, ensure_ascii=False))