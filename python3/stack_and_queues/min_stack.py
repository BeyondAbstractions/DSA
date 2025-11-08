# https://leetcode.com/problems/min-stack/


class MinStack:

    def __init__(self):
        self.st = list()

    def push(self, val: int) -> None:
        if not self.st:
            self.st.append((val, 0))
        else:
            small_idx = self.st[-1][-1]
            small_val = self.st[small_idx][0]
            if val < small_val:
                self.st.append((val, len(self.st)))
            else:
                self.st.append((val, small_idx))

    def pop(self) -> None:
        self.st.pop()[0]

    def top(self) -> int:
        return self.st[-1][0]

    def getMin(self) -> int:
        small_idx = self.st[-1][-1]
        small_val = self.st[small_idx][0]
        return small_val
