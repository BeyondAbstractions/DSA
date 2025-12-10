import track
import functools
import random
import pprint


class Function:

    @track.track
    @staticmethod
    def rod_cutting_complex(n):
        if n <= 0:
            return

        for i in range(1, n):
            Function.rod_cutting_complex(n=i)
            Function.rod_cutting_complex(n=n - i)

    @track.track
    @functools.cache
    @staticmethod
    def rod_cutting_complex_cached(n):
        if n <= 0:
            return

        for i in range(1, n):
            Function.rod_cutting_complex_cached(n=i)
            Function.rod_cutting_complex_cached(n=n - i)

    @track.track
    @staticmethod
    def rod_cutting_uncached(n):
        if n <= 0:
            return

        for i in range(1, n):
            Function.rod_cutting_uncached(n=n - i)

    @track.track
    @functools.cache
    @staticmethod
    def rod_cutting_cached(n):
        if n > 1:
            for i in range(1, n):
                Function.rod_cutting_cached(n=n - i)

    @track.track
    @staticmethod
    def matrix_chain_multiplication(i, j):
        if i >= j:
            return
        else:
            for k in range(i, j):
                Function.matrix_chain_multiplication(i=i, j=k)
                Function.matrix_chain_multiplication(i=k + 1, j=j)

    @track.track
    @functools.cache
    @staticmethod
    def matrix_chain_multiplication_cached(i, j):
        if i >= j:
            return
        else:
            for k in range(i, j):
                Function.matrix_chain_multiplication_cached(i=i, j=k)
                Function.matrix_chain_multiplication_cached(i=k + 1, j=j)

    @track.track
    @staticmethod
    def func4(i, j):
        for k in range(i, j):
            Function.func4(i=k, j=j - k)

    @track.track
    @functools.cache
    @staticmethod
    def cached_func4(i, j):
        for k in range(i, j):
            Function.cached_func4(i=k, j=j - k)

    @track.track
    @staticmethod
    def fibonacci_uncached(n):
        if n <= 1:
            return
        Function.fibonacci_uncached(n - 1)
        Function.fibonacci_uncached(n - 2)

    @track.track
    @functools.cache
    @staticmethod
    def fibonacci_cached(n):
        if n <= 1:
            return
        Function.fibonacci_cached(n - 1)
        Function.fibonacci_cached(n - 2)

    @track.track
    @staticmethod
    def merge_sort(l, r):
        if l >= r:
            return
        mid = (l + r) // 2
        Function.merge_sort(l, mid)
        Function.merge_sort(mid + 1, r)

    @track.track
    @staticmethod
    def stock_buy_sell(i, have_stock):
        if i < 0:
            return
        Function.stock_buy_sell(i=i - 1, have_stock=True)
        Function.stock_buy_sell(i=i - 1, have_stock=False)

    @track.track
    @functools.cache
    @staticmethod
    def cached_stock_buy_sell(i, have_stock):
        if i < 0:
            return
        Function.cached_stock_buy_sell(i=i - 1, have_stock=True)
        Function.cached_stock_buy_sell(i=i - 1, have_stock=False)

    @track.track
    @staticmethod
    def func8(i):
        if i <= 0:
            return
        Function.func8(i - 1)
        Function.func8(i - 1)

    @track.track
    @staticmethod
    def subsequence(l, r):
        if l <= 0 or r <= 0:
            return
        else:
            Function.subsequence(l=l, r=r - 1)
            Function.subsequence(l=l - 1, r=r)
            Function.subsequence(l=l - 1, r=r - 1)

    @track.track
    @functools.cache
    @staticmethod
    def cached_subsequence(l, r):
        if l <= 0 or r <= 0:
            return
        else:
            Function.cached_subsequence(l=l, r=r - 1)
            Function.cached_subsequence(l=l - 1, r=r)
            Function.cached_subsequence(l=l - 1, r=r - 1)

    @staticmethod
    def coin_change_problem_cached(coins, amount):
        mcoin = min(coins)

        @track.track
        @functools.cache
        def coin_change_problem_cached_impl(amount):
            nonlocal coins, mcoin

            if amount in coins:
                return

            if amount == 0:
                return

            for coin in coins:
                if (amount - coin) >= mcoin:
                    coin_change_problem_cached_impl(amount=amount - coin)

        coin_change_problem_cached_impl(amount=amount)

    @staticmethod
    def coin_change_problem(coins, amount):
        mcoin = min(coins)

        @track.track
        def coin_change_problem_impl(amount):
            nonlocal coins, mcoin

            if amount in coins:
                return

            if amount == 0:
                return

            for coin in coins:
                if (amount - coin) >= mcoin:
                    coin_change_problem_impl(amount=amount - coin)

        coin_change_problem_impl(amount=amount)

    @staticmethod
    def knapscak_0_1(wt, weights):

        @track.track
        def solve_knapscak_0_1(wt, i):
            nonlocal weights

            if (i - 1) >= 0:
                solve_knapscak_0_1(wt=wt, i=i - 1)
                if (wt - weights[i]) > 0:
                    solve_knapscak_0_1(wt=wt - weights[i], i=i - 1)

        solve_knapscak_0_1(wt=wt, i=len(weights) - 1)

    @track.track
    @staticmethod
    def test_n(n):
        if n <= 0:
            return
        for i in range(1, n + 1):
            Function.test_n(n=n - i)

    @track.track
    @functools.cache
    @staticmethod
    def test_n_cached(n, r):
        if n == 0:
            return
        # for i in range(1, n+1):
        #     Function.test_n_cached(n=n-i)
        # for i in range(1, 3):
        #     Function.test_n_cached(n=n-i)
        for i in r:
            if (n - i) > 0:
                Function.test_n_cached(n=n - i, r=range(r.start, r.stop, r.step))

    @track.track
    @staticmethod
    def apsp(i, j, r, n):
        if i == j:
            return
        if r == 0:
            return

        for _k in range(n):
            Function.apsp(i=i, j=_k, r=r - 1, n=n)

    @track.track
    @functools.cache
    @staticmethod
    def apsp_cached(i, j, r, n):
        if i == j:
            return
        if r == 0:
            return

        for _k in range(n):
            Function.apsp_cached(i=i, j=_k, r=r - 1, n=n)


