class Solution:

    def stack_solution(self, arr):
        ret = [-1 for i in range(len(arr))]

        # the stack is always decreasing
        st = list()

        i = len(arr) - 1
        while i >= 0:
            if not st:
                st.append(i)
            else:
                current_index = i
                current_element = arr[i]
                while 1:
                    if st:
                        top_idx = st[-1]
                        top_element = arr[top_idx]
                        if top_element < current_element:
                            st.pop()
                            ret[top_idx] = current_index
                        else:
                            st.append(i)
                            break
                    else:
                        st.append(i)
                        break
            i -= 1

        i = 0

        while i < len(ret):
            if ret[i] != -1:
                ret[i] = arr[ret[i]]
            i += 1

        return ret

    def arr_solution(self, arr):
        ret = [-1 for i in range(len(arr))]
        j = 1
        while j < len(arr):
            current_element = arr[j]
            prev_indx = j - 1
            while 1:
                if prev_indx == -1:
                    ret[j] = -1
                    break

                prev_element = arr[prev_indx]

                if current_element < prev_element:
                    ret[j] = prev_indx
                    break
                else:
                    prev_indx = ret[prev_indx]

            j += 1

        i = 0

        while i < len(ret):
            if ret[i] != -1:
                ret[i] = arr[ret[i]]
            i += 1

        return ret

    # Function to find the next greater element for each element of the array.
    def nextLargerElement(self, arr):
        return self.stack_solution(arr)
        # return self.arr_solution(arr)
