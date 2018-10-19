from datetime import date
from typing import Dict, Tuple

from example.fruit_market import FruitMarketState, ListedFruitInstrument
from market_model import CalibratedMarketModel, MarketState, MarketModel, MarketModelConfiguration
from measure import MeasureMap
from priceable import Priceable


class CurveMarketState(MarketState):
    def __init__(self, name: str):
        self.name = name

    def observations(self):
        return []


class CurveMarketModelConfiguration(MarketModelConfiguration):
    def __init__(self, curve_starting_date: date):
        self.curve_starting_date = curve_starting_date


class CurveMarketModel(MarketModel):
    def __init__(self, config: CurveMarketModelConfiguration):
        self.config = config

    def market_model_configuration(self) -> MarketModelConfiguration:
        return self.config

    def calibrate(self, market_state: CurveMarketState) -> CalibratedMarketModel:
        return DiscountCurveCalibratedMarketModel(market_state, self.config.curve_starting_date)


class DiscountCurveCalibratedMarketModel(CalibratedMarketModel):
    def __init__(self, curve_market: CurveMarketState, curve_starting_date: date):
        self.curve_market = curve_market
        self.curve_starting_date = curve_starting_date

    def market_state(self) -> MarketState:
        return self.curve_market

    def measure_map(self, priceable: Priceable) -> MeasureMap:
        return MeasureMap.empty()

    def discount_factor(self, discount_date: date):
        days = (discount_date - self.curve_starting_date).days
        if days <= 0:
            return 1.0
        else:
            return 1 / days


class FruitCalibratedMarketModel(CalibratedMarketModel):
    def __init__(self, curve_model: DiscountCurveCalibratedMarketModel, fruit_market: FruitMarketState):
        self.curve_model = curve_model
        self.fruit_market = fruit_market

    def market_state(self) -> FruitMarketState:
        return self.fruit_market

    def measure_map(self, priceable: Priceable) -> MeasureMap:
        return MeasureMap.empty()

    def discount_curve(self) -> DiscountCurveCalibratedMarketModel:
        return self.curve_model

    def market_prices(self) -> Dict[Tuple[str,str], float]:
        ms = self.market_state()
        obs = ms.observations()
        return dict(map(lambda o: (o.observable.instrument.key(), o.value), obs))


class FruitMarketModel(MarketModel):
    def __init__(self, curve_config: CurveMarketModelConfiguration):
        self.curve_config = curve_config

    def market_model_configuration(self) -> CurveMarketModelConfiguration:
        return self.curve_config

    def calibrate(self, market_state: FruitMarketState) -> FruitCalibratedMarketModel:
        curve_cmm = self.calibrate_curve()
        return FruitCalibratedMarketModel(curve_cmm, market_state)

    def calibrate_curve(self):
        curve_model = CurveMarketModel(self.curve_config)
        curve_market = CurveMarketState("stupid discount curve")
        curve_cmm = curve_model.calibrate(curve_market)
        return curve_cmm