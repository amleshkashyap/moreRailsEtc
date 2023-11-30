import math

class GenericSorts:
    def __init__(self):
        pass

    def merge_sort(self, array):
        if len(array) <= 1:
            return
        mid = len(array)//2
        left = array[:mid]
        right = array[mid:]

        self.merge_sort(left)
        self.merge_sort(right)

        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                array[k] = left[i]
                i += 1
            else:
                array[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            array[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            array[k] = right[j]
            j += 1
            k += 1


    def inplace_merge_sort(self, array):
        if len(array) <= 1:
            return

        mid = len(array)//2

        self.inplace_merge_sort(array[:mid])
        self.inplace_merge_sort(array[mid:])

        i = 0
        j = mid

        while i < len(array[:mid]) and j < len(array[mid:]):
            if array[i] > array[j]:
                array[i], array[j] = array[j], array[i]
            i += 1
            j += 1

        while i < len(array[:mid]):
            

        while j < len(array[mid:]):
            if array[j] > array[j-1]:
                array[j], array[j-1] = array[j-1], array[j]
            j += 1

    def partition(self, array):
        low = 0
        high = len(array) - 1
        pivot = array[high]

        i = -1

        for j in range(low, high-1):
            if array[j] <= pivot:
                i += 1
                array[i], array[j] = array[j], array[i]

        i += 1
        array[i], array[high] = array[high], array[i]
        return i

    def quick_sort(self, array):
        pass

    def insertion_sort(self, array):
        n = len(array)
        for i in range(n):
            for j in range(i, 0, -1):
                if array[j-1] > array[j]:
                    array[j], array[j-1] = array[j-1], array[j]


    def max_heapify(self, array, size, idx):
        l = 2 * idx + 1
        r = 2 * idx + 2
        max_idx = idx
        if l < size and array[l] > array[max_idx]:
            max_idx = l

        if r < size and array[r] > array[max_idx]:
            max_idx = r

        if idx != max_idx:
            array[idx], array[max_idx] = array[max_idx], array[idx]
            self.max_heapify(array, size, max_idx)


    def heapsort(self, array):
        n = len(array)
        start = n//2
        for i in range(start, -1, -1):
            self.max_heapify(array, n, i)

        for i in range(n-1, -1, -1):
            array[0], array[i] = array[i], array[0]
            self.max_heapify(array, i, 0)


    def introsort(self, array, maxdepth):
        n = len(array)
        if n < 16:
            self.insertion_sort(array)
        elif maxdepth == 0:
            self.heapsort(array)
        else:
            p = self.partition(array)
            array[:p] = self.introsort(array[:p], maxdepth - 1)
            array[p+1:] = self.introsort(array[p+1:], maxdepth - 1)
        return array

    def topological_sort(self, array):
        pass

    def radix_sort(self, array):
        pass


if __name__ == "__main__":
    testcases = [
            [1, 2, 3, 3, 8, 9, 11, 11, 12],
            [12, 11, 11, 9, 8, 3, 3, 2, 1],
            [1, 8, 9, 3, 11, 3, 12, 11, 2],
            [1, 8, 9, 6, 11, 3, 12, 4, 2],
            [12, 11, 11, 9, 8, 3, 3, 2, 1, 1, 2, 3, 3, 8, 9, 11, 11, 12, 1, 8, 9, 6, 11, 3, 12, 4, 2, 1, 8, 9, 3, 11, 3, 12, 11]
    ]

    sorter = GenericSorts()
    print("Testing MergeSort")
    for i in range(len(testcases)):
        t = testcases[i].copy()
        print(f"{i} - Sorting: {t}")
        sorter.merge_sort(t)
        print(f"             {t}")
        print("")

    print("Testing InsertionSort")
    for i in range(len(testcases)):
        t = testcases[i].copy()
        print(f"{i} - Sorting: {t}")
        sorter.insertion_sort(t)
        print(f"             {t}")
        print("")

    print("Testing Heapsort")
    for i in range(len(testcases)):
        t = testcases[i].copy()
        print(f"{i} - Sorting: {t}")
        sorter.heapsort(t)
        print(f"             {t}")
        print("")

    print("Testing IntroSort")
    for i in range(len(testcases)):
        t = testcases[i].copy()
        print(f"{i} - Sorting: {t}")
        maxdepth = 2 * math.floor(math.log2(len(t)))
        t1 = sorter.introsort(t, maxdepth)
        print(f"             {t}")
        print("")
