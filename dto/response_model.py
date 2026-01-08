from datetime import date
from typing import Optional

from pydantic import ConfigDict, Field
from pydantic.dataclasses import dataclass


@dataclass(config=ConfigDict(extra='ignore'))
class Links:
    itself: str = Field(alias='self')
    doacoes: str = ""


@dataclass(config=ConfigDict(extra='ignore'))
class LinksDonation:
    projeto: str = ""
    incentivador: str = ""


@dataclass(config=ConfigDict(extra='ignore'))
class Incentivador:
    uf: str = Field(alias='UF')
    links: Links = Field(alias='_links')
    nome: str = ""
    municipio: str = ""
    responsavel: str = ""
    total_doado: float = 0
    tipo_pessoa: str = ""
    cgccpf: str = ""


@dataclass(config=ConfigDict(extra='ignore'))
class Incentivadores:
    incentivadores: Optional[list[Incentivador]] = ()
    count: int = 0
    total: int = 0


@dataclass(config=ConfigDict(extra='ignore'))
class IncentivadoresResponse:
    data: Optional[Incentivadores] = Field(alias='_embedded')
    count: int = 0
    total: int = 0


@dataclass(config=ConfigDict(extra='ignore'))
class Donation:
    pronac: str = Field(alias='PRONAC')
    links: LinksDonation = Field(alias='_links')
    valor: float = 0
    data_recibo: date = None
    nome_projeto: str = ""
    cgccpf: str = ""
    nome_doador: str = ""


@dataclass(config=ConfigDict(extra='ignore'))
class Donations:
    doacoes: list[Donation] = ()


@dataclass(config=ConfigDict(extra='ignore'))
class DonationsResponse:
    data: Donations = Field(alias="_embedded")
    count: int = 0
    total: int = 0


@dataclass(config=ConfigDict(extra='ignore'))
class Project:
    pronac: str = Field(alias='PRONAC')
    mecanismo: str = Field(alias='mecanisnmo')
    uf: str = Field(alias='UF')
    nome: str = ""
    cgccpf: str = ""
    resumo: str = ""
    tipologia: str = ""
    municipio: str = ""
    segmento: str = ""
    data_inicio: date = None
    data_termino: date = None
    proponente: str = ""
    valor_solicitado: float = 0
    valor_aprovado: float = 0
    valor_projeto: float = 0
    valor_captado: float = 0
    valor_proposta: float = 0


@dataclass(config=ConfigDict(extra='ignore'))
class Projects:
    projetos: list[Project] = ()


@dataclass(config=ConfigDict(extra='ignore'))
class ProjectsResponse:
    data: Optional[Projects] = Field(alias='_embedded')
    count: int = 0
    total: int = 0