#!/usr/bin/env python3
import time
import schedule
import logging
from Bio import SeqIO
import matplotlib.pyplot as plt
import pandas as pd
import gffutils
from simula_enhanced import simulate

print(">>> Scheduler Python iniciado", flush=True)

# Logging para arquivo e console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[logging.FileHandler('simulation.log'),
              logging.StreamHandler()]
)

# Caminhos aos bancos já criados
DB_MORANGO   = 'morango.db'
DB_TOMATE    = 'tomate.db'
FASTA_MORANGO= 'public_data/Camarosa_v1.0a1_unmasked.fa.gz'
FASTA_TOMATE = 'public_data/Solanum_lycopersicum/Solanum_lycopersicum.SL3.0.dna.toplevel.fa.gz'

# Conecta aos bancos existentes
print("–> Abrindo bancos gffutils...", flush=True)
db_morango = gffutils.FeatureDB(DB_MORANGO)
db_tomate  = gffutils.FeatureDB(DB_TOMATE)
print("   • morango.db e tomate.db carregados", flush=True)

# Carrega FASTAs em memória
print("–> Carregando FASTA do morango...", flush=True)
genoma_morango = SeqIO.to_dict(SeqIO.parse(FASTA_MORANGO, 'fasta'))
print(f"   • {len(genoma_morango)} seqs no morango", flush=True)

print("–> Carregando FASTA do tomate...", flush=True)
genoma_tomate  = SeqIO.to_dict(SeqIO.parse(FASTA_TOMATE, 'fasta'))
print(f"   • {len(genoma_tomate)} seqs no tomate", flush=True)

def executar_simulacao():
    ts = time.strftime('%Y%m%d_%H%M%S')
    logging.info(f"=== Starting simulation at {ts} ===")
    print(f"\n=== Início da simulação: {ts} ===", flush=True)

    df = simulate(db_morango, genoma_morango, db_tomate, genoma_tomate)

    logging.info(f"Simulation tested {len(df)} pathways")
    print(f"Simulação testou {len(df)} vias — salvando CSV...", flush=True)

    csv_file = f'resultados_{ts}.csv'
    df.to_csv(csv_file, index=False)
    print(f"   • CSV salvo: {csv_file}", flush=True)
    logging.info(f"Results saved to {csv_file}")

    for metric in ['activation_score', 'pathway_match']:
        plt.figure()
        df[metric].hist()
        plt.title(f'{metric} – {ts}')
        plt.xlabel(metric); plt.ylabel('Frequency')
        png = f'{metric}_{ts}.png'
        plt.savefig(png); plt.close()
        print(f"   • Plot salvo: {png}", flush=True)
        logging.info(f"Saved plot {png}")

    print(f"=== Fim da simulação: {ts} ===\n", flush=True)
    logging.info(f"=== Finished simulation at {ts} ===")

# Executa agora e agenda a cada hora
executar_simulacao()
schedule.every().hour.do(executar_simulacao)
print("Scheduler agendado para rodar a cada hora. Ctrl+C para sair.", flush=True)
logging.info("Scheduler iniciado.")

while True:
    schedule.run_pending()
    time.sleep(1)
