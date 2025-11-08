import track
import functools


@track.track
def fibonacci(n):
    if n <= 1:
        return n
    n_1 = fibonacci(n=n - 1)
    n_2 = fibonacci(n=n - 2)
    return n_1 + n_2


@track.track
@functools.cache
def cached_fibonacci(n):
    if n <= 1:
        return n
    n_1 = cached_fibonacci(n - 1)
    n_2 = cached_fibonacci(n - 2)
    return n_1 + n_2


if __name__ == "__main__":
    n = int(input())
    # fibonacci(n=n)
    # cached_fibonacci(n=n)
