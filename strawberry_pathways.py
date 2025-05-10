# strawberry_pathways.py

import json
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

def list_all(json_path: str = "config/pathways.json") -> List[Dict]:
    """
    Lê vias metabólicas de morango definidas em JSON externo.
    Estrutura esperada do JSON:
    {
      "pathways": [
        { "id": "anthocyanin_synthesis", "genes": ["Gene1", "Gene2", ...] },
        ...
      ]
    }
    """
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)  # Leitura de JSON :contentReference[oaicite:0]{index=0}
        raw = data.get("pathways", [])
        valid = []
        for pw in raw:
            pid = pw.get("id")
            genes = pw.get("genes")
            if isinstance(pid, str) and isinstance(genes, list):
                valid.append({"pathway_id": pid, "genes": genes})
            else:
                logger.warning(f"Via malformada ignorada: {pw}")
        logger.info(f"Carregadas {len(valid)} vias de {json_path}")
        return valid
    except Exception as e:
        logger.error(f"Erro ao ler {json_path}: {e}")
        return []
