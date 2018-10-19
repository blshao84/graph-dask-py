from datetime import date

from example.fruit_market import ListedFruitInstrument, FruitInstrumentRepo
from payoff import PayoffParameter, Payoff, PayoffModel
from priceable import Priceable


class Fruit(Payoff, PayoffParameter):
    def __init__(self, name: str, weight: float, delivery_date: date):
        self.name = name
        self.weight = weight
        self.delivery_date = delivery_date

    def instrument(self) -> ListedFruitInstrument:
        pass


class Apple(Fruit, Priceable):
    def __init__(self, name: str, weight: float, delivery_date: date, country: str):
        Fruit.__init__(self, name, weight, delivery_date)
        self.country = country
        self.pvrm_key = "FruitModel"

    def instrument(self):
        filtered = list(filter(lambda i: i.product == "Apple", FruitInstrumentRepo))
        print(f"find instrument {filtered}")
        return filtered[0]


class Orange(Fruit, Priceable):
    def __init__(self, name: str, weight: float, delivery_date: date):
        Fruit.__init__(self, name, weight, delivery_date)
        self.pvrm_key = "FruitModel"

    def instrument(self):
        filtered = list(filter(lambda i: i.product == "Orange", FruitInstrumentRepo))
        print(f"find instrument {filtered}")
        return filtered[0]


class FruitPayoffModel(PayoffModel):
    def payoff(self, fruit: Fruit) -> Fruit:
        return fruit
