import datetime

from config.configuration import Configuration
from dto.response_model import Incentivador, Donation


class DataFilter:
    def __init__(self, config: Configuration):
        self.config = config

    @staticmethod
    def filter_incentivadores(incentivadores: list[Incentivador]) -> list[Incentivador]:
        return list(filter(lambda x: x.tipo_pessoa == "juridica", incentivadores))

    def filter_donations(self, donations: list[Donation]) -> list[Donation]:
        return list(filter(self._donation_filter_criteria, donations))

    def _donation_filter_criteria(self, donation: Donation) -> bool:
        return (
                self.config.getfloat("FILTERS", "min_donation") <= donation.valor <= self.config.getfloat("FILTERS", "max_donation")
                and datetime.date.fromisoformat(self.config.get("FILTERS", "from_date")) <= donation.data_recibo <= datetime.date.fromisoformat(self.config.get("FILTERS", "until_date"))
        )