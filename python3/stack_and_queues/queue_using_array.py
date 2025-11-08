# https://www.geeksforgeeks.org/problems/implement-queue-using-array/1?utm_source=youtube&utm_medium=collab_striver_ytdescription&utm_campaign=implement-queue-using-array

from collections import deque


class MyQueue:

    def __init__(self):
        self.q = deque()

    # Function to push an element x in a queue.
    def push(self, x):
        self.q.append(x)

    # Function to pop an element from queue and return that element.
    def pop(self):
        try:
            return self.q.popleft()
        except:
            return -1
