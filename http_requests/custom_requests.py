import logging
import random
import time
from typing import Any

import curl_cffi

from dto.response_model import Incentivadores, Incentivador, Donation, DonationsResponse, IncentivadoresResponse
from http_requests.url_assembler import assemble_incentiv_url, assemble_doacoes_url

logger = logging.getLogger(__name__)


INCENTIV_PER_PAGE = 50
DONATIONS_PER_PAGE = 100


class VERSALICRequests():
    def __init__(self, config: Any):
        self.base_url = config.get("URL", "base_url")
        self.city = config.get("FILTERS", "city")
        self.state = config.get("FILTERS", "state")

        self.session = curl_cffi.Session()

    def _get(self, url: str) -> dict:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0',
            'Accept': 'application/json, text/plain, */*',
        }
        time.sleep(random.random())
        logger.info(f"HTTP GET {url}")
        response = self.session.get(url, impersonate='firefox', headers=headers)
        if response.status_code != 200:
            logger.error(f'[GET {url}] failed: HTTP {response.status_code}')
            raise Exception(f'[GET {url}] failed: HTTP {response.status_code}')
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

    def get_list_of_incentivadores(self) -> list[Incentivador]:
        incentivadores_list = []
        total = 1
        offset = 0

        while offset < total:
            url = assemble_incentiv_url(self.base_url, self.city, self.state, INCENTIV_PER_PAGE, offset)
            incentivadores_json = self._get(url)
            incentivadores = IncentivadoresResponse(**incentivadores_json).data
            total = incentivadores.total
            offset += incentivadores.count
            incentivadores_list.extend(incentivadores.incentivadores)

        return incentivadores_list