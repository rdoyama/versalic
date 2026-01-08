# Filtro avançado para coleta de dados da plataforma VERSALIC

## Instalação e Execução
1. Clone o repositório
```bash
$ git clone https://github.com/rdoyama/versalic
```

2. Edite os filtros no arquivo de configuração `config.ini`
 * `city` __(obrigatório)__: Cidade
 * `state` __(obrigatório)__: Estado (sigla)
 * `min_donation`: Valor mínimo das doações q serão selecionadas (R$ 0 por padrão)
 * `max_donation`: Valor máximo das doações q serão selecionadas (ilimitado por padrão)
 * `from_date`: Data mínima da doação (YYYY-MM-DD, 1970-01-01 por padrão)
 * `until_date`: Data máxima da doação (YYYY-MM-DD, data atual por padrão)

3. Instale os requisitos
```bash
$ pip install -r requirements.txt
```

4. Execute
```bash
$ python3 app.py
```

## Observações
* É gerado um arquivo `doacoes.csv` na pasta raiz do projeto contendo as seguintes colunas:
  * Incentivador
  * Município
  * UF
  * Responsável
  * CNPJ
  * PRONAC
  * Valor da doação (R$)
  * Data da doação
  * Nome do projeto
* Entre cada requisição é adicionado um tempo aleatório (entre 0 e 1 segundo) para evitar bloqueios no servidor (DDoS)
* Há projetos em outras cidades que são apoiados por empresas de Piracicaba (ex: a Caterpillar fez doações ao MASP), e estes projetos aparecerão na lista
* Não incluí detalhes dos projetos que aparecem na tabela para não causar maior lentidão na geração do arquivo
* É possível conseguir um subset dos incentivadores de um determinado projeto fazendo um groupby por projeto seguindo da seleção dos incentivadores com os dados da minha tabela.
