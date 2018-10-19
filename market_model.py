from typing import List

from measure import MeasureMap
from observation import Observation
from priceable import Priceable


class MarketState:
    def __init__(self, name: str):
        self.name = name

    def observations(self) -> List[Observation]:
        pass


class CalibratedMarketModel:
    def market_state(self) -> MarketState:
        pass

    def measure_map(self, priceable: Priceable) -> MeasureMap:
        pass


class MarketModelConfiguration:
    pass


class MarketModel:
    def market_model_configuration(self) -> MarketModelConfiguration:
        pass

    def calibrate(self, market_state: MarketState) -> CalibratedMarketModel:
        pass
