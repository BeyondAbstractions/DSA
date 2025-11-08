# https://www.geeksforgeeks.org/problems/reverse-a-stack/1?utm_source=youtube&utm_medium=collab_striver_ytdescription&utm_campaign=reverse-a-stack


class Solution:
    def reverse(self, St):

        def insert_last(st, element):

            if not st:
                st.append(element)
                return

            current = st.pop()
            insert_last(st, element)
            st.append(current)

        def solve(st):

            if not st:
                return

            element = st.pop()
            solve(st)
            insert_last(st, element)

        solve(St)
