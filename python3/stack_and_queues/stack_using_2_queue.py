# https://leetcode.com/problems/implement-stack-using-queues/

from collections import deque


class MyStack:

    def __init__(self):
        self.push_q = deque()
        self.pop_q = deque()

    def push(self, x: int) -> None:
        self.push_q.append(x)
        while self.pop_q:
            self.push_q.append(self.pop_q.popleft())
        self.push_q, self.pop_q = self.pop_q, self.push_q

    def pop(self) -> int:
        return self.pop_q.popleft()

    def top(self) -> int:
        return self.pop_q[0]

    def empty(self) -> bool:
        return not bool(self.pop_q)
