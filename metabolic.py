# metabolic.py
import cobra

def load_metabolic_model(path: str):
    """Carrega um modelo SBML de tomate para COBRApy."""
    return cobra.io.read_sbml_model(path)

def test_pathway_flux(model, pathway: dict) -> bool:
    """
    pathway deve ter lista 'reactions': IDs das reações no modelo.
    Ativa cada reação (0..1000) e roda FBA.
    Retorna True se objectivo > 1e-6.
    """
    with model:
        # ativa as reações da via
        for rxn_id in pathway.get('reactions', []):
            if rxn_id in model.reactions:
                model.reactions.get_by_id(rxn_id).bounds = (0, 1000)
        sol = model.optimize()
        return sol.status == 'optimal' and sol.objective_value > 1e-6
