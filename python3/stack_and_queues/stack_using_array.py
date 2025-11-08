# https://www.geeksforgeeks.org/problems/implement-stack-using-array/1?utm_source=youtube&utm_medium=collab_striver_ytdescription&utm_campaign=implement-stack-using-array


class MyStack:

    def __init__(self):
        self.arr = []

    # Function to push an integer into the stack.
    def push(self, data):
        self.arr.append(data)

    # Function to remove an item from top of the stack.
    def pop(self):
        try:
            return self.arr.pop()
        except IndexError:
            return -1
