import logging
import random
import time

import curl_cffi

from config.configuration import Configuration
from dto.response_model import Incentivador, Donation, DonationsResponse, IncentivadoresResponse, \
    Project, ProjectsResponse
from http_requests.url_assembler import assemble_incentiv_url, assemble_doacoes_url, assemble_projects_url

logger = logging.getLogger(__name__)


INCENTIV_PER_PAGE = 50
DONATIONS_PER_PAGE = 100
PROJECTS_PER_PAGE = 50


class VERSALICRequests():
    def __init__(self, config: Configuration):
        self.base_url = config.get("URL", "base_url")
        self.city = config.get("FILTERS", "city")
        self.state = config.get("FILTERS", "state").upper()
        self.min_value = config.getfloat("FILTERS", "min_donation")

        self.session = curl_cffi.Session()

    def _get(self, url: str) -> dict | bool:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0',
            'Accept': 'application/json, text/plain, */*',
        }
        time.sleep(random.random())
        logger.info(f"HTTP GET {url}")
        response = self.session.get(url, impersonate='firefox', headers=headers)
        if response.status_code != 200:
            err_msg = f'[GET {url}] failed: HTTP {response.status_code}'
            logger.error(err_msg)
            return False
        return response.json()

    def get_donations(self, base_url: str) -> list[Donation]:
        donations = []
        total = 1
        offset = 0
        while offset < total:
            url = assemble_doacoes_url(base_url, DONATIONS_PER_PAGE, offset)
            donations_response = DonationsResponse(**self._get(url))
            total = donations_response.total
            offset += donations_response.count
            donations.extend(donations_response.data.doacoes)
        return donations

    def get_list_of_incentivadores(self, pronac: str = None, restrict_location: bool = False) -> list[Incentivador]:
        incentivadores_list = []
        total = 1
        offset = 0

        while offset < total:
            if restrict_location:
                url = assemble_incentiv_url(self.base_url, self.city, self.state, INCENTIV_PER_PAGE, offset, pronac)
            else:
                url = assemble_incentiv_url(self.base_url, None, None, INCENTIV_PER_PAGE, offset, pronac)
            incentivadores_json = self._get(url)
            if not incentivadores_json:
                return incentivadores_list
            incentivadores = IncentivadoresResponse(**incentivadores_json)
            total = incentivadores.total
            offset += incentivadores.count
            incentivadores_list.extend(incentivadores.data.incentivadores)

        return incentivadores_list

    def get_list_of_projects(self) -> list[Project]:
        project_list = []
        total = 1
        offset = 0

        while offset < total:
            url = assemble_projects_url(self.base_url, self.city, self.state, PROJECTS_PER_PAGE, offset)
            projects_json = self._get(url)
            projects = ProjectsResponse(**projects_json)
            total = projects.total
            offset += projects.count
            project_list.extend(projects.data.projetos)

        return project_list