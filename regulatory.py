# regulatory.py

from Bio import SeqIO
import gffutils

def fetch_promoter(db: gffutils.FeatureDB, genome, gene_id: str, length: int = 2000):
    feat = db[gene_id]
    seq = genome[feat.seqid].seq
    start = max(feat.start - length, 0)
    prom = seq[start:feat.start-1]
    return prom.reverse_complement() if feat.strand == '-' else prom

def compute_regulatory_score(
    genes, orthos, 
    db_morango, genoma_morango, 
    db_tomate,  genoma_tomate
) -> float:
    """
    Para cada gene de morango e seus ortólogos em tomate, 
    compara %GC do promotor (2kb upstream) e devolve média [0..1].
    """
    scores = []
    for gene in genes:
        prom_mor = fetch_promoter(db_morango, genoma_morango, gene)
        for tomo_ids in orthos.get(gene, []):
            prom_tom = fetch_promoter(db_tomate, genoma_tomate, tomo_ids)
            gc_mor = 100 * (prom_mor.count('G') + prom_mor.count('C')) / len(prom_mor)
            gc_tom = 100 * (prom_tom.count('G') + prom_tom.count('C')) / len(prom_tom)
            diff = abs(gc_mor - gc_tom)
            # score 1 para diff=0, 0 para diff>=50
            scores.append(max(0.0, 1 - diff/50))
    return sum(scores)/len(scores) if scores else 0.0
