import concurrent.futures
import logging
from itertools import chain

from config.configuration import Configuration
from csv_writer.csv_writer import write_objects_to_csv
from dto.csv_model import DonationModelCSVComplete
from dto.response_model import Project
from filters.data_filter import DataFilter
from http_requests.custom_requests import VERSALICRequests

logger = logging.getLogger(__name__)


class DonationToCityCSV():
    def __init__(self, config: Configuration):
        self.config = config
        self.data_filter = DataFilter(config)
        self.versalic = VERSALICRequests(config)

    def generate_donation_csv(self):
        logger.info('Gerando o CSV de doações para uma determinada cidade')
        logger.info('Baixando a lista de Projetos...')
        projetos = self.versalic.get_list_of_projects()
        total_projetos_nofilt = len(projetos)
        logger.info('Filtrando a lista de Projetos')
        projetos = self.data_filter.filter_projects(projetos)
        logger.info(f'Total: {len(projetos)} de {total_projetos_nofilt} após filtro\n')

        logger.info('Baixando a lista de doações para os projetos...')
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            donations = executor.map(self._gen_csv_entries_with_donations, projetos)

        donations = list(chain.from_iterable(donations))
        donations = list(filter(lambda x: type(x) != str, donations))
        logger.info(f'Total: {len(donations)} doações\n')

        write_objects_to_csv(donations, [
            "Incentivador",
            "Município (Incent)",
            "UF (Incent)",
            "Responsável",
            "CNPJ",
            "PRONAC",
            "Valor da doação (R$)",
            "Nome do projeto",
            "Município (Projeto)",
            "UF (Projeto)",
            "Mecanismo",
            "Resumo",
            "Tipologia",
            "Segmento",
            "Data de Início do Projeto",
            "Data de Término do Projeto",
            "Proponente",
            "Valor solicitado (R$)",
            "Valor aprovado (R$)",
            "Valor do projeto (R$)",
            "Valor captado (R$)",
            "Valor da proposta (R$)"
        ], output="doacoes_para_cidade.csv")

    def _gen_csv_entries_with_donations(self, projeto: Project) -> list[DonationModelCSVComplete]:
        donations = []
        pronac = projeto.pronac
        incentivadores = self.versalic.get_list_of_incentivadores(pronac)
        incentivadores = self.data_filter.filter_incentivadores(incentivadores)
        for incentivador in incentivadores:
            cnpj_formatted = f"{incentivador.cgccpf[:2]}.{incentivador.cgccpf[2:5]}.{incentivador.cgccpf[5:8]}/{incentivador.cgccpf[8:12]}-{incentivador.cgccpf[12:]}"
            donations.append(DonationModelCSVComplete(
                **{
                    "Incentivador": incentivador.nome,
                    "Município (Incent)": incentivador.municipio,
                    "UF (Incent)": incentivador.uf,
                    "Responsável": incentivador.responsavel,
                    "CNPJ": cnpj_formatted,
                    "PRONAC": projeto.pronac,
                    "Valor da doação (R$)": incentivador.total_doado,
                    "Nome do projeto": projeto.nome,
                    "Município (Projeto)": projeto.municipio,
                    "UF (Projeto)": projeto.uf,
                    "Mecanismo": projeto.mecanismo,
                    "Resumo": projeto.resumo,
                    "Tipologia": projeto.tipologia,
                    "Segmento": projeto.segmento,
                    "Data de Início do Projeto": projeto.data_inicio,
                    "Data de Término do Projeto": projeto.data_termino,
                    "Proponente": projeto.proponente,
                    "Valor solicitado (R$)": projeto.valor_solicitado,
                    "Valor aprovado (R$)": projeto.valor_aprovado,
                    "Valor do projeto (R$)": projeto.valor_projeto,
                    "Valor captado (R$)": projeto.valor_captado,
                    "Valor da proposta (R$)": projeto.valor_proposta,
                }
            ))
        return donations
