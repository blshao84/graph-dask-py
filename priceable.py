from present_value import PresentValue
#from pvrm import PVRMManager


class Priceable:
    def __init__(self, pvrm_key):
        self.pvrm_key = pvrm_key

    # def pvrm_manager(self):
    #     return PVRMManager.pvrm(self)
    #
    # def valuation_model(self):
    #     pvrm = self.pvrm_manager(self)
    #     return pvrm.valuation_model(self)
    #
    # def present_value(self) -> PresentValue:
    #     vm = self.valuation_model(self)
    #     return vm.present_value()


