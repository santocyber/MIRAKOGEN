# simula_enhanced.py

import pandas as pd
import logging
import time
from typing import List, Dict

import strawberry_pathways      # list_all()
import orthologue_map           # find_tomato_orthologues()
import transcriptomics          # load_expression, compute_expression_score()
import regulatory               # fetch_promoters, compute_regulatory_score()
import metabolic                # load_metabolic_model, test_pathway_flux()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
logger.addHandler(handler)

def simulate(db_morango, genoma_morango, db_tomate, genoma_tomate) -> pd.DataFrame:
    """
    Para cada via de morango:
      1) Ortologia: mede quantos genes têm ortólogos em tomate.
      2) Transcriptômica: mede expressão média desses ortólogos em fruto de tomate.
      3) Regulação: compara motivos cis dos promotores (2kb upstream).
      4) Metabólica: injeta reações no modelo COBRApy e testa FBA.
      5) Combina scores em viabilidade geral.
    Retorna um DataFrame com todas essas métricas por via.
    """
    # --- 1. Carrega dados ômicos de expressão ---
    expr_tomate = transcriptomics.load_expression('data/tomato_expression.tsv')
    expr_morango = transcriptomics.load_expression('data/strawberry_expression.tsv')

    # --- 2. Carrega modelo metabólico de tomate em COBRApy ---
    model = metabolic.load_metabolic_model('models/tomato_sbml.xml')

    results: List[Dict] = []
    pathways = strawberry_pathways.list_all()

    for pw in pathways:
        pid    = pw['pathway_id']
        genes  = pw['genes']
        total  = len(genes)

        # Ortologia
        orthos = {g: orthologue_map.find_tomato_orthologues(g) for g in genes}
        matched = sum(1 for o in orthos.values() if o)
        ortho_score = matched / total

        # Transcriptômica
        expr_score = transcriptomics.compute_expression_score(orthos, expr_tomate)

        # Regulação cis/trans
        # extrai 2kb upstream do gene de tomate e do morango e compara motivos
        reg_score = regulatory.compute_regulatory_score(
            genes, orthos, db_morango, genoma_morango, db_tomate, genoma_tomate
        )

        # Metabólica
        flux_ok = metabolic.test_pathway_flux(model, pw)  # True/False
        meta_score = 1.0 if flux_ok else 0.0

        # Viabilidade composta (exemplo: média ponderada)
        viability = (ortho_score * 0.4 +
                     expr_score  * 0.3 +
                     reg_score   * 0.2 +
                     meta_score  * 0.1)

        results.append({
            'pathway_id':     pid,
            'total_genes':    total,
            'matched':        matched,
            'ortho_score':    round(ortho_score,3),
            'expr_score':     round(expr_score,3),
            'reg_score':      round(reg_score,3),
            'meta_score':     round(meta_score,1),
            'viability':      round(viability,3)
        })

        logger.info(f"{pid}: ortho={ortho_score:.2f} expr={expr_score:.2f} "
                    f"reg={reg_score:.2f} meta={meta_score:.1f} → viability={viability:.2f}")

    return pd.DataFrame(results)
