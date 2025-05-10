#!/usr/bin/env python3
import os
import time
import schedule
import logging
import gffutils
from Bio import SeqIO
import matplotlib.pyplot as plt
import pandas as pd
from simula import simulate

print(">>> Scheduler Python iniciado", flush=True)

# ── Configuração de logging para arquivo e console ────────────────────────────
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('simulation.log'),
        logging.StreamHandler()      # envia também ao console
    ]
)

# ── Caminhos para arquivos baixados ────────────────────────────────────────────
GFF_MORANGO   = 'public_data/Camarosa_v1.0a1_genes.gff.gz'
FASTA_MORANGO = 'public_data/Camarosa_v1.0a1_unmasked.fa.gz'
GFF_TOMATE    = 'public_data/Solanum_lycopersicum/gtf/Solanum_lycopersicum.SL3.0.61.gtf.gz'
FASTA_TOMATE  = 'public_data/Solanum_lycopersicum/dna/Solanum_lycopersicum.SL3.0.dna.toplevel.fa.gz'

def prepare_dbs():
    """Remove DBs antigos e cria bancos de dados GFF/GTF limpos."""
    print("–> Removendo bancos antigos (se existirem)...", flush=True)
    for dbf in ('morango.db', 'tomate.db'):
        if os.path.exists(dbf):
            os.remove(dbf)
            logging.info(f"Removed stale DB: {dbf}")
            print(f"   * {dbf} removido", flush=True)

    print("–> Criando morango.db a partir de GFF_MORANGO...", flush=True)
    gffutils.create_db(
        GFF_MORANGO,
        dbfn='morango.db', force=True, keep_order=True,
        disable_infer_genes=True, disable_infer_transcripts=True,
        merge_strategy='merge', sort_attribute_values=True
    )
    logging.info("Created morango.db")

    print("–> Criando tomate.db a partir de GFF_TOMATE...", flush=True)
    gffutils.create_db(
        GFF_TOMATE,
        dbfn='tomate.db', force=True, keep_order=True,
        disable_infer_genes=True, disable_infer_transcripts=True,
        merge_strategy='merge', sort_attribute_values=True
    )
    logging.info("Created tomate.db")

    print("–> Bancos criados com sucesso", flush=True)

def load_data():
    """Carrega bancos de dados e FASTAs em memória."""
    print("–> Carregando bancos de dados em memória...", flush=True)
    db_morango = gffutils.FeatureDB('morango.db')
    db_tomate  = gffutils.FeatureDB('tomate.db')

    print("–> Lendo FASTA do morango...", flush=True)
    gen_mor = SeqIO.to_dict(SeqIO.parse(FASTA_MORANGO, 'fasta'))
    print(f"   • {len(gen_mor)} sequências carregadas de {FASTA_MORANGO}", flush=True)

    print("–> Lendo FASTA do tomate...", flush=True)
    gen_tom = SeqIO.to_dict(SeqIO.parse(FASTA_TOMATE, 'fasta'))
    print(f"   • {len(gen_tom)} sequências carregadas de {FASTA_TOMATE}", flush=True)

    return db_morango, gen_mor, db_tomate, gen_tom

# ── Preparação inicial ─────────────────────────────────────────────────────────
prepare_dbs()
db_morango, genoma_morango, db_tomate, genoma_tomate = load_data()

def executar_simulacao():
    """Executa a simulação, salva resultados, logs e gera gráficos."""
    ts = time.strftime('%Y%m%d_%H%M%S')
    print(f"\n=== Início da simulação: {ts} ===", flush=True)
    logging.info(f"=== Starting simulation at {ts} ===")

    df = simulate(db_morango, genoma_morango, db_tomate, genoma_tomate)

    logging.info(f"Simulation tested {len(df)} pathways")
    print(f"Simulação testou {len(df)} vias — salvando CSV...", flush=True)

    csv_file = f'resultados_{ts}.csv'
    df.to_csv(csv_file, index=False)
    logging.info(f"Results saved to {csv_file}")
    print(f"   • CSV salvo: {csv_file}", flush=True)

    for metric in ['activation_score', 'pathway_match']:
        plt.figure()
        df[metric].hist()
        plt.title(f'{metric} – {ts}')
        plt.xlabel(metric)
        plt.ylabel('Frequency')
        png = f'{metric}_{ts}.png'
        plt.savefig(png)
        plt.close()
        logging.info(f"Saved plot {png}")
        print(f"   • Plot salvo: {png}", flush=True)

    logging.info(f"=== Finished simulation at {ts} ===")
    print(f"=== Fim da simulação: {ts} ===\n", flush=True)

# ── Execução imediata e agendamento ─────────────────────────────────────────────
executar_simulacao()
schedule.every().hour.do(executar_simulacao)
print("Scheduler agendado para rodar a cada hora. Press Ctrl+C para sair.", flush=True)
logging.info("Scheduler iniciado.")

# ── Loop principal ───────────────────────────────────────────────────────────────
while True:
    schedule.run_pending()
    time.sleep(1)
