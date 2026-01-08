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


class DonationModelCSVComplete(BaseModel):
    incentivador: Optional[str] = Field(default="", alias="Incentivador")
    municipio_incent: Optional[str] = Field(default="", alias="Município (Incent)")
    uf_incent: Optional[str] = Field(default="", alias="UF (Incent)")
    responsavel: Optional[str] = Field(default="", alias="Responsável")
    cnpj: Optional[str] = Field(default="", alias="CNPJ")
    pronac: Optional[str] = Field(default="", alias="PRONAC")
    valor_doacao: Optional[float] = Field(default=0, alias="Valor da doação (R$)")
    nome_projeto: Optional[str] = Field(default="", alias="Nome do projeto")
    municipio_proj: Optional[str] = Field(default="", alias="Município (Projeto)")
    municipio_uf: Optional[str] = Field(default="", alias="UF (Projeto)")
    mecanismo: Optional[str] = Field(default="", alias="Mecanismo")
    resumo: Optional[str] = Field(default="", alias="Resumo")
    tipologia: Optional[str] = Field(default="", alias="Tipologia")
    segmento: Optional[str] = Field(default="", alias="Segmento")
    data_inicio: Optional[datetime.date] = Field(alias="Data de Início do Projeto")
    data_termino: Optional[datetime.date] = Field(alias="Data de Término do Projeto")
    proponente: Optional[str] = Field(default="", alias="Proponente")
    valor_solicitado: Optional[float] = Field(default=0, alias="Valor solicitado (R$)")
    valor_aprovado: Optional[float] = Field(default=0, alias="Valor aprovado (R$)")
    valor_projeto: Optional[float] = Field(default=0, alias="Valor do projeto (R$)")
    valor_captado: Optional[float] = Field(default=0, alias="Valor captado (R$)")
    valor_proposta: Optional[float] = Field(default=0, alias="Valor da proposta (R$)")

