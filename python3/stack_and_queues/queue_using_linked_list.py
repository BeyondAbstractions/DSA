# https://www.geeksforgeeks.org/problems/implement-queue-using-linked-list/1?utm_source=youtube&utm_medium=collab_striver_ytdescription&utm_campaign=implement-queue-using-linked-list


class Node:

    def __init__(self, data=None):
        self.data = data
        self.next = None


class MyQueue:

    def __init__(self):
        self.head = None
        self.tail = None

    # Function to push an element into the queue.
    def push(self, item):
        it = self.head
        while it is not self.tail:
            it = it.next
        n = Node(data=item)
        if it is None:
            self.head = n
            self.tail = n
        else:
            self.tail.next = n
            self.tail = self.tail.next

    # Function to pop front element from the queue.
    def pop(self):
        it = self.head
        if it is None:
            return -1
        ret = it.data
        self.head = it.next
        if self.head is None:
            self.tail = self.head
        it.next = None
        return ret
