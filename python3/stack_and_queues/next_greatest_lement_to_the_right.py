# https://www.geeksforgeeks.org/problems/next-larger-element-1587115620/1


class Solution:

    def stack_solution(self, arr):
        ret = [-1 for i in range(len(arr))]

        # the stack is always descreasing
        st = list()

        i = 0
        while i < len(arr):
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
            i += 1

        i = 0

        while i < len(ret):
            if ret[i] != -1:
                ret[i] = arr[ret[i]]
            i += 1

        return ret

    def arr_solution(self, arr):
        ret = [-1 for i in range(len(arr))]
        j = len(arr) - 2
        while j >= 0:
            current_element = arr[j]
            next_index = j + 1
            while 1:
                if next_index == -1:
                    ret[j] = -1
                    break

                next_element = arr[next_index]

                if current_element < next_element:
                    ret[j] = next_index
                    break
                else:
                    next_index = ret[next_index]

            j -= 1

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
