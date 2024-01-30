import ecdsa
import hashlib
from bitcoinlib.keys import Key
from bitcoinlib.transactions import Transaction



def sign_transaction(private_key, transaction, txid, vout):
# 使用私钥创建 ECDSA 签名对象
    signing_key = ecdsa.SigningKey.from_string(bytes.fromhex(private_key), curve=ecdsa.SECP256k1)

# 获取交易输入对应的输出的脚本
    script_pubkey = transaction.tx_inputs[0].get_output().script

# 计算交易数据的哈希值
    transaction_hash = hashlib.sha256(transaction.serialize()).digest()

# 使用私钥对交易哈希进行签名
    signature = signing_key.sign(transaction_hash)

# 构建输入脚本
    input_script = script_pubkey + bytes([len(signature)]) + signature
    transaction.tx_inputs[0].script = input_script
    return transaction

# 示例私钥和交易数据
private_key = "2d9e386e9d7d3f3d128f344c9729d29bd2a27044214c789bf8574e5323b3602b"
sender_address = Key(private_key).address()
receiver_address = "1KFHE7w8BhaENAswwryaoccDb6qcT6DbYY"
amount = 1.0

# 创建交易
transaction = Transaction()
transaction.add_input(prev_txid='5787c3d0740f13f280118404405f1c93fb7a63a953fa482b13e23c3b03a14bd4', output_n=0)
signed_transaction = sign_transaction(private_key, transaction, '5787c3d0740f13f280118404405f1c93fb7a63a953fa482b13e23c3b03a14bd4', 0)

# 构建交易数据
transaction_data = transaction.raw_hex()

# 进行交易签名
signature_result = sign_transaction(private_key, transaction_data)

# 将签名添加到交易输入脚本中
transaction.inputs[0].scriptSig = signature_result + bytes([len(signature_result)]) + bytes.fromhex(private_key)

# 打印签名后的交易数据
signed_transaction_data = transaction.serialize()
print("Signed Transaction Data:", signed_transaction_data.hex())
