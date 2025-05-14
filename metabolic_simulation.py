#!/usr/bin/env python
"""
Script para realizar simulações de fluxo metabólico (FBA, pFBA)
utilizando COBRApy, NumPy e SciPy nos modelos metabólicos gerados.
"""

import os
import cobra
import numpy as np
# SciPy pode ser necessário para otimizações mais complexas ou análises estatísticas,
# mas para FBA/pFBA básicos, COBRApy geralmente lida com os solvers.

MODEL_DIR = "/home/ubuntu/metabolic_models"
TOMATO_MODEL_FILE = os.path.join(MODEL_DIR, "solanum_lycopersicum_model.xml")
STRAWBERRY_MODEL_FILE = os.path.join(MODEL_DIR, "fragaria_x_ananassa_model.xml") # Placeholder, GFF ainda pendente

def load_model(model_path):
    """Carrega um modelo SBML do caminho especificado."""
    if not os.path.exists(model_path):
        print(f"ERRO: Arquivo de modelo não encontrado em {model_path}")
        return None
    try:
        model = cobra.io.read_sbml_model(model_path)
        print(f"Modelo {model.id} carregado com sucesso de {model_path}")
        return model
    except Exception as e:
        print(f"ERRO ao carregar o modelo de {model_path}: {e}")
        return None

def run_fba(model, objective_reaction_id=None):
    """Executa a Análise de Balanço de Fluxo (FBA) no modelo."""
    if not model:
        return None
    
    print(f"\nExecutando FBA para o modelo {model.id}...")
    if objective_reaction_id and objective_reaction_id in model.reactions:
        model.objective = objective_reaction_id
        print(f"Objetivo definido para a reação: {objective_reaction_id}")
    elif model.objective.expression == 0:
        if len(model.reactions) > 0:
            # Tenta definir um objetivo padrão se nenhum for especificado e o atual for zero
            # Para o modelo placeholder, será 'DUMMY_R01'
            default_obj = model.reactions[0].id
            try:
                model.objective = default_obj
                print(f"Nenhum objetivo explícito ou válido definido. Usando o primeiro objetivo encontrado no modelo: {default_obj}")
            except Exception as e:
                 print(f"ERRO ao definir o objetivo padrão {default_obj}: {e}. Verifique as reações do modelo.")
                 return None
        else:
            print("ERRO: Modelo não possui reações para definir um objetivo.")
            return None
    else:
        print(f"Usando objetivo já definido no modelo: {model.objective}")

    try:
        solution = model.optimize()
        print(f"Status da solução FBA: {solution.status}")
        if solution.status == 'optimal':
            print(f"Valor da função objetivo: {solution.objective_value:.4f}")
            # print("Fluxos principais:")
            # for reaction_id, flux in solution.fluxes.items():
            #     if abs(flux) > 1e-6: # Mostrar apenas fluxos significativos
            #         print(f"  {reaction_id}: {flux:.4f}")
            # Para o modelo placeholder, o fluxo será apenas na DUMMY_R01
            if 'DUMMY_R01' in solution.fluxes:
                print(f"  Fluxo em DUMMY_R01: {solution.fluxes['DUMMY_R01']:.4f}")
        else:
            print("Não foi encontrada uma solução ótima.")
        return solution
    except Exception as e:
        print(f"ERRO durante a execução do FBA: {e}")
        return None

def run_pfba(model, objective_reaction_id=None):
    """Executa a Análise de Balanço de Fluxo Parsimoniosa (pFBA) no modelo."""
    if not model:
        return None

    print(f"\nExecutando pFBA para o modelo {model.id}...")
    if objective_reaction_id and objective_reaction_id in model.reactions:
        model.objective = objective_reaction_id
        print(f"Objetivo definido para a reação: {objective_reaction_id}")
    elif model.objective.expression == 0:
        if len(model.reactions) > 0:
            default_obj = model.reactions[0].id
            try:
                model.objective = default_obj
                print(f"Nenhum objetivo explícito ou válido definido. Usando o primeiro objetivo encontrado no modelo: {default_obj}")
            except Exception as e:
                 print(f"ERRO ao definir o objetivo padrão {default_obj}: {e}. Verifique as reações do modelo.")
                 return None
        else:
            print("ERRO: Modelo não possui reações para definir um objetivo.")
            return None
    else:
        print(f"Usando objetivo já definido no modelo: {model.objective}")

    try:
        # pFBA requer que o modelo tenha uma solução ótima de FBA primeiro
        fba_solution = model.optimize()
        if fba_solution.status != 'optimal':
            print("ERRO: Solução FBA ótima não encontrada, pFBA não pode ser executado.")
            return None
        
        pfba_solution = cobra.flux_analysis.pfba(model)
        print(f"Status da solução pFBA: {pfba_solution.status} (geralmente o mesmo do FBA)")
        print(f"Valor da função objetivo (pFBA): {pfba_solution.objective_value:.4f}")
        # print("Fluxos principais (pFBA):")
        # for reaction_id, flux in pfba_solution.fluxes.items():
        #     if abs(flux) > 1e-6:
        #         print(f"  {reaction_id}: {flux:.4f}")
        if 'DUMMY_R01' in pfba_solution.fluxes:
            print(f"  Fluxo em DUMMY_R01 (pFBA): {pfba_solution.fluxes['DUMMY_R01']:.4f}")
        return pfba_solution
    except Exception as e:
        print(f"ERRO durante a execução do pFBA: {e}")
        return None

if __name__ == "__main__":
    print("Iniciando script de simulação metabólica...")

    # Carregar e simular modelo de tomateiro
    print("\n--- Processando Modelo de Tomateiro ---")
    tomato_model = load_model(TOMATO_MODEL_FILE)
    if tomato_model:
        # Para o modelo placeholder, o objetivo é 'DUMMY_R01'
        run_fba(tomato_model, objective_reaction_id='DUMMY_R01')
        run_pfba(tomato_model, objective_reaction_id='DUMMY_R01')
    else:
        print("Não foi possível carregar o modelo de tomateiro para simulação.")

    # Tentativa de carregar e simular modelo de morango (se existir e GFF for encontrado no futuro)
    # print("\n--- Processando Modelo de Morango ---")
    # strawberry_model = load_model(STRAWBERRY_MODEL_FILE)
    # if strawberry_model:
    #     # Supondo que o modelo de morango também teria um 'DUMMY_R01' se fosse um placeholder
    #     run_fba(strawberry_model, objective_reaction_id='DUMMY_R01') 
    #     run_pfba(strawberry_model, objective_reaction_id='DUMMY_R01')
    # else:
    #     print("Modelo de morango não disponível ou não pôde ser carregado para simulação.")

    print("\nScript de simulação metabólica concluído.")

