from ecdsa import VerifyingKey, SECP256k1, util
from binascii import unhexlify

def verify_signature(transaction_hex, input_hex, public_key_hex, signature_hex):
    # 将十六进制字符串形式的交易、输入、公钥和签名转换为字节数组
    transaction = unhexlify(transaction_hex)
    input_data = unhexlify(input_hex)
    public_key = unhexlify(public_key_hex)
    signature = unhexlify(signature_hex)

    # 提取交易的消息部分（包含输入脚本）
    transaction_message = transaction[: -len(input_data)]

    # 解码 DER 编码的签名
    r, s = util.sigdecode_der(signature[4:], SECP256k1.order)

    # 创建 VerifyingKey 对象
    verifying_key = VerifyingKey.from_string(public_key, curve=SECP256k1)

    # 使用 ECDSA 验证签名
    if verifying_key.verify((r, s), transaction_message):
        print("签名验证成功！")
    else:
        print("签名验证失败。")

# 示例数据
transaction_hex = "010000000181f46502fd3a9e7df61e409ace29acaba95130a041cd4467c299984d6849bd09010000006a47304402204300d701d7beb055b369955adf7fa39faedc2c0d1f1cd49b4c7e7913ac937d9c0220713f7f19b72e4399db2a1a627176c4a093db8ea72bb612dd949f3e0c0cf28a3c012103683ad7dd8a485e4be62e963d8f60cf51aca0652660b1ed8cf2b6b2a2e34631f0ffffffff01a0860100000000001976a9144d6567616e264769616e6e69466f72657665722188ac00000000"
input_hex = "0100000001d29238890c25f5ec5c8e269c5fd98ff8968a6c6e43c0846064df79544c138264240000008a473044022058cc79c8b7afc176241f5089d36f1cb57dad04996c33c1e3f5de74d4ef32ede702205ad3738871dc548551fa6f485fae2df44d560b54440f53a62469ebe10f1643310141043362b9b0904c205d457488eb85ea4549cbbee4159a9fd48bcf37a352898b9628be8409052352980708de7e4258568278ec118e93a3939166deb820b80c15b71dffffffff02300b1e00000000001976a914b3aebe5ba69e568857bcb6dfc2a4fb806164b9e088ac40420f00000000001976a914a59a2816a7d1e6c163e6c164cd3a463727f1a4c388ac00000000"
public_key_hex = "03362b9b0904c205d457488eb85ea4549cbbee4159a9fd48bcf37a352898b9628b"
signature_hex = "3045022100b75eb4b8e3f6fb2bfedf7db15a22e453fb2eef33cf49c5f946c801c4f8f03175022037a4a0a2f8b22b4c0701605d7bc13f0d951db4625e0a79dd7eb6c110d6876321"

# 调用验证函数
verify_signature(transaction_hex, input_hex, public_key_hex, signature_hex)
