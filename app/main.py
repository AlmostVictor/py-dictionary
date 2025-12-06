from typing import Any, Hashable


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value


class Dictionary:
    def __init__(self) -> None:
        self.hash_table: list[None | Node] = [None] * 8
        self.reserved_count = 0
        self.real_size = 8

    def save(self, saving_node: Node) -> None:
        for existed_node in self.hash_table:
            if existed_node and existed_node.key == saving_node.key:
                existed_node.value = saving_node.value
                return

        idx = hash(saving_node.key) % self.real_size
        for _ in range(self.reserved_count):
            if self.hash_table[idx] is None:
                self.hash_table[idx] = saving_node
                return
            else:
                idx = (idx + 1) % self.real_size

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self.save(Node(key, value))
        self.reserved_count += 1

        if self.reserved_count > self.real_size * 0.66:
            old_nodes = [node for node in self.hash_table if node]
            self.real_size *= 2
            self.hash_table = [None] * self.real_size
            for node in old_nodes:
                self.save(node)

    def __getitem__(self, key: Hashable) -> Any:
        for node in self.hash_table:
            if node and node.key == key:
                return node.value
        raise KeyError(key)

    def __len__(self) -> int:
        return self.reserved_count

    def clear(self) -> None:
        self.hash_table = [None] * 8
        self.reserved_count = 0
        self.real_size = 8

    def __delitem__(self, key: Hashable) -> None:
        for node in self.hash_table:
            if node and node.key == key:
                node = None
                return
        raise KeyError(key)

    def get(self, key: Hashable, default_value: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default_value
