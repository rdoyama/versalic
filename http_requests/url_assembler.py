from urllib.parse import urlencode


def assemble_incentiv_url(base_url: str, city: str, state: str, limit: int, offset: int) -> str:
    base_url = base_url.strip() + "/api/v1/incentivadores"
    params = {
        "limit": limit,
        "offset": offset,
        "municipio": city,
        "UF": state,
        "sort": "total_doado:desc"
    }
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