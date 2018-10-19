from datetime import date, timedelta

import dask

from example.fruit import Apple, Orange
from example.fruit_valuation import FruitPVRM

if __name__ == '__main__':
    d1 = date.today() + timedelta(10)
    apple1 = Apple("a1", 3.2, d1, "U.S")
    apple2 = Apple("a2", 5.8, d1, "U.S")
    orange = Orange("o1", 23.5, d1)
    pvrm = FruitPVRM()
    fruits = [apple1, apple2, orange]
    pv1 = dask.delayed(pvrm.present_value)(apple1)
    pv1.visualize()
    r = dask.compute(pv1)
    print(r)
    #pvs = list(map(pvrm.present_value, fruits))
    #for (fruit, pv) in zip(fruits, pvs):
        #print(f"{fruit.name}'s pv = {pv.value}")
        #print(f"{fruit.name}'s pv = {pv.value.compute().compute()}")
