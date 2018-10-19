from datetime import date

import dask

from present_value import PresentValue
from priceable import Priceable
from valuation import ValuationModel


class PVRMManager:
    def pvrm_configuration(self):
        return PVRMConfiguration.default_pvrm_config()

    #@dask.delayed
    def valuation_model(self, priceable: Priceable) -> ValuationModel:
        pass

    #@dask.delayed
    def present_value(self, priceable: Priceable) -> PresentValue:
        vm = dask.delayed(self.valuation_model)(priceable)
        return dask.delayed(vm.present_value)()


class PVRMConfiguration:
    def __init__(self, pricing_date: date):
        self.pricing_date = pricing_date

    @staticmethod
    def default_pvrm_config():
        return PVRMConfiguration(date.today())
