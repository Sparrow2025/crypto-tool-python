class PatriciaNode:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.children = {}

    def __str__(self):
        return f"Key: {self.key}, Value: {self.value}, Children: {list(self.children.keys())}"


class PatriciaTree:
    def __init__(self):
        self.root = PatriciaNode()

    def insert(self, key, value):
        if not key:
            return  # Ignore empty key
        self._insert_recursive(self.root, key, value)

    def _insert_recursive(self, node, key, value):
        if not key:
            node.value = value
            return

        for child_key in node.children:
            # 检查匹配情况
            common_prefix = self._longest_common_prefix(child_key, key)
            if common_prefix:
                if common_prefix == len(child_key):
                    # 全匹配的情况:直接在匹配的节点添加children
                    # Continue traversal
                    self._insert_recursive(node.children[child_key], key[common_prefix:], value)
                else:
                    # 不完全匹配的情况下，需要拆分节点
                    # 1. 拆分节点
                    # 2. 给拆分出来的节点添加children
                    # 3. 拆分出的点击的父节点需要更改key
                    # Split node
                    split_node = PatriciaNode(child_key[common_prefix:])
                    split_node.value = node.children[child_key].value
                    split_node.children = node.children[child_key].children
                    node.children[child_key[0:common_prefix]] = PatriciaNode(child_key[0:common_prefix])
                    node.children[child_key[0:common_prefix]].children = {child_key[common_prefix:]: split_node}
                    del node.children[child_key]
                    child_key = child_key[0:common_prefix]
                    if common_prefix < len(key):
                        node.children[child_key].children[key[common_prefix:]] = PatriciaNode(key[common_prefix:],
                                                                                              value)
                    else:
                        node.children[child_key].value = value
                return
        # 没有匹配的情况，直接插入
        node.children[key] = PatriciaNode(key, value)

    def search(self, key):
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node, key):
        if not key:
            return node.value

        for child_key in node.children:
            if key.startswith(child_key):
                return self._search_recursive(node.children[child_key], key[len(child_key):])

        return None

    # 这里获取两个字符串的最长前缀匹配
    def _longest_common_prefix(self, str1, str2):
        min_len = min(len(str1), len(str2))
        for i in range(min_len):
            if str1[i] != str2[i]:
                return i
        return min_len

    def __str__(self):
        return self._stringify(self.root)

    def _stringify(self, node, depth=0):
        result = "  " * depth + str(node) + "\n"
        for child_key in sorted(node.children.keys()):  # Sort children keys
            result += self._stringify(node.children[child_key], depth + 1)
        return result


# 测试
if __name__ == "__main__":
    tree = PatriciaTree()

    tree.insert("alice", 10)
    tree.insert("alivea", 20)
    tree.insert("aitana", 30)
    tree.insert("abanoub", 15)
    tree.insert("aicha", 18)
    tree.insert("abiy", 100)

    print(tree.search("alice"))  # Output: 10
    print(tree.search("alivea"))  # Output: 20
    print(tree.search("aitana"))  # Output: 30
    print(tree.search("abanoub"))  # Output: 15
    print(tree.search("aicha"))  # Output: 18
    print(tree.search("abiy"))  # Output: 100

    print("\nPatricia Tree Structure:")
    print(tree)
