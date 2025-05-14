#!/bin/bash

# Script para validar os dados genômicos e transcriptômicos baixados
# de Morango (Fragaria x ananassa) e Tomateiro (Solanum lycopersicum)

# --- Configuração Geral ---
BASE_DIR="/home/ubuntu/genomic_data"
STRAWBERRY_DIR="${BASE_DIR}/fragaria_x_ananassa"
TOMATO_DIR="${BASE_DIR}/solanum_lycopersicum"
VALIDATION_LOG_FILE="${BASE_DIR}/validation_log.txt"
DOWNLOAD_LOG_FILE="${BASE_DIR}/download_log.txt"

# Limpar log de validação anterior, se existir
> "${VALIDATION_LOG_FILE}"

# Função para registrar mensagens no log de validação e no console
log_validation_message() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - VALIDATION - $1" | tee -a "${VALIDATION_LOG_FILE}"
}

log_validation_message "Início do script de validação de dados genômicos."

# --- Validação de Dados do Morango (Fragaria x ananassa) ---
log_validation_message "Iniciando validação dos dados do Morango (Fragaria x ananassa)."

EXPECTED_STRAWBERRY_FILES=(
    "F_ana_Camarosa_6-28-17_hardmasked.fasta.gz"
    "F_ana_Camarosa_6-28-17.fasta.gz"
    "Fxa_v1.2_makerStandard_MakerGenes_woTposases.gff.gz"
    "Fxa_v1.2_makerStandard_transcripts_woTposases.fasta.gz"
    "Fxa_v1.2_makerStandard_proteins_woTposases.fasta.gz"
    "F_ana_lincRNAs_masked_transcripts_removed.gtf.gz"
)

for file_name in "${EXPECTED_STRAWBERRY_FILES[@]}"; do
    file_path="${STRAWBERRY_DIR}/${file_name}"
    log_validation_message "Validando arquivo: ${file_path}"
    if [ -f "${file_path}" ]; then
        log_validation_message "EXISTE: ${file_name}"
        if [ -s "${file_path}" ]; then
            log_validation_message "NÃO VAZIO: ${file_name}"
            if [[ "${file_name}" == *.gz ]]; then
                if gzip -t "${file_path}" &> /dev/null; then
                    log_validation_message "INTEGRIDADE GZIP OK: ${file_name}"
                else
                    log_validation_message "ERRO DE INTEGRIDADE GZIP: ${file_name}"
                fi
            fi
        else
            log_validation_message "ERRO: ARQUIVO VAZIO: ${file_name}"
        fi
    else
        log_validation_message "ERRO: ARQUIVO NÃO ENCONTRADO: ${file_name}"
    fi
done

log_validation_message "Validação dos dados do Morango concluída."

# --- Validação de Dados do Tomateiro (Solanum lycopersicum) ---
log_validation_message "Iniciando validação dos dados do Tomateiro (Solanum lycopersicum)."

# Estes são os arquivos esperados se o download FTP foi bem-sucedido
EXPECTED_TOMATO_FILES=(
    "GCF_036512215.1_SLM_r2.1_genomic.fna.gz"
    "GCF_036512215.1_SLM_r2.1_genomic.gff.gz"
    "GCF_036512215.1_SLM_r2.1_rna.fna.gz"
    "GCF_036512215.1_SLM_r2.1_protein.faa.gz"
)

# Verificar se o download via NCBI Datasets foi sugerido/realizado
NCBI_DATASETS_ZIP_FILE="${TOMATO_DIR}/GCF_036512215.1.zip"

if [ -f "${NCBI_DATASETS_ZIP_FILE}" ]; then
    log_validation_message "Arquivo ZIP do NCBI Datasets encontrado: ${NCBI_DATASETS_ZIP_FILE}"
    log_validation_message "Validando arquivo ZIP: ${NCBI_DATASETS_ZIP_FILE}"
    if [ -s "${NCBI_DATASETS_ZIP_FILE}" ]; then
        log_validation_message "NÃO VAZIO: ${NCBI_DATASETS_ZIP_FILE}"
        # A validação de integridade de ZIP pode ser feita com 'unzip -t'
        if unzip -tqq "${NCBI_DATASETS_ZIP_FILE}" &> /dev/null; then
            log_validation_message "INTEGRIDADE ZIP OK: ${NCBI_DATASETS_ZIP_FILE}"
            log_validation_message "Conteúdo do ZIP (arquivos esperados dentro de ncbi_dataset/data/GCF_.../): genomic.fna, genomic.gff, rna.fna, protein.faa etc."
            log_validation_message "Descompacte e valide os arquivos individuais se necessário."
        else
            log_validation_message "ERRO DE INTEGRIDADE ZIP: ${NCBI_DATASETS_ZIP_FILE}"
        fi
    else
        log_validation_message "ERRO: ARQUIVO ZIP VAZIO: ${NCBI_DATASETS_ZIP_FILE}"
    fi
