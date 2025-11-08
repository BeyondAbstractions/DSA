# https://leetcode.com/problems/online-stock-span/


class StockSpanner:

    def __init__(self):
        self.prices = list()
        self.nge = list()

    def next_greatest_element_to_left(self):
        j = len(self.prices) - 1
        current_element = self.prices[j]
        prev_indx = j - 1
        while 1:
            if prev_indx == -1:
                self.nge[j] = -1
                break

            prev_element = self.prices[prev_indx]

            if prev_element > current_element:
                self.nge[j] = prev_indx
                break
            else:
                prev_indx = self.nge[prev_indx]

    def next(self, price: int) -> int:
        self.nge.append(-1)
        self.prices.append(price)
        self.next_greatest_element_to_left()
        if self.nge[-1] == -1:
            return len(self.prices)
        else:
            return len(self.prices) - self.nge[-1] - 1
