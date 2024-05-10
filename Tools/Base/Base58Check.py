import base58
import hashlib


def base58check_decode(encoded):
    # 进行Base58解码
    decoded = base58.b58decode(encoded)

    # 验证数据长度
    if len(decoded) < 5:
        raise ValueError("Invalid Base58Check encoded data length")

    # 提取校验和
    checksum = decoded[-4:]

    # 计算校验和
    hash1 = hashlib.sha256(decoded[:-4]).digest()
    hash2 = hashlib.sha256(hash1).digest()
    expected_checksum = hash2[:4]

    # 比较校验和
    if checksum != expected_checksum:
        raise ValueError("Invalid Base58Check checksum")

    # 提取数据
    return decoded[:-4]  # 去除版本前缀和校验和


# 准备数据
data = b'Hello, Base58Check!'

# 计算两次SHA256哈希
hash1 = hashlib.sha256(data).digest()
hash2 = hashlib.sha256(hash1).digest()

# 取前4个字节作为校验和
checksum = hash2[:4]

# 添加校验和
data_with_checksum = data + checksum

# 进行Base58编码
base58check_encoded = base58.b58encode(data_with_checksum)
base58check_decode = base58check_decode(base58check_encoded)
print("Base58Check编码结果:", base58check_encoded.decode())  # 解码为字符串并打印
print("Base58Check解码结果:", base58check_decode.decode())  # 解码为字符串并打印
