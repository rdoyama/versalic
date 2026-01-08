from urllib.parse import urlencode


def assemble_incentiv_url(base_url: str, city: str, state: str, limit: int, offset: int, pronac: str = None) -> str:
    base_url = base_url.strip() + "/api/v1/incentivadores"
    params = {
        "limit": limit,
        "offset": offset
    }
    if city:
        params['municipio'] = city
    if state:
        params['UF'] = state
    if pronac:
        params['PRONAC'] = pronac

    query_string = urlencode(params)
    return f"{base_url}?{query_string}"

def assemble_doacoes_url(base_url: str, limit: int = 100, offset: int = 0) -> str:
    base_url = base_url.strip()
    params = {
        "limit": limit,
        "offset": offset,
    }
    query_string = urlencode(params)
    return f"{base_url}?{query_string}"

def assemble_projects_url(base_url: str, city: str, state: str, limit: int = 100, offset: int = 0) -> str:
    base_url = base_url.strip() + "/api/v1/projetos"
    params = {
        "UF": state,
        "municipio": city,
        "limit": limit,
        "offset": offset,
        "sort": "valor_captado:desc"
    }
    query_string = urlencode(params)
    return f"{base_url}?{query_string}"