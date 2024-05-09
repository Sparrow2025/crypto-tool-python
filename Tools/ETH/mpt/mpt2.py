def string_to_ascii(string):
    # 将字符串转换为其 ASCII 表示形式
    ascii_representation = ""
    for char in string:
        ascii_representation += str(ord(char)) + " "
    return ascii_representation.strip()

# 示例用法
verb = b'do'
verb2 = b'dog'
verb3 = b'doge'
verb4 = b'horse'
print(verb.hex())
print(verb2.hex())
print(verb3.hex())
print(verb4.hex())

print(b''.hex())
