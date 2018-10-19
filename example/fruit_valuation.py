from datetime import date
from typing import Dict, Tuple

from example.fruit import Fruit, FruitPayoffModel
from example.fruit_market import FruitMarketState, FruitObservationRepo
from example.fruit_model import FruitCalibratedMarketModel, FruitMarketModel, CurveMarketModelConfiguration
from present_value import PresentValue
from priceable import Priceable
# from pvrm import PVRMManager
from pvrm import PVRMManager
from valuation import PricingAlgorithm, ValuationModel


class FruitPricingAlgorithm(PricingAlgorithm):
    def present_value(self, payoff: Fruit, cmm: FruitCalibratedMarketModel) -> PresentValue:
        all_marks = cmm.market_prices()
        instrument = payoff.instrument()
        key = instrument.key()
        print(f"key={key}, all_marks={all_marks}")
        unit_price = all_marks.get(key)
        discount_curve = cmm.discount_curve()
        if unit_price is not None:
            value = unit_price * payoff.weight * discount_curve.discount_factor(payoff.delivery_date)
            return PresentValue(value, "CNY")
        else:
            raise RuntimeError(f"pricing failure due to missing market instrument ${instrument.product}")


class FruitValuationModel(ValuationModel):
    def __init__(self, priceable: Priceable, valuation_date: date):
        self.priceable = priceable
        self.valuation_date = valuation_date

    def market_model(self) -> FruitMarketModel:
        curve_config = CurveMarketModelConfiguration(self.valuation_date)
        return FruitMarketModel(curve_config)

    def market_state(self) -> FruitMarketState:
        return FruitMarketState("fruit", FruitObservationRepo)

    def payoff_model(self) -> FruitPayoffModel:
        return FruitPayoffModel()

    def payoff_parameter(self) -> Fruit:
        return self.priceable

    def pricing_algorithm(self) -> PricingAlgorithm:
        return FruitPricingAlgorithm()


class FruitPVRM(PVRMManager):
    def valuation_model(self, priceable):
        return FruitValuationModel(priceable, date.today())
