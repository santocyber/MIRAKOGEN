pip install biopython pandas gffutils schedule matplotlib 
pip install requests-cache
pip install cobra



# Cria diretórios locais
mkdir -p public_data/solanum_lycopersicum/{dna,gtf}

# Baixa os FASTA (genoma) do tomate SL3.0
rsync -Lav \
  rsync://ftp.ebi.ac.uk/ensemblgenomes/pub/plants/current/fasta/solanum_lycopersicum/dna/ \
  public_data/solanum_lycopersicum/dna/  \
  --include='*SL3.0.dna.toplevel.fa.gz' --exclude='*'

# Baixa os GTF (anotação ITAG3.0)
rsync -Lav \
  rsync://ftp.ebi.ac.uk/ensemblgenomes/pub/plants/current/gtf/solanum_lycopersicum/ \
  public_data/solanum_lycopersicum/gtf/ \
  --include='*SL3.0.*.gtf.gz' --exclude='*'




mkdir -p public_data/fragaria_x_ananassa

# FASTA hardmasked
wget \
  https://www.rosaceae.org/rosaceae_downloads/Fragaria_x_ananassa/Fragaria_x_ananassa_Camarosa_Genome_v1.0.a1/assembly/F_ana_Camarosa_6-28-17_hardmasked.fasta.gz \
  -O public_data/Camarosa_v1.0a1_hardmasked.fa.gz
# :contentReference[oaicite:1]{index=1}

# FASTA unmasked
wget \
  https://www.rosaceae.org/rosaceae_downloads/Fragaria_x_ananassa/Fragaria_x_ananassa_Camarosa_Genome_v1.0.a1/assembly/F_ana_Camarosa_6-28-17.fasta.gz \
  -O public_data/Camarosa_v1.0a1_unmasked.fa.gz
# :contentReference[oaicite:2]{index=2}



# Arquivo GFF3 de predições gênicas
wget \
  https://www.rosaceae.org/rosaceae_downloads/Fragaria_x_ananassa/Fragaria_x_ananassa_Camarosa_Genome_v1.0.a1/genes/Fxa_v1.2_makerStandard_MakerGenes_woTposases.gff.gz \
  -O public_data/Camarosa_v1.0a1_genes.gff.gz
# :contentReference[oaicite:3]{index=3}
