#!/bin/bash

# Ativar o ambiente Conda
source /home/ubuntu/miniconda3/bin/activate ncbi_datasets_env

# Diretório base para os downloads
BASE_DOWNLOAD_DIR="/home/ubuntu/genomic_data"
mkdir -p "${BASE_DOWNLOAD_DIR}"

# Accessions e nomes de arquivo
FRAGARIA_ACCESSION="GCF_034382235.1"
FRAGARIA_FILENAME="fragaria_x_ananassa_${FRAGARIA_ACCESSION}"
FRAGARIA_ZIP="${FRAGARIA_FILENAME}.zip"
FRAGARIA_DIR="${BASE_DOWNLOAD_DIR}/${FRAGARIA_FILENAME}"

SOLANUM_ACCESSION="GCF_000188115.5"
SOLANUM_FILENAME="solanum_lycopersicum_${SOLANUM_ACCESSION}"
SOLANUM_ZIP="${SOLANUM_FILENAME}.zip"
SOLANUM_DIR="${BASE_DOWNLOAD_DIR}/${SOLANUM_FILENAME}"

echo "Iniciando download dos dados genômicos..."

# Download para Morango (Fragaria x ananassa)
echo "Baixando dados para Fragaria x ananassa (${FRAGARIA_ACCESSION})..."
datasets download genome accession "${FRAGARIA_ACCESSION}" --include genome,gff3,rna,protein --filename "${BASE_DOWNLOAD_DIR}/${FRAGARIA_ZIP}"
if [ -f "${BASE_DOWNLOAD_DIR}/${FRAGARIA_ZIP}" ]; then
    echo "Download de ${FRAGARIA_ZIP} concluído. Descompactando..."
    unzip -q "${BASE_DOWNLOAD_DIR}/${FRAGARIA_ZIP}" -d "${FRAGARIA_DIR}"
    if [ -d "${FRAGARIA_DIR}/ncbi_dataset" ]; then
        echo "Descompactação concluída. Verificando integridade dos arquivos..."
        cd "${FRAGARIA_DIR}"
        if md5sum -c md5sum.txt; then
            echo "Verificação de integridade para ${FRAGARIA_FILENAME} bem-sucedida."
        else
            echo "ERRO: Verificação de integridade para ${FRAGARIA_FILENAME} falhou."
        fi
        cd "/home/ubuntu"
    else
        echo "ERRO: Diretório ncbi_dataset não encontrado após descompactar ${FRAGARIA_ZIP}."
    fi
    # rm "${BASE_DOWNLOAD_DIR}/${FRAGARIA_ZIP}" # Opcional: remover o zip após descompactar
else
    echo "ERRO: Download de ${FRAGARIA_ZIP} falhou."
fi

echo "--------------------------------------------------"

# Download para Tomateiro (Solanum lycopersicum)
echo "Baixando dados para Solanum lycopersicum (${SOLANUM_ACCESSION})..."
datasets download genome accession "${SOLANUM_ACCESSION}" --include genome,gff3,rna,protein --filename "${BASE_DOWNLOAD_DIR}/${SOLANUM_ZIP}"
if [ -f "${BASE_DOWNLOAD_DIR}/${SOLANUM_ZIP}" ]; then
    echo "Download de ${SOLANUM_ZIP} concluído. Descompactando..."
    unzip -q "${BASE_DOWNLOAD_DIR}/${SOLANUM_ZIP}" -d "${SOLANUM_DIR}"
    if [ -d "${SOLANUM_DIR}/ncbi_dataset" ]; then
        echo "Descompactação concluída. Verificando integridade dos arquivos..."
        cd "${SOLANUM_DIR}"
        if md5sum -c md5sum.txt; then
            echo "Verificação de integridade para ${SOLANUM_FILENAME} bem-sucedida."
        else
            echo "ERRO: Verificação de integridade para ${SOLANUM_FILENAME} falhou."
        fi
        cd "/home/ubuntu"
    else
        echo "ERRO: Diretório ncbi_dataset não encontrado após descompactar ${SOLANUM_ZIP}."
    fi
    # rm "${BASE_DOWNLOAD_DIR}/${SOLANUM_ZIP}" # Opcional: remover o zip após descompactar
else
    echo "ERRO: Download de ${SOLANUM_ZIP} falhou."
fi

echo "--------------------------------------------------"
echo "Processo de download de dados genômicos concluído."

# Desativar o ambiente Conda (opcional, dependendo do fluxo de trabalho)
# conda deactivate

