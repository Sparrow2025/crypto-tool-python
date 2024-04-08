import hashlib

# 用来保存层层hash过程中产生的hash array
hashed_array = []


# 计算数据的哈希值
def calculate_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()


# 构建默克尔树
def build_merkle_tree(hashed_data_list):
    if len(hashed_data_list) == 1:
        return hashed_data_list[0]
    new_data_list = []
    for i in range(0, len(hashed_data_list), 2):
        if i + 1 < len(hashed_data_list):
            new_data_list.append(calculate_hash(hashed_data_list[i] + hashed_data_list[i + 1]))
        else:
            # 如果数据列表长度为奇数，最后两个数据保持一致
            new_data_list.append(calculate_hash(hashed_data_list[i] + hashed_data_list[i]))
    hashed_array.append(new_data_list)
    return build_merkle_tree(new_data_list)


# 验证默克尔树的有效性
def verify_merkle_tree(root_hash, leaf_hash, merkle_path):
    current_hash = leaf_hash
    for sibling_hash in merkle_path:
        if sibling_hash[0] == 'L':
            current_hash = calculate_hash(sibling_hash[1:] + current_hash)
        else:
            current_hash = calculate_hash(current_hash + sibling_hash[1:])
    return current_hash == root_hash


# 示例数据
data_list = ["Data1", "Data2", "Data3", "Data4", "Data5", "Data6", "Data7", "Data8"]

# 构建默克尔树
merkle_root = build_merkle_tree([calculate_hash(data) for data in data_list])
print("Merkle Root:", merkle_root)
print("All Hashed:", hashed_array)

# 验证叶子节点的有效性
data3_index = 2
data3_hash = calculate_hash(data_list[data3_index])
merkle_path = ['R' + calculate_hash(data_list[3]), 'L' + hashed_array[0][0], 'R' + hashed_array[1][1]]
print("Leaf Hash:", data3_hash)
print("Merkle Path:", merkle_path)
print("Is Valid:", verify_merkle_tree(merkle_root, data3_hash, merkle_path))
