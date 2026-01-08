import datetime

from config.configuration import Configuration
from dto.csv_model import DonationModelCSVComplete
from dto.response_model import Incentivador, Donation, Project


class DataFilter:
    def __init__(self, config: Configuration):
        self.config = config

    def filter_incentivadores(self, incentivadores: list[Incentivador]) -> list[Incentivador]:
        return list(filter(self._incentivadores_filter_criteria, incentivadores))

    def _incentivadores_filter_criteria(self, incentivador: Incentivador) -> bool:
        return (
                incentivador.tipo_pessoa == "juridica"
                and self.config.getfloat("FILTERS", "max_donation") >= incentivador.total_doado >= self.config.getfloat("FILTERS", "min_donation")
        )

    def filter_donations(self, donations: list[Donation]) -> list[Donation]:
        return list(filter(self._donation_filter_criteria, donations))

    def _donation_filter_criteria(self, donation: Donation) -> bool:
        return (
                self.config.getfloat("FILTERS", "min_donation") <= donation.valor <= self.config.getfloat("FILTERS", "max_donation")
                and datetime.date.fromisoformat(self.config.get("FILTERS", "from_date")) <= donation.data_recibo <= datetime.date.fromisoformat(self.config.get("FILTERS", "until_date"))
        )

    def filter_projects(self, projects: list[Project]) -> list[Project]:
        return list(filter(self._project_filter_criteria, projects))

    def _project_filter_criteria(self, projeto: Project) -> bool:
        return (
                self.config.getfloat("FILTERS", "min_donation") <= projeto.valor_captado <= self.config.getfloat("FILTERS","max_donation")
        )

    def filter_donations_complete(self, donations: list[DonationModelCSVComplete]) -> list[DonationModelCSVComplete]:
        return list(filter(self._donation_complete_filter_criteria, donations))

    def _donation_complete_filter_criteria(self, donation: DonationModelCSVComplete) -> bool:
        return (
            True
        )