import base64

# 原始字符串
original_string = "Hello, Base64!"

# 编码
encoded_string = base64.b64encode(original_string.encode("utf-8")).decode("utf-8")
print("Encoded:", encoded_string)

# 解码
decoded_string = base64.b64decode(encoded_string).decode("utf-8")
print("Decoded:", decoded_string)