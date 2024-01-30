from bitcoin.core import CTransaction, b2lx

def print_transaction_info(tx):
    print("Transaction Information:")
    print(f"  Version: {tx.nVersion}")
    print(f"  Inputs ({len(tx.vin)}):")
    for i, txin in enumerate(tx.vin):
        print(f"    Input {i + 1}:")
        print(f"      Previous Tx Output: {b2lx(txin.prevout.hash)}:{txin.prevout.n}")
        print(f"      ScriptSig: {txin.scriptSig.hex()}")
        # 获取witness
        witness_data = tx.wit.vtxinwit[i].scriptWitness.stack if tx.wit.vtxinwit else None
        if witness_data:
            print(f"      Witness (SegWit): {witness_data}")
    print(f"  Outputs ({len(tx.vout)}):")
    for i, txout in enumerate(tx.vout):
        print(f"    Output {i + 1}:")
        print(f"      Amount: {txout.nValue / 100000000} BTC")
        print(f"      ScriptPubKey (hex): {txout.scriptPubKey.hex()}")
    print(f"  Lock Time: {tx.nLockTime}")

# 输入你的原始交易数据
raw_transaction = "010000000181f46502fd3a9e7df61e409ace29acaba95130a041cd4467c299984d6849bd09010000006a47304402204300d701d7beb055b369955adf7fa39faedc2c0d1f1cd49b4c7e7913ac937d9c0220713f7f19b72e4399db2a1a627176c4a093db8ea72bb612dd949f3e0c0cf28a3c012103683ad7dd8a485e4be62e963d8f60cf51aca0652660b1ed8cf2b6b2a2e34631f0ffffffff01a0860100000000001976a9144d6567616e264769616e6e69466f72657665722188ac00000000"

# 将十六进制字符串转换为字节数组
raw_transaction_bytes = bytes.fromhex(raw_transaction)

# 使用CTransaction解析交易数据
tx = CTransaction.deserialize(raw_transaction_bytes)

# 打印交易信息
print_transaction_info(tx)

