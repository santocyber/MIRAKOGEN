# orthologue_map.py

import logging
from typing import List

# Tentar usar requests-cache para desempenho e cache automático
try:
    import requests_cache
    # Configura cache SQLite em disco por 24h
    requests_cache.install_cache('ensembl_cache', expire_after=86400)  # 24h :contentReference[oaicite:6]{index=6}
    from requests_cache import CachedSession as Session
    logging.info("Usando requests-cache para cache de REST API")
except ModuleNotFoundError:
    import requests
    from cachecontrol import CacheControlAdapter
    from requests.adapters import HTTPAdapter
    # Fallback: usar CacheControl ou requests simples
    session = requests.Session()
    try:
        # tenta adicionar CacheControl
        cc_adapter = CacheControlAdapter()
        session.mount('http://', cc_adapter)
        session.mount('https://', cc_adapter)
        logging.info("requests-cache não disponível, usando CacheControl para cache básico")  # :contentReference[oaicite:7]{index=7}
    except Exception:
        logging.warning("CacheControl não disponível; usando requests sem cache")
    Session = lambda *args, **kwargs: session

import requests
ENSEMBL_REST = "https://rest.ensembl.org"

def find_tomato_orthologues(
    straw_gene_id: str,
    target_species: str = "solanum_lycopersicum"
) -> List[str]:
    """
    Consulta o Ensembl Plants REST para ortólogos de um gene de morango.
    Retorna lista de IDs de tomate ou [] se não houver.
    """
    url = f"{ENSEMBL_REST}/homology/id/{straw_gene_id}"
    params = {
        "format": "condensed",
        "target_species": target_species,
        "type": "orthologues"
    }
    headers = {"Content-Type": "application/json"}
    sess = Session()
    try:
        resp = sess.get(url, params=params, headers=headers, timeout=10)  # usa cache se possível
        resp.raise_for_status()  # HTTP 200 check 
        data = resp.json().get("data", [])
        if not data:
            logging.debug(f"Sem homologias para {straw_gene_id}")
            return []
        homologies = data[0].get("homologies", [])
        orthos = [h['target']['id'] for h in homologies]
        logging.info(f"{straw_gene_id} → {len(orthos)} ortólogo(s): {orthos}")
        return orthos
    except Exception as e:
        logging.error(f"Falha na consulta REST para {straw_gene_id}: {e}")
        return []
