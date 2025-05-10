# simula.py

import pandas as pd
import logging
import time
from typing import List, Dict

import strawberry_pathways
import orthologue_map

# Configure logger to show DEBUG on console
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()  
ch.setLevel(logging.DEBUG)
ch.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
logger.addHandler(ch)

def simulate(
    db_morango, genoma_morango,
    db_tomate, genoma_tomate
) -> pd.DataFrame:
    """
    Testa todas as vias de morango contra o genoma de tomate,
    e PAUSA quando encontrar cada via viável, mas NÃO interrompe
    o loop — continua até avaliar todas. Retorna DataFrame com
    todos os resultados.
    """
    results: List[Dict] = []
    all_pathways = strawberry_pathways.list_all()
    logger.info(f"Iniciando teste de {len(all_pathways)} vias metabólicas.")

    for idx, pw in enumerate(all_pathways, start=1):
        pid = pw['pathway_id']
        genes = pw['genes']
        total = len(genes)
        matched = 0

        logger.debug(f"[{idx}/{len(all_pathways)}] Testando via '{pid}' ({total} genes)...")

        for g in genes:
            orthos = orthologue_map.find_tomato_orthologues(g)
            if orthos:
                matched += 1
                logger.debug(f"  ✔ {g} → ortólogos: {orthos}")
            else:
                logger.debug(f"  ✘ {g} → sem ortólogo")

        score = matched / total if total else 0.0
        viable = (matched == total)

        # Imprime na tela o resultado resumido
        print(f"Via '{pid}': {matched}/{total} → score={score:.3f}{'  [VIÁVEL]' if viable else ''}")

        # Se for viável, pausa até o usuário pressionar Enter
        if viable:
            input(f"→ Via VIÁVEL encontrada: '{pid}'. Pressione Enter para continuar testes...")

        results.append({
            'pathway_id':       pid,
            'enzymes_total':    total,
            'enzymes_matched':  matched,
            'activation_score': round(score, 3),
            'viable':           viable
        })

    df = pd.DataFrame(results)
    logger.info("Teste concluído para todas as vias.")
    return df
