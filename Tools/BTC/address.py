import ecdsa
import hashlib
import base58


# 从16进制私钥计算出压缩，非压缩的公钥
def private_key_to_public_key(private_key):
    # 转换私钥为bytes
    private_key_bytes = bytes.fromhex(private_key)

    # 使用ECDSA库进行椭圆曲线加密
    sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)

    # 获取公钥
    vk = sk.get_verifying_key()

    # 获取未压缩的公钥（64字节）
    uncompressed_public_key = vk.to_string()

    # 获取压缩后的公钥
    compressed_public_key = vk.to_string("compressed")

    return uncompressed_public_key.hex(), compressed_public_key.hex()


# 从public_key计算出BTC地址
def public_key_to_address(public_key_hex):
    # 将公钥进行哈希（SHA256 和 RIPEMD160）
    sha256_hash = hashlib.sha256(bytes.fromhex(public_key_hex)).digest()
    ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()

    # 添加版本字节
    extended_hash = b'\x00' + ripemd160_hash  # 主网比特币地址版本字节为0x00

    # 使用两次SHA256进行校验和计算
    checksum = hashlib.sha256(hashlib.sha256(extended_hash).digest()).digest()[:4]

    # 添加校验和
    binary_address = extended_hash + checksum

    # 使用Base58进行编码
    bitcoin_address = base58.b58encode(binary_address).decode('utf-8')

    return bitcoin_address


# 从16进制的私钥计算出WIF格式的私钥
def private_key_to_wif(private_key_hex):
    # 添加版本字节
    extended_key = b'\x80' + bytes.fromhex(private_key_hex) + b'\x01'  # 主网比特币私钥版本字节为0x80, 0x01表示使用压缩公钥

    # 使用两次SHA256进行校验和计算
    checksum = hashlib.sha256(hashlib.sha256(extended_key).digest()).digest()[:4]

    # 添加校验和
    extended_key_with_checksum = extended_key + checksum

    # 使用Base58进行编码
    wif_key = base58.b58encode(extended_key_with_checksum).decode('utf-8')

    return wif_key


# 替换下面的private_key为你的BTC私钥
private_key = "2d9e386e9d7d3f3d128f344c9729d29bd2a27044214c789bf8574e5323b3602b"
wif_private_key = private_key_to_wif(private_key)
print("输入的BTC私钥为:", private_key)
print("WIF格式的私钥:", wif_private_key)

public_key_array = private_key_to_public_key(private_key)

print("BTC公钥(未压缩，16进制表示):", public_key_array[0])
print("BTC公钥(压缩，16进制表示):", public_key_array[1])

bitcoin_address = public_key_to_address(public_key_array[1])
print("BTC address:", bitcoin_address)
