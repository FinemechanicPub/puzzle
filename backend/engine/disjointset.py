from collections import defaultdict


class DisjointSet:
    def __init__(self, size: int):
        self.parent = [i for i in range(size)]
        self.rank = [0] * size

    def find(self, item: int):
        if item == self.parent[item]:
            return item
        self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, first: int, second: int):
        first = self.find(first)
        second = self.find(second)
        if first == second:
            return
        if self.rank[first] < self.rank[second]:
            first, second = second, first
        self.parent[second] = first
        if self.rank[first] == self.rank[second]:
            self.rank[first] += 1

    def sets(self):
        _sets: dict[int, list[int]] = defaultdict(list)
        for item in range(len(self.parent)):
            _sets[self.find(item)].append(item)
        return list(_sets.values())

    def set_sizes(self):
        _sets: dict[int, int] = defaultdict(int)
        for item in range(len(self.parent)):
            _sets[self.find(item)] += 1
        return list(_sets.values())
