class Solution:
    def Sorted(self, s):

        def combine(element):
            nonlocal s
            if not s or element >= s[-1]:
                s.append(element)
                return

            current_element = s.pop()
            combine(element)
            s.append(current_element)

        def reduce():
            nonlocal s, combine
            if not s:
                return

            element = s.pop()
            reduce()
            combine(element)

        reduce()
