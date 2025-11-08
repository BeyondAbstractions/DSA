import unittest
import types


class ScratchPad(unittest.TestCase):

    @staticmethod
    def gen():
        yield 0
        yield 1
        yield 2

    def test_yield(self):
        g = ScratchPad.gen()
        for i in range(3):
            self.assertEqual(next(g), i)
        self.assertRaises(StopIteration, lambda: next(g))

    def test_multi_yield(self):
        for i in range(3):
            g = ScratchPad.gen()
            for i in range(3):
                self.assertEqual(next(g), i)
            self.assertRaises(StopIteration, lambda: next(g))

    def test_dynamic_object_method_creation(self):
        class Container(object):
            pass

        c = Container()
        c.state = None

        def method(self):
            return self.state

        c.method = types.MethodType(method, c)
        self.assertEqual(c.method(), None)


def main():
    return unittest.main()


if __name__ == "__main__":
    main()
