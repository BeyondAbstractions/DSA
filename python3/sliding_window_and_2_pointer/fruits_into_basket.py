# https://www.geeksforgeeks.org/problems/fruit-into-baskets-1663137462/1


def counter_add(d: dict, k):
    if k not in d:
        d[k] = 1
    else:
        d[k] += 1


def counter_sub(d: dict, k):
    if k in d:
        d[k] -= 1
        if d[k] == 0:
            del d[k]


def get_total(d: dict):
    total = 0
    for v in d.values():
        total += v
    return total


class Solution:
    def totalFruits(self, arr):
        basket = dict()
        i = 0
        j = 0
        total = 0
        arr_len = len(arr)

        while 1:
            if j >= arr_len:
                break

            counter_add(basket, arr[j])
            while len(basket) > 2:
                counter_sub(basket, arr[i])
                i += 1

            total = max(total, get_total(basket))
            j += 1

        return total
