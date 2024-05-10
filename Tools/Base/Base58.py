import base58

# 要编码的数据
data = b'Hello, Base58!'

# 进行Base58编码
encoded = base58.b58encode(data)

# 进行Base58解码
decoded = base58.b58decode(encoded)

print("Base58编码结果:", encoded.decode())  # 解码为字符串并打印
print("Base58解码结果:", decoded.decode())  # 解码为字符串并打印
