import unittest
import types


class ScratchPad(unittest.TestCase):

    @staticmethod
    def gen():
        yield 0
        yield 1
        yield 2

    @staticmethod
    def gen_2():
        yield 0
        return
        yield 1

    def test_gen_2(self):
        g = ScratchPad.gen_2()
        self.assertEqual(next(g), 0)
        self.assertRaises(StopIteration, next, g)

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


class Style(object):

    def __init__(self):
        pass

    def italics(self, fn):
        def wrapper():
            return "<i>" + fn() + "</i>"

        return wrapper

    def upper(self, fn):
        def wrapper():
            return fn().upper()

        return wrapper


style = Style()


@style.italics
@style.upper
def welcome():
    return "welcome"


class Style2(object):

    def __init__(self, fmt):
        self.fmt = fmt

    def __call__(self, fn):
        if self.fmt == "upper":

            def wrapper():
                return fn().upper()

            return wrapper
        elif self.fmt == "italics":

            def wrapper():
                return "<i>" + fn() + "</fi>"

            return wrapper


@Style2("upper")
@Style2("italics")
def welcome2():
    return "welcome"


def main():
    # return unittest.main()
    # w = welcome()
    # print(w)
    w = welcome2()
    print(w)


if __name__ == "__main__":
    main()
