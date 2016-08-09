import unittest
from app.libs.typed import typechecked


@typechecked
def test_func(a: int, b: int) -> int:
    return a + b


@typechecked
def test_func2(a: int, b: int) -> int:
    return [a, b]


class Test(unittest.TestCase):
    def test(self):
        print(test_func(1, 10))
        try:
            print(test_func(10, '12'))
        except TypeError:
            pass

        try:
            print(test_func2(1, 20))
        except TypeError:
            pass


if __name__ == '__main__':
    unittest.main()
