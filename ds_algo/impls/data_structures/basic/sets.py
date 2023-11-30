import random
class RandomizedSet:
    def __init__(self):
        self.data = {}
        self.array = []

    def insert(self, val: int) -> bool:
        if val in self.data:
            return False
        self.array.append(val)
        self.data[val] = len(self.array) - 1
        return True

    def remove(self, val: int) -> bool:
        if val in self.data:
            i = self.data[val]
            last = self.array[-1]
            self.array[i] = last
            self.data[last] = i
            self.array.pop()
            del self.data[val]
            return True
        return False

    def getRandom(self) -> int:
        i = random.randint(0, len(self.array) - 1)
        return self.array[i]

class RandomizedMultiset:
    def __init__(self):
        self.reset()

    def reset(self):
        self.data = {}
        self.array = []

    def insert(self, val: int) -> bool:
        self.array.append(val)
        insert_at = len(self.array) - 1
        if val in self.data:
            self.data[val].append(insert_at)
            return False
        self.data[val] = [insert_at]
        return True

    def remove(self, val: int) -> bool:
        if val not in self.data:
            return False

        idx = self.data[val]
        remove_from = idx[-1]

        # remove the last occurrence
        if len(idx) == 1:
            del self.data[val]
        else:
            self.data[val].pop()

        last_idx = len(self.array) - 1
        last = self.array[last_idx]
        self.array[remove_from] = last
        self.array.pop()

        if val == last:
            return True

        idx = self.data[last]
        if len(idx) == 1:
            self.data[last] = [i]
            return True

        # ensure that the last occurrence is always at the end for next correct removal
        idx = idx.index(last_idx)
        j = t - 1
        while(j > -1 and remove_from < idx[j]):
            idx[j+1] = idx[j]
            j -= 1
        idx[j+1] = remove_from
        self.data[last] = idx
        return True

    def getRandom(self) -> int:
        idx = random.randint(0, len(self.array) - 1)
        return self.array[idx]


if __name__ == "__main__":
    s = RandomizedSet()
    ms = RandomizedMultiset()
