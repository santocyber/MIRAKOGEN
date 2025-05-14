Automatizar a aquisição de dados genômicos e metabólicos de repositórios públicos para morango e tomateiro.

**Repositórios e Ferramentas Identificados:**

1.  **NCBI Datasets:**
    *   Ferramenta de linha de comando: `datasets`
    *   Documentação: [https://www.ncbi.nlm.nih.gov/datasets/docs/v2/reference-docs/data-packages/genome/](https://www.ncbi.nlm.nih.gov/datasets/docs/v2/reference-docs/data-packages/genome/)
    *   Permite baixar genomas completos, sequências (FASTA para genoma, transcritos, proteínas) e anotações (GFF3, GTF, GBFF).
    *   Inclui verificação de integridade via `md5sum.txt`.

**Accessions de Referência (NCBI):**

*   **Morango (_Fragaria x ananassa_):**
    *   Assembly RefSeq: `GCF_034382235.1` (Zhengzhou Fruit Research Institute, CAAS, 2023/12/14, Complete Genome)
    *   Link NCBI Assembly: [https://www.ncbi.nlm.nih.gov/assembly/GCF_034382235.1](https://www.ncbi.nlm.nih.gov/assembly/GCF_034382235.1)
*   **Tomateiro (_Solanum lycopersicum_):**
    *   Assembly RefSeq: `GCF_000188115.5` (SL4.0, Solanaceae Genomics Project, 2025/02/27, Chromosome level)
    *   Link NCBI Assembly: [https://www.ncbi.nlm.nih.gov/assembly/GCF_000188115.5](https://www.ncbi.nlm.nih.gov/assembly/GCF_000188115.5)

**Tipos de Arquivos a Baixar:**

*   Sequência do Genoma Completo (FASTA): `*_genomic.fna`
*   Anotação Genômica (GFF3): `genomic.gff`
*   Sequências de Transcritos (FASTA): `rna.fna`
*   Sequências de Proteínas (FASTA): `protein.faa`

**Comandos `datasets` (Exemplos):**

```bash
# Para Morango (Fragaria x ananassa)
datasets download genome accession GCF_034382235.1 --include genome,gff3,rna,protein --filename fragaria_x_ananassa_GCF_034382235.1.zip
unzip fragaria_x_ananassa_GCF_034382235.1.zip -d fragaria_x_ananassa_GCF_034382235.1
cd fragaria_x_ananassa_GCF_034382235.1
md5sum -c md5sum.txt
cd ..

# Para Tomateiro (Solanum lycopersicum)
datasets download genome accession GCF_000188115.5 --include genome,gff3,rna,protein --filename solanum_lycopersicum_GCF_000188115.5.zip
unzip solanum_lycopersicum_GCF_000188115.5.zip -d solanum_lycopersicum_GCF_000188115.5
cd solanum_lycopersicum_GCF_000188115.5
md5sum -c md5sum.txt
cd ..
```

2.  **Modelos Metabólicos (SBML):**
    *   **BioModels Database:** Pesquisar por modelos existentes para _Fragaria x ananassa_ e _Solanum lycopersicum_.
        *   Link: [https://www.ebi.ac.uk/biomodels/](https://www.ebi.ac.uk/biomodels/)
    *   **ModelSEED / KBase:** Podem conter modelos reconstruídos ou permitir a reconstrução.
        *   Link ModelSEED: [https://modelseed.org/](https://modelseed.org/)
        *   Link KBase: [https://kbase.us/](https://kbase.us/)
    *   **Publicações Científicas:** Muitas vezes, modelos GEM são publicados como material suplementar em artigos.
    *   **Busca por APIs:** Verificar se esses repositórios oferecem APIs para download programático de modelos em formato SBML.

**Próximos Passos Imediatos:**

*   Verificar a disponibilidade da ferramenta `datasets` no sandbox ou instalá-la.
*   Desenvolver um script shell (`download_data.sh`) para automatizar os downloads do NCBI e a verificação de integridade.
*   Pesquisar modelos SBML nos repositórios mencionados e identificar como automatizar seu download.



**Atualização sobre Modelos Metabólicos (SBML):**

*   **Tomateiro (_Solanum lycopersicum_):**
    *   O modelo iHY3410 foi referenciado em publicações, mas o link direto para download do arquivo SBML no GitHub (MetClassNet/iHY3410) resultou em erro 404 (Não Encontrado).
    *   Buscas em BioModels não retornaram um modelo genômico específico e curado para _Solanum lycopersicum_ de forma direta e facilmente acessível para download automatizado.
    *   ModelSEED e KBase são plataformas que permitem a reconstrução de modelos a partir de genomas anotados. Esta será a abordagem principal caso um modelo SBML validado e pronto não seja localizado.
*   **Morango (_Fragaria x ananassa_):**
    *   A disponibilidade de modelos SBML genômicos curados e públicos para _Fragaria x ananassa_ é ainda mais limitada do que para o tomateiro.
    *   A reconstrução a partir do genoma anotado (baixado do NCBI) utilizando ferramentas como ModelSEED/KBase será a estratégia primária.

**Estratégia Adotada para Modelos SBML:**

1.  **Prioridade 1: Reconstrução Automatizada:** Utilizar os genomas e anotações (arquivos GFF3) baixados do NCBI como entrada para pipelines de reconstrução de modelos metabólicos em plataformas como KBase (que integra o ModelSEED) ou utilizando ferramentas de reconstrução _standalone_ que possam ser executadas no ambiente sandbox (se disponíveis e compatíveis).
2.  **Busca Contínua (Paralela):** Manter uma busca por modelos SBML publicados que possam ter se tornado disponíveis ou cujos links de download possam ser obtidos através de contato com autores ou em bancos de dados mais específicos, se encontrados.
3.  **Foco na Qualidade e Validação:** Qualquer modelo obtido (reconstruído ou baixado) passará por uma etapa de curadoria e validação (ex: verificação de consistência, gap-filling, comparação com dados fisiológicos conhecidos) antes de ser utilizado para simulações quantitativas.

