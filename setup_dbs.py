#!/usr/bin/env python3
import os
import logging
import gffutils
from Bio import SeqIO

# Configuração de logging simples
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

# Caminhos para os arquivos baixados
GFF_MORANGO   = 'public_data/Camarosa_v1.0a1_genes.gff.gz'
FASTA_MORANGO = 'public_data/Camarosa_v1.0a1_unmasked.fa.gz'
GFF_TOMATE    = 'public_data/Solanum_lycopersicum/gtf/Solanum_lycopersicum.SL3.0.61.gtf.gz'
FASTA_TOMATE  = 'public_data/Solanum_lycopersicum/dna/Solanum_lycopersicum.SL3.0.dna.toplevel.fa.gz'

def create_db(gtf_path: str, db_name: str):
    """Cria um banco gffutils a partir de GFF/GTF usando flags para acelerar importação."""
    if os.path.exists(db_name):
        logging.info(f"{db_name} já existe, removendo para recriar.")
        os.remove(db_name)
    logging.info(f"Criando {db_name} a partir de {gtf_path} ...")
    # disable_infer_* acelera ~100× quando GTF já possui genes/transcritos :contentReference[oaicite:0]{index=0}
    gffutils.create_db(
        gtf_path,
        dbfn=db_name,
        force=True,
        keep_order=True,
        disable_infer_genes=True,
        disable_infer_transcripts=True,
        merge_strategy='merge',
        sort_attribute_values=True
    )
    logging.info(f"{db_name} criado com sucesso.")

def verify_fasta(fasta_path: str):
    """Verifica carregamento rápido do FASTA (apenas contagem de seqs)."""
    logging.info(f"Lendo FASTA em {fasta_path} ...")
    seqs = list(SeqIO.parse(fasta_path, 'fasta'))
    logging.info(f"Encontradas {len(seqs)} sequências em {fasta_path}.")

if __name__ == "__main__":
    # Criação dos bancos
    create_db(GFF_MORANGO, 'morango.db')
    create_db(GFF_TOMATE,  'tomate.db')

    # Verificação de FASTA
    verify_fasta(FASTA_MORANGO)
    verify_fasta(FASTA_TOMATE)

    logging.info("Configuração inicial concluída. Execute scheduler.py sem recriar bancos.")

