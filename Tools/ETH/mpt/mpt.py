class Node:
    def __init__(self, node_type, value=None):
        # 初始化节点，指定节点类型和值
        self.node_type = node_type
        self.value = value
        self.children = {}


class MPTree:
    def __init__(self):
        # 初始化 MPT 树，根节点为扩展节点
        self.root = Node("extension")

    def insert(self, key, value):
        # 插入键值对到 MPT 树
        self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        if len(key) == 0:
            # 如果键为空，则当前节点为叶子节点，存储值
            node.value = value
            node.node_type = "leaf"
            return

        if node.node_type == "extension":
            # 如果当前节点为扩展节点
            prefix = key[0]
            if prefix in node.children:
                # 如果子节点存在相同的前缀，递归插入到子节点
                self._insert(node.children[prefix], key[1:], value)
            else:
                # 否则创建一个新的叶子节点作为子节点
                leaf_node = Node("leaf", value)
                node.children[prefix] = leaf_node
        elif node.node_type == "leaf":
            # 如果当前节点为叶子节点
            common_prefix = self._calculate_common_prefix(node.value, key)
            if common_prefix:
                # 如果当前键与节点值有公共前缀，则创建一个新的扩展节点作为父节点
                new_extension_node = Node("extension")
                node.value = node.value[len(common_prefix):]
                new_extension_node.children[node.value[0]] = node
                remaining_key = key[len(common_prefix):]
                new_leaf_node = Node("leaf", value)
                new_extension_node.children[remaining_key[0]] = new_leaf_node
                self.root = new_extension_node
            else:
                # 如果没有公共前缀，则创建一个新的分支节点
                branch_node = Node("branch")
                branch_node.children[node.value[0]] = node
                remaining_key = key[1:]
                new_leaf_node = Node("leaf", value)
                branch_node.children[remaining_key[0]] = new_leaf_node
                self.root = branch_node

    def _calculate_common_prefix(self, str1, str2):
        # 计算两个字符串的公共前缀
        prefix = ""
        for a, b in zip(str1, str2):
            if a == b:
                prefix += a
            else:
                break
        return prefix

    def get(self, key):
        # 获取指定键对应的值
        return self._get(self.root, key)

    def _get(self, node, key):
        if len(key) == 0:
            # 如果键为空，则返回当前节点的值
            return node.value

        prefix = key[0]
        if node.node_type == "extension" and prefix in node.children:
            # 如果当前节点为扩展节点且存在相同的前缀，递归获取子节点的值
            return self._get(node.children[prefix], key[1:])
        elif node.node_type == "branch" and prefix in node.children:
            # 如果当前节点为分支节点且存在相同的前缀，递归获取子节点的值
            return self._get(node.children[prefix], key[1:])
        else:
            # 如果不存在相同的前缀，则键不存在于树中
            return None


# 测试用例
if __name__ == "__main__":
    mpt = MPTree()
    mpt.insert("apple", "fruit")
    mpt.insert("banana", "fruit")
    mpt.insert("app", "application")
    mpt.insert("bat", "animal")

    # 测试插入和获取功能
    assert mpt.get("apple") == "fruit"
    assert mpt.get("banana") == "fruit"
    assert mpt.get("app") == "application"
    assert mpt.get("bat") == "animal"
    assert mpt.get("foo") is None

    print("All test cases passed!")
