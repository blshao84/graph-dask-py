import dask.delayed


class Calc:
    def __init__(self, num: int):
        self.num = num

    def compute(self):
        return self.num * self.num


def inc(x):
    print(f"inc {x}")
    return Calc(x)


def double(x):
    return x + 2


def add(x, y):
    print(f"add {x} , {y}")
    s = x+y
    dx = dask.delayed(inc)(s)
    return dask.delayed(dx.compute)()


if __name__ == '__main__':

    x = dask.delayed(add)(1,2)
    print(x.compute().compute().compute())
    # data = [1]  # , 2, 3, 4, 5]
    #
    # output = []
    # for x in data:
    #     a = dask.delayed(inc)(x)
    #     b = dask.delayed(double)(x)
    #     c = dask.delayed(add)(a, b)
    #     output.append(c)
    #
    # total = dask.delayed(sum)(output)
    # print("computing ...")
    # print(total.compute().compute())
