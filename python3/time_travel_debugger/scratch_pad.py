import bdb
from types import FrameType


# Define a simple function to debug
def demo(n):
    total = 0
    for i in range(n):
        total += i * i
    return total


def raise_exception():
    raise Exception("Dummy!")


def callee():
    pass


def caller():
    callee()


# Minimal subclass of Bdb (required because Bdb is abstract)
class MyDebugger(bdb.Bdb):
    def user_line(self, frame: FrameType):
        # Called on every line event
        bdb.Bdb.user_line(self, frame=frame)
        print(
            f"Line: {frame.f_code.co_filename}:{frame.f_code.co_name}:{frame.f_lineno}"
        )
        # self.set_continue()

        # self.set_break()
        # Just continue execution without interaction
        # self.set_step()

    def user_call(self, frame, arglist):
        print(f"Call: {frame.f_code.co_name}")

    def user_return(self, frame, return_value):
        print(f"Return: {frame.f_code.co_name} -> {return_value}")

    def user_exception(self, frame, exc_info):
        print(f"Exception: {exc_info[0].__name__}: {exc_info[1]}")


def main():
    dbg = MyDebugger()
    # dbg.runcall(demo, 5)
    # dbg.runcall(raise_exception)
    dbg.runcall(caller)


if __name__ == "__main__":
    main()
