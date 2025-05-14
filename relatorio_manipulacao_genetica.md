# Relatório de Simulações de Manipulação Genética

Data: 2025-05-14 14:07:57

## Resumo do Modelo
- Modelo: Tomateiro (iHY3410)
- Reações: 2224
- Metabólitos: 2084
- Genes: 0

## Valor Objetivo Base
- Status: optimal
- Valor: 0.0

## Resultados das Simulações

| Tipo | Alvo | Descrição | Valor Objetivo | Status | % Mudança |
|------|------|-----------|----------------|--------|----------|
| Baseline | N/A | Modelo Base | 0.0 | optimal | N/A |
| Deleção | G6P_bm_tx | Deleção G6P_bm_tx... | 0.0 | optimal | Ref. N/A ou 0 |
| Deleção | reac_897 | Deleção reac_897... | 0.0 | optimal | Ref. N/A ou 0 |
| Deleção | reac_1875 | Deleção reac_1875... | 0.0 | optimal | Ref. N/A ou 0 |
| Superexpressão | G6P_bm_tx | Superexp. G6P_bm_tx... | 0.0 | optimal | Ref. N/A ou 0 |
| Superexpressão | reac_897 | Superexp. reac_897... | 0.0 | optimal | Ref. N/A ou 0 |
| Superexpressão | reac_1875 | Superexp. reac_1875... | 0.0 | optimal | Ref. N/A ou 0 |
| Co-expressão | G6P_bm_tx+reac_897 | Co-exp. G6P_bm_tx...+reac_897... | 0.0 | optimal | Ref. N/A ou 0 |


## Visualização

![Comparação de Manipulações Genéticas](plots/manipulacoes_geneticas_tomateiro.png)

## Detalhes das Reações Mais Afetadas


## Conclusões e Próximos Passos

Esta simulação demonstra o potencial de manipulações genéticas no metabolismo do tomateiro. As manipulações foram simuladas usando deleção e superexpressão de reações como proxy para técnicas como CRISPR/Cas9 e engenharia de fatores de transcrição.

### Limitações
- O modelo iHY3410 não possui associações gene-proteína-reação (GPRs) detalhadas, limitando a simulação direta de manipulações gênicas.
- A função objetivo teve que ser definida artificialmente em alguns casos, o que pode não representar perfeitamente o crescimento ou produção de biomassa real.

### Próximos Passos
1. Reconstruir ou encontrar um modelo metabólico para morango (Fragaria x ananassa) com GPRs.
2. Adicionar/Refinar GPRs ao modelo do tomateiro usando os dados genômicos e transcriptômicos.
3. Identificar vias metabólicas específicas para transferência entre morango e tomateiro.
4. Simular manipulações genéticas mais específicas focadas nas vias de interesse, utilizando GPRs.
5. Integrar os resultados em uma interface web interativa.
