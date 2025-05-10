# transcriptomics.py
import pandas as pd

def load_expression(path: str) -> pd.DataFrame:
    # TSV com colunas: gene_id, tissue, TPM
    df = pd.read_csv(path, sep='\t')
    return df

def compute_expression_score(orthos, expr_tomate):
    # extrai TPM médio dos ortólogos em fruto maduro
    values = []
    for straw_gene, tomato_genes in orthos.items():
        for tg in tomato_genes:
            subset = expr_tomate[(expr_tomate.gene_id==tg) &
                                 (expr_tomate.tissue=='fruit_ripe')]
            if not subset.empty:
                values.append(subset.TPM.mean())
    # normaliza e retorna score [0,1]
    if not values: return 0.0
    raw = sum(values)/len(values)
    return min(raw/100.0,1.0)  # assume TPM≤100

# regulatory.py
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqUtils import MeltingTemp
import gffutils

def fetch_promoter(db, genome, gene_id, length=2000):
    feat = db[gene_id]
    seq = genome[feat.seqid].seq
    if feat.strand=='-':
        return seq[feat.start-length:feat.start].reverse_complement()
    else:
        return seq[feat.start-length:feat.start]

def compute_regulatory_score(genes, orthos, db_mor, gen_mor, db_tom, gen_tom):
    # compara GC content, Tm, ou presença de motivos PFMs
    scores=[]
    for g in genes:
        p_mor = fetch_promoter(db_mor, gen_mor, g)
        for tg in orthos.get(g,[]):
            p_tom = fetch_promoter(db_tom, gen_tom, tg)
            # exemplo simples: similaridade de %GC
            gc_diff = abs(100*p_mor.count('G')/len(p_mor) - 100*p_tom.count('G')/len(p_tom))
            scores.append(max(0,1 - gc_diff/50))
    return sum(scores)/len(scores) if scores else 0.0

# metabolic.py
import cobra

def load_metabolic_model(path: str):
    return cobra.io.read_sbml_model(path)

def test_pathway_flux(model, pathway):
    # assume pathway['reactions'] lista de reaction IDs do COBRA model
    with model:
        for rxn_id in pathway.get('reactions',[]):
            if rxn_id in model.reactions:
                model.reactions.get_by_id(rxn_id).bounds = (0,1000)
        sol = model.optimize()
        return sol.status=='optimal' and sol.objective_value>1e-6
