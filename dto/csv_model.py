import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DonationModelCSV(BaseModel):
    incentivador: Optional[str] = Field(default="", alias="Incentivador")
    municipio: Optional[str] = Field(default="", alias="Município")
    uf: Optional[str] = Field(default="", alias="UF")
    responsavel: Optional[str] = Field(default="", alias="Responsável")
    cnpj: Optional[str] = Field(default="", alias="CNPJ")
    pronac: Optional[str] = Field(default="", alias="PRONAC")
    valor_doacao: Optional[str] = Field(default="", alias="Valor da doação (R$)")
    data_doacao: Optional[datetime.date] = Field(default=None, alias="Data da doação")
    nome_projeto: Optional[str] = Field(default="", alias="Nome do projeto")