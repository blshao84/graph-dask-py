class Payoff:
    pass


class PayoffParameter:
    pass


class PayoffModel:
    def payoff(self, param: PayoffParameter) -> Payoff:
        pass
