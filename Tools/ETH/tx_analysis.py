import web3
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://ethereum-sepolia-rpc.publicnode.com'))
print("Web3 RPC Status: ", w3.is_connected())
pk = '0x4f1c508199650369ddc6293d8bcbbe658ebb7fb0b241636964edc16dc1edef44'


def get_tx(hash_str):
    return w3.eth.get_transaction(hash_str)


def sign_transaction(from_address, to_address, value):
    # 1. 构建交易
    transaction = {
        'from': from_address,
        'to': to_address,
        'value': value,
        'nonce': w3.eth.get_transaction_count(from_address),
        'gas': 200000,
        'maxFeePerGas': 2000000000,
        'maxPriorityFeePerGas': 1000000000,
        # 这里需要指定chainId，否则会报错 Invalid Sender
        'chainId': 11155111
    }

    # 2. 签名交易
    signed = w3.eth.account.sign_transaction(transaction, pk)
    # 3. 发送交易
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    # 4. 根据交易hash查询交易
    tx = w3.eth.get_transaction(tx_hash)
    assert tx["from"] == from_address
    print("交易成功，交易hash: ", tx_hash.hex())


if __name__ == "__main__":
    b = Web3.from_wei(w3.eth.get_balance('0x6e0eE795051b89193273f7A9df1B4393D97ba563'), "ether")
    print("账户余额: ", b, "ETH")
    sign_transaction(from_address='0x6e0eE795051b89193273f7A9df1B4393D97ba563',
                     to_address='0x6E006CE71555B03DE544f984a0Ac28a72B528d52',
                     value=1000000000)
