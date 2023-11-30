class BinarySearch:
    def __init__(self):
        pass

    def find_target(self, array, target):
        m = len(array)
        first, last = 0, m-1
        while(first <= last):
            mid = first + (last - first)//2
            if array[mid] == target:
                return mid
            elif array[mid] > target:
                last = mid - 1
            elif array[mid] < target:
                first = mid + 1
        return -1

    def find_smaller(self, array, target):
        if target < array[0]:
            return -1
        m = len(array)
        if target > array[-1]:
            return m-1
        first, last = 0, m-1
        while(first <= last):
            mid = first + (last - first)//2
            if array[mid] > target:
                last = mid - 1
            elif array[mid] < target:
                if mid < m-1 and array[mid+1] > target:
                    return mid
                elif mid == m-1:
                    return mid
                first = mid + 1
            else:
                while(mid > -1 and array[mid] == target):
                    mid -= 1
                return mid
        return mid

    def find_larger(self, array, target):
        m = len(array)
        if target > array[-1]:
            return -1
        if target < array[0]:
            return 0
        first, last = 0, m-1
        while(first <= last):
            mid = first + (last - first)//2
            if array[mid] > target:
                if mid > 0 and array[mid-1] < target:
                    return mid
                elif mid == 0:
                    return mid
                last = mid - 1
            elif array[mid] < target:
                first = mid + 1
            else:
                while(mid < m and array[mid] == target):
                    mid += 1
                if mid == m:
                    return -1
                else:
                    return mid
        return mid

    def find_smaller_or_target(self, array, target):
        m = len(array)
        if target < array[0]:
            return -1
        if target > array[-1]:
            return m-1
        first, last = 0, m-1
        while(first <= last):
            mid = first + (last - first)//2
            if array[mid] == target:
                return mid
            elif array[mid] > target:
                last = mid - 1
            else:
                if mid < m-1 and array[mid+1] > target:
                    return mid
                elif mid == m-1:
                    return mid
                first = mid + 1
        return mid

    def find_larger_or_target(self, array, target):
        m = len(array)
        if target > array[-1]:
            return -1
        if target < array[0]:
            return 0
        first, last = 0, m-1
        while(first <= last):
            mid = first + (last - first)//2
            if array[mid] == target:
                return mid
            elif array[mid] > target:
                if mid > 0 and array[mid-1] < target:
                    return mid
                elif mid == 0:
                    return mid
                last = mid - 1
            else:
                first = mid + 1
        return mid

    def bisect_and_find_peak(self, array, first, last):
        if last < first:
            return -1
        m = last - first
        n = len(array)
        mid = first + m//2
        if m == 0:
            if mid == 0:
                if array[0] > array[1]:
                    return 0
                return -1
            if mid == n-1:
                if array[n-1] > array[n-2]:
                    return n-1
                return -1
        elif mid == 0 and mid + 1 == n-1:
            if array[1] > array[0]:
                return 1
            return 0

        if array[mid] > array[mid+1] and array[mid] > array[mid-1]:
            return mid

        peak = self.bisect_and_find_peak(array, first, mid-1)
        if peak != -1:
            return peak

        peak = self.bisect_and_find_peak(array, mid+1, last)
        return peak
    
    def find_target_first_occurrence(self, array, target):
        pass

    def find_target_last_occurrence(self, array, target):
        pass


if __name__ == "__main__":
    testcases = [
        [ [1, 2, 3, 4, 5],          [2, 3, 5, 6, 0] ],
        [ [1, 2, 3, 4, 5, 6],       [2, 3, 5, 6, 0] ],
        [ [1, 1, 2, 3, 3, 4, 5],    [2, 3, 5, 6, 0] ],
        [ [1, 1, 2, 2, 3, 3, 4, 5], [2, 3, 5, 6, 0] ],
        [ [1, 1, 2, 3, 4, 5, 5],    [2, 3, 5, 6, 0] ],
        [ [1, 1, 2, 3, 3, 4, 5, 5], [2, 3, 5, 6, 0] ],
        [ [1, 2, 5, 8, 10],         [4, 7, 9] ]
    ]

    bs = BinarySearch()
    print("Finding Equal")
    for i in range(len(testcases)):
        array = testcases[i][0]
        for target in testcases[i][1]:
            res = bs.find_target(array, target)
            print(i, array, target, res)

    print("Finding Smaller")
    for i in range(len(testcases)):
        array = testcases[i][0]
        for target in testcases[i][1]:
            res = bs.find_smaller(array, target)
            print(i, array, target, res)

    print("Finding Larger")
    for i in range(len(testcases)):
        array = testcases[i][0]
        for target in testcases[i][1]:
            res = bs.find_larger(array, target)
            print(i, array, target, res)

    print("Finding Smaller Or Target")
    for i in range(len(testcases)):
        array = testcases[i][0]
        for target in testcases[i][1]:
            res = bs.find_smaller_or_target(array, target)
            if res == -1:
                print(i, array, target, res)
            elif array[res] == target:
                print(i, array, target, res, "Target")
            else:
                print(i, array, target, res, "Smaller")

    print("Finding Larger Or Target")
    for i in range(len(testcases)):
        array = testcases[i][0]
        for target in testcases[i][1]:
            res = bs.find_larger_or_target(array, target)
            if res == -1:
                print(i, array, target, res)
            elif array[res] == target:
                print(i, array, target, res, "Target")
            else:
                print(i, array, target, res, "Larger")
