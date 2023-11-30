class MinStack:
    def __init__(self):
        self.reset()

    def push(self, val: int) -> None:
        self.array.append(val)
        if len(self.array) == 1:
            self.min = val
            self.freq = 1
        elif val == self.min:
            self.freq += 1
        elif val < self.min:
            self.min = val
            self.freq = 1
        
    def pop(self) -> None:
        val = self.array.pop()
        if val == self.min:
            self.freq -= 1
            if self.freq == 0 and len(self.array) > 0:
                self.min = min(self.array)
                self.freq = 1

    def top(self) -> int:
        return self.array[-1]        

    def getMin(self) -> int:
        return self.min

    def reset(self) -> None:
        self.array = []
        self.min = None
        self.freq = 0


if __name__ == "__main__":
    stack = MinStack()
    ops = [
            ["push","push","push","top","pop","getMin","pop","getMin","pop","push","top","getMin","push","top","getMin","pop","getMin"],
            ["push","push","push","getMin","pop","top","getMin"]
    ]
    push_numbers = [
            [2147483646,2147483646,2147483647,2147483647,-2147483648],
            [-2,0,-3]
    ]

    for i in range(len(ops)):
        print(f"Starting testcase: {i}")
        o = ops[i]
        n = push_numbers[i]
        count = 0
        for j in ops[i]:
            if j == "push":
                v = stack.push(n[count])
                count += 1
            elif j == "pop":
                v = stack.pop()
            elif j == "getMin":
                v = stack.getMin()
            elif j == "top":
                v = stack.top()
            else:
                v = None
            print(f"  op: {j}, res: {v}, stack: {stack.array}")
        stack.reset()
        print("")
