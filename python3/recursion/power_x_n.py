import unittest
import track


class Solution:

    @track.track
    def pow(self, x, n):
        if n == 0:
            return 1

        if n % 2 == 0:
            val = self.pow(x=x, n=n / 2)
            return val**2
        else:
            val = self.pow(x=x, n=(n - 1) / 2)
            return x * (val**2)

    def __repr__(self):
        return "self=self"


class Test(unittest.TestCase):

    def test_2_pow_0(self):
        s = Solution()
        self.assertEqual(s.pow(2, 0), 1)

    def test_2_pow_1(self):
        s = Solution()
        self.assertEqual(s.pow(2, 1), 2)

    def test_2_pow_odd(self):
        s = Solution()
        self.assertEqual(s.pow(2, 9), 512)

    def test_2_pow_even(self):
        s = Solution()
        self.assertEqual(s.pow(2, 10), 1024)


def unittest_main():
    unittest.main()


def main():
    s = Solution()
    s.pow(x=2, n=10)


if __name__ == "__main__":
    main()
