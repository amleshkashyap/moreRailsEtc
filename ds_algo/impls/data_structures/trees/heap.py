from util import Util

class MaxBinaryHeap:
    def __init__(self, array):
        self.heapArray = array
        self.size = len(array)

    def maxHeapify(self, array, size, idx):
        l = 2 * idx + 1
        r = 2 * idx + 2
        maxval_idx = idx

        if l < size and array[l] > array[maxval_idx]:
            maxval_idx = l

        if r < size and array[r] > array[maxval_idx]:
            maxval_idx = r

        if maxval_idx != idx:
            array[idx], array[maxval_idx] = array[maxval_idx], array[idx]
            self.maxHeapify(array, size, maxval_idx)

    def minHeapify(self, array, size, idx):
        l = 2 * idx + 1
        r = 2 * idx + 1
        minval_idx = idx

        if l < size and array[l] < array[minval_idx]:
            minval_idx = l

        if r < size and array[r] < array[minval_idx]:
            minval_idx = r

        if idx != minval_idx:
            array[idx], array[minval_idx] = array[minval_idx], array[idx]
            self.minHeapify(array, size, minval_idx)

    def minHeapifiedInsert(self, array, idx):
        parent = (idx - 1)//2
        if parent >= 0 and array[parent] > array[idx]:
            array[parent], array[idx] = array[idx], array[parent]
            self.minHeapifiedInsert(array, parent)

    def maxHeapifiedInsert(self, array, idx):
        parent = (idx - 1)//2
        if parent >= 0 and array[parent] < array[idx]:
            array[parent], array[idx] = array[idx], array[parent]
            self.maxHeapifiedInsert(array, parent)

    # expects an existing max heap and sorts it in ascending order
    # for descending order, another method can be written with min-heap
    def heapSort(self, array, size):
        for i in range(size - 1, -1, -1):
            array[0], array[i] = array[i], array[0]
            self.maxHeapify(array, i, 0)

    def buildMaxHeap(self, array, size):
        start = self.size // 2 - 1
        for i in range(start, -1, -1):
            self.maxHeapify(array, i, 0)

    def buildMinHeap(self, array, size):
        start = self.size//2 - 1
        for i in range(start, -1, -1):
            self.minHeapify(array, i, 0)

    def delete(self, num):
        pass

    def getHeap(self):
        return self.heapArray


if __name__ == "__main__":
    array = [3, 7, 8, 4, 3, 1, 2, 3, 1, 2, 4, 5, 5, 6, 1, 1, 2, 1, 2, 2]
    print(array)
    heap = MaxBinaryHeap(array)
    heap.buildMaxHeap(heap.heapArray, heap.size)
    print(f"Max Heap: {heap.heapArray}")
    Util.print_array_as_tree(heap.heapArray)
    print("")
    heap.heapSort(heap.heapArray, heap.size)
    print(f"Sorted: {heap.heapArray}")
    Util.print_array_as_tree(heap.heapArray)

    print("")
    array = [3, 7, 8, 4, 3, 1, 2, 3, 1, 2, 4, 5, 5, 6, 1, 1, 2, 1, 2, 2]
    print(array)
    heap = MaxBinaryHeap([])
    for i in array:
        heap.heapArray.append(i)
        heap.size += 1
        heap.maxHeapifiedInsert(heap.heapArray, heap.size - 1)
    print(f"Max Heap: {heap.heapArray}")
    Util.print_array_as_tree(heap.heapArray)