else
    log_validation_message "Arquivo ZIP do NCBI Datasets (${NCBI_DATASETS_ZIP_FILE}) não encontrado. Validando arquivos individuais baixados via FTP (se houver)."
    for file_name in "${EXPECTED_TOMATO_FILES[@]}"; do
        file_path="${TOMATO_DIR}/${file_name}"
        log_validation_message "Validando arquivo: ${file_path}"
        if [ -f "${file_path}" ]; then
            log_validation_message "EXISTE: ${file_name}"
            if [ -s "${file_path}" ]; then
                log_validation_message "NÃO VAZIO: ${file_name}"
                if [[ "${file_name}" == *.gz ]]; then
                    if gzip -t "${file_path}" &> /dev/null; then
                        log_validation_message "INTEGRIDADE GZIP OK: ${file_name}"
                    else
                        log_validation_message "ERRO DE INTEGRIDADE GZIP: ${file_name}"
                    fi
                fi
            else
                log_validation_message "ERRO: ARQUIVO VAZIO: ${file_name}"
            fi
        else
            log_validation_message "ERRO: ARQUIVO NÃO ENCONTRADO: ${file_name} (Verifique o log de download: ${DOWNLOAD_LOG_FILE})"
        fi
    done
fi

log_validation_message "Validação dos dados do Tomateiro concluída."

# --- Sumário da Validação ---
SUMMARY_FILE="${BASE_DIR}/data_validation_summary.md"

log_validation_message "Gerando sumário da validação em: ${SUMMARY_FILE}"

{ 
    echo "# Sumário da Validação dos Dados Genômicos Baixados"
    echo "Data da Validação: $(date)"
    echo ""
    echo "## Log de Download"
    echo "Consulte o arquivo: [download_log.txt](./download_log.txt) para detalhes do processo de download."
    echo ""
    echo "## Log de Validação"
    echo "Consulte o arquivo: [validation_log.txt](./validation_log.txt) para detalhes do processo de validação."
    echo ""
    echo "## Status dos Arquivos de Morango (Fragaria x ananassa)"
    echo "| Arquivo Esperado | Status | Detalhes |"
    echo "|---|---|---|"
} > "${SUMMARY_FILE}"

for file_name in "${EXPECTED_STRAWBERRY_FILES[@]}"; do
    file_path="${STRAWBERRY_DIR}/${file_name}"
    status="NÃO ENCONTRADO"
    details="-"
    if [ -f "${file_path}" ]; then
        status="ENCONTRADO"
        if [ -s "${file_path}" ]; then
            details="Não vazio."
            if [[ "${file_name}" == *.gz ]]; then
                if gzip -t "${file_path}" &> /dev/null; then
                    details+=" Integridade GZIP OK."
                else
                    status="ERRO"
                    details+=" Falha na integridade GZIP."
                fi
            fi
        else
            status="ERRO"
            details="Arquivo vazio."
        fi
    fi
    echo "| ${file_name} | ${status} | ${details} |" >> "${SUMMARY_FILE}"
done

echo "" >> "${SUMMARY_FILE}"
echo "## Status dos Arquivos de Tomateiro (Solanum lycopersicum)" >> "${SUMMARY_FILE}"

if [ -f "${NCBI_DATASETS_ZIP_FILE}" ]; then
    echo "Download realizado via NCBI Datasets CLI (arquivo ZIP)." >> "${SUMMARY_FILE}"
    echo "| Arquivo Esperado (ZIP) | Status | Detalhes |" >> "${SUMMARY_FILE}"
    echo "|---|---|---|" >> "${SUMMARY_FILE}"
    status="NÃO ENCONTRADO"
    details="-"
    if [ -f "${NCBI_DATASETS_ZIP_FILE}" ]; then
        status="ENCONTRADO"
        if [ -s "${NCBI_DATASETS_ZIP_FILE}" ]; then
            details="Não vazio."
            if unzip -tqq "${NCBI_DATASETS_ZIP_FILE}" &> /dev/null; then
                details+=" Integridade ZIP OK. Conteúdo interno precisa ser verificado após descompactação."
            else
                status="ERRO"
                details+=" Falha na integridade ZIP."
            fi
        else
            status="ERRO"
            details="Arquivo ZIP vazio."
        fi
    fi
    echo "| $(basename ${NCBI_DATASETS_ZIP_FILE}) | ${status} | ${details} |" >> "${SUMMARY_FILE}"
    echo "" >> "${SUMMARY_FILE}"
    echo "Nota: Se o arquivo ZIP estiver OK, os arquivos individuais dentro dele (genomic.fna, genomic.gff, etc.) devem ser verificados após a descompactação manual ou programática." >> "${SUMMARY_FILE}"
else
    echo "Download tentado via FTP (arquivos individuais)." >> "${SUMMARY_FILE}"
    echo "| Arquivo Esperado | Status | Detalhes |" >> "${SUMMARY_FILE}"
    echo "|---|---|---|" >> "${SUMMARY_FILE}"
    for file_name in "${EXPECTED_TOMATO_FILES[@]}"; do
        file_path="${TOMATO_DIR}/${file_name}"
        status="NÃO ENCONTRADO"
        details="-"
        if [ -f "${file_path}" ]; then
            status="ENCONTRADO"
            if [ -s "${file_path}" ]; then
                details="Não vazio."
                if [[ "${file_name}" == *.gz ]]; then
                    if gzip -t "${file_path}" &> /dev/null; then
                        details+=" Integridade GZIP OK."
                    else
                        status="ERRO"
                        details+=" Falha na integridade GZIP."
                    fi
                fi
            else
                status="ERRO"
                details="Arquivo vazio."
            fi
        fi
        echo "| ${file_name} | ${status} | ${details} |" >> "${SUMMARY_FILE}"
    done
fi

log_validation_message "Sumário da validação gerado em ${SUMMARY_FILE}."
log_validation_message "Fim do script de validação de dados genômicos."

exit 0

