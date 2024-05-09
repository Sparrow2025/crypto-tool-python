# 原始字符串
original_string = "Hello, Hex!"

# 编码
encoded_string = original_string.encode("utf-8").hex()
print("Encoded:", encoded_string)

# 解码
decoded_string = bytes.fromhex(encoded_string).decode("utf-8")
print("Decoded:", decoded_string)