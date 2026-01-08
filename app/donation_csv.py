import logging

from config.configuration import Configuration
from csv_writer.csv_writer import write_objects_to_csv
from dto.csv_model import DonationModelCSV
from dto.response_model import Incentivador
from filters.data_filter import DataFilter
from http_requests.custom_requests import VERSALICRequests

logger = logging.getLogger(__name__)

class DonationCSV:
    def __init__(self, config: Configuration):
        self.config = config
        self.data_filter = DataFilter(config)
        self.versalic = VERSALICRequests(config)

    def generate_donation_csv(self):
        logger.info('Gerando o CSV de doações')
        logger.info('Baixando a lista de Incentivadores...')
        incentivadores = self.versalic.get_list_of_incentivadores()
        logger.info('Filtrando a lista de Incentivadores')
        incentivadores = self.data_filter.filter_incentivadores(incentivadores)
        logger.info(f'Total: {len(incentivadores)}')
        logger.info('Baixando a lista de doações para os incentivadores...\n')
        donations_to_csv = self.get_donations_from_incentivadores(incentivadores)
        write_objects_to_csv(donations_to_csv, [
            "Incentivador",
            "Município",
            "UF",
            "Responsável",
            "CNPJ",
            "PRONAC",
            "Valor da doação (R$)",
            "Data da doação",
            "Nome do projeto"
        ], output="doacoes.csv")

    def get_donations_from_incentivadores(self, incentivadores: list[Incentivador]) -> list[DonationModelCSV]:
        donations_to_csv = []
        total_incentivadores = len(incentivadores)
        for i, incentivador in enumerate(incentivadores):
            if incentivador.links.doacoes.strip():
                logger.info(f'[{i + 1}/{total_incentivadores}] Doações do incentivador {incentivador.nome}')
                donations = self.versalic.get_donations(incentivador.links.doacoes.strip())
                logger.info('Filtrando doações')
                donations = self.data_filter.filter_donations(donations)
                logger.info(f'Total de doações: {len(donations)}\n')
                for donation in donations:
                    cnpj_formatted = f"{incentivador.cgccpf[:2]}.{incentivador.cgccpf[2:5]}.{incentivador.cgccpf[5:8]}/{incentivador.cgccpf[8:12]}-{incentivador.cgccpf[12:]}"
                    donations_to_csv.append(DonationModelCSV(
                        **{
                            "Incentivador": incentivador.nome,
                            "Município": incentivador.municipio,
                            "UF": incentivador.uf,
                            "Responsável": incentivador.responsavel,
                            "CNPJ": cnpj_formatted,
                            "PRONAC": donation.pronac,
                            "Valor da doação (R$)": f"{donation.valor:.2f}",
                            "Data da doação": donation.data_recibo,
                            "Nome do projeto": donation.nome_projeto,
                        }
                    ))
        logger.info(f'Total de doações: {len(donations_to_csv)}')
        return donations_to_csv

