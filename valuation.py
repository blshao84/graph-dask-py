import dask

from market_model import MarketModel, MarketState, CalibratedMarketModel
from measure import MeasureMap
from payoff import Payoff, PayoffModel, PayoffParameter
from present_value import PresentValue
from priceable import Priceable


class PricingAlgorithm:
    def present_value(self, payoff: Payoff, cmm: CalibratedMarketModel) -> PresentValue:
        pass


class ValuationModel:
    def __init__(self, priceable: Priceable):
        self.priceable = priceable

    #@dask.delayed
    def market_model(self) -> MarketModel:
        pass

    #@dask.delayed
    def market_state(self) -> MarketState:
        pass

    #@dask.delayed
    def payoff_model(self) -> PayoffModel:
        pass

    #@dask.delayed
    def payoff_parameter(self) -> PayoffParameter:
        pass

    #@dask.delayed
    def pricing_algorithm(self) -> PricingAlgorithm:
        pass

    #@dask.delayed
    def payoff(self) -> Payoff:
        pm = dask.delayed(self.payoff_model)()
        pp = dask.delayed(self.payoff_parameter)()
        return dask.delayed(pm.payoff)(pp)

    #@dask.delayed
    def calibrated_market_model(self) -> CalibratedMarketModel:
        mm = dask.delayed(self.market_model)()
        ms = dask.delayed(self.market_state)()
        return dask.delayed(mm.calibrate)(ms)

    #@dask.delayed
    def present_value(self) -> PresentValue:
        po = dask.delayed(self.payoff)()
        cmm = dask.delayed(self.calibrated_market_model)()
        pa = dask.delayed(self.pricing_algorithm)()
        return dask.delayed(pa.present_value)(po, cmm)

    def measure_map(self) -> MeasureMap:
        cmm = self.calibrated_market_model()
        return cmm.measure_map(self.priceable)
