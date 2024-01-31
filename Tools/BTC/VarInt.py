def encode_varint(value):
    if value < 0xfd:
        return bytes([value])
    elif value <= 0xffff:
        return b'\xfd' + value.to_bytes(2, 'little')
    elif value <= 0xffffffff:
        return b'\xfe' + value.to_bytes(4, 'little')
    else:
        return b'\xff' + value.to_bytes(8, 'little')


def decode_varint(data):
    first_byte = data[0]
    if first_byte < 0xfd:
        return first_byte, 1
    elif first_byte == 0xfd:
        return int.from_bytes(data[1:3], 'little'), 3
    elif first_byte == 0xfe:
        return int.from_bytes(data[1:5], 'little'), 5
    elif first_byte == 0xff:
        return int.from_bytes(data[1:9], 'little'), 9


# 示例
# 这里输入整数值
value = 100000
encoded_varint = encode_varint(value)
decoded_varint, length = decode_varint(encoded_varint)

print("Original Value:", value)
print("Encoded VarInt:", "0x" + encoded_varint.hex())
print("Decoded VarInt:", decoded_varint)
print("Length:", length)
