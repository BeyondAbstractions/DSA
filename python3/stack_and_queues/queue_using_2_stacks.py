# https://leetcode.com/problems/implement-queue-using-stacks/


class MyQueue:

    def __init__(self):
        self.push_st = list()
        self.pop_st = list()

    def push(self, x: int) -> None:
        self.push_st.append(x)
        while self.pop_st:
            self.push_st.append(self.pop_st.pop())
        self.push_st, self.pop_st = self.pop_st, self.push_st

    def pop(self) -> int:
        return self.pop_st.pop()

    def peek(self) -> int:
        return self.pop_st[-1]

    def empty(self) -> bool:
        return not bool(self.pop_st)
