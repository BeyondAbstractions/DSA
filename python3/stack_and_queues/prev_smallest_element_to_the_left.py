# https://www.geeksforgeeks.org/problems/smallest-number-on-left3403/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card


class Solution:
    def leftSmaller(self, n, arr):
        len_arr = n
        pse = [-1 for i in range(len_arr)]

        i = 1

        while 1:

            if i >= len_arr:
                break

            prev_idx = i - 1
            prev_element = arr[prev_idx]
            current_element = arr[i]

            while 1:

                if prev_element < current_element:
                    pse[i] = prev_idx
                    break

                prev_idx = pse[prev_idx]

                if prev_idx == -1:
                    break

                prev_element = arr[prev_idx]

            i += 1

        i = 0
        while 1:
            if i >= len_arr:
                break

            if pse[i] != -1:
                pse[i] = arr[pse[i]]

            i += 1

        return pse