def main():

    # n = int(input())

    # Function.rod_cutting_complex(n=n)
    # Function.rod_cutting_complex_cached(n=n)

    # Function.rod_cutting_uncached(n=n)
    # Function.rod_cutting_cached(n=n)

    # Function.matrix_chain_multiplication(i=0, j=n)
    # Function.matrix_chain_multiplication_cached(i=0, j=n)

    # Function.func4(i=1, j=n)
    # Function.cached_func4(i=1, j=n)

    # Function.fibonacci_uncached(n=n)
    # Function.fibonacci_cached(n=n)

    # Function.merge_sort(l=0, r=n)

    # Function.stock_buy_sell(i=n, have_stock=False)
    # Function.cached_stock_buy_sell(i=n, have_stock=False)

    # Function.func8(i=n)

    # Function.subsequence(l=n, r=n + (n // 2))
    # Function.cached_subsequence(l=n, r=n + (n // 2))

    # Function.coin_change_problem_cached(coins=[1, 3, 5], amount=n)
    # Function.coin_change_problem_cached(coins=[3, 7, 11], amount=n)

    # Function.coin_change_problem_cached(coins=[1, 2, 7], amount=n)

    # Function.coin_change_problem(coins=[1, 3, 5], amount=n)
    # Function.coin_change_problem(coins=[1, 2, 7], amount=n)

    # weights = sorted([random.randint(1, n - 1) for i in range(5)])
    # with open(file="weights.txt", mode="w") as fp:
    #     pprint.pprint(weights, stream=fp)
    # weights = [16, 21, 24, 53, 92]
    # Function.knapscak_0_1(wt=n, weights=weights)

    # Function.test_n_cached(n=n, r=range(1, n + 1, 1))
    # Function.test_n_cached(n=n, r=range(1, 3, 1))
    # Function.test_n_cached(n=n, r=range(2, 7, 2))
    # Function.test_n_cached(n=n, r=range(1, 6, 2))

    # apsp
    n = 7
    # for i in range(n):
    #     for j in range(n):
    #         if i != j:
    #             Function.apsp_cached(i=2, j=5, r=n - 1, n=n)

    Function.apsp_cached(i=2, j=5, r=n - 1, n=n)

#  python3 ./functions.py | python3 track/__init__.py analyze - output
if __name__ == "__main__":
    main()
