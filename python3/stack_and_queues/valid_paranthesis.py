class Solution:

    def isValid(self, s: str) -> bool:
        st = list()
        for c in s:
            if c in "({[":
                st.append(c)
            elif c == ")":
                if len(st) == 0:
                    return False
                if st[-1] == "(":
                    st.pop()
                else:
                    return False
            elif c == "}":
                if len(st) == 0:
                    return False
                if st[-1] == "{":
                    st.pop()
                else:
                    return False
            elif c == "]":
                if len(st) == 0:
                    return False
                if st[-1] == "[":
                    st.pop()
                else:
                    return False
        return True
