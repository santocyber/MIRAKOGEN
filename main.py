import sys
import os
# Garantir que o diretório src seja encontrado para importações, não modificar esta parte
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, request, jsonify, render_template
# Importar o módulo de simulação que foi copiado para o diretório src
from integrated_genetic_manipulation_module import MetabolicEngineeringSimulator

app = Flask(__name__, static_folder='static', template_folder='static')

# Instanciar o simulador globalmente ou por requisição, dependendo da necessidade de estado
# Para este exemplo, uma nova instância por requisição é mais simples e evita problemas de estado concorrente
# No entanto, carregar o modelo SBML a cada requisição pode ser lento para modelos grandes.
# Uma otimização seria carregar o modelo uma vez na inicialização do app se o modelo for fixo.
simulator_instance = MetabolicEngineeringSimulator() # Carrega o modelo padrão na inicialização

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_simulation', methods=['POST'])
def run_simulation_route():
    data = request.get_json()
    simulation_type = data.get('simulation_type')
    
    # Resetar o modelo do simulador para o estado original antes de cada nova simulação da UI
    # Isso garante que as modificações de uma simulação não afetem a próxima
    if simulator_instance.original_model:
        simulator_instance.reset_model()
    else:
        return jsonify({'error': 'Modelo base não carregado no servidor.'}), 500

    results = None
    error_message = None

    try:
        if simulation_type == 'fba_original':
            solution = simulator_instance.run_fba(description='FBA no modelo original via Web UI')
            if solution:
                results = {
                    'status': solution.status,
                    'objective_value': solution.objective_value if solution.status == 'optimal' else None,
                    'fluxes': {k: v for k, v in solution.fluxes.items() if abs(v) > 1e-9} # Mostrar fluxos significativos
                }
            else:
                error_message = 'Falha ao executar FBA original.'

        elif simulation_type == 'coexpression':
            gene_ids = data.get('gene_ids_to_overexpress', [])
            factor = data.get('overexpression_factor', 2.0)
            # A função no módulo conceitual já roda FBA internamente e imprime.
            # Para a API, queremos capturar a saída ou o estado do modelo/solução.
            # Por enquanto, vamos simular a chamada e retornar uma mensagem conceitual.
            # Em uma implementação real, a função simulate_gene_coexpression modificaria o current_model
            # e então chamaríamos run_fba nele.
            
            # Como é conceitual, vamos apenas chamar e pegar o resultado do FBA que ela executa.
            solution = simulator_instance.simulate_gene_coexpression(gene_ids, factor)
            if solution:
                results = {
                    'status': solution.status,
                    'objective_value': solution.objective_value if solution.status == 'optimal' else None,
                    'fluxes': {k: v for k, v in solution.fluxes.items() if abs(v) > 1e-9}
                }
            else:
                error_message = f'Falha ao simular co-expressão para {gene_ids}.'

        elif simulation_type == 'crispr_knockout' or simulation_type == 'crispr_upregulate':
            gene_id = data.get('gene_id_to_modify')
            mod_type = data.get('modification_type')
            if not gene_id:
                error_message = 'ID do gene para CRISPR não fornecido.'
            else:
                solution = simulator_instance.simulate_crispr_modification(gene_id, mod_type)
                if solution:
                    results = {
                        'status': solution.status,
                        'objective_value': solution.objective_value if solution.status == 'optimal' else None,
                        'fluxes': {k: v for k, v in solution.fluxes.items() if abs(v) > 1e-9}
                    }
                else:
                    error_message = f'Falha ao simular CRISPR {mod_type} para {gene_id}.'
        else:
            error_message = 'Tipo de simulação inválido.'

        if error_message:
            return jsonify({'error': error_message}), 400
        if results is None and not error_message: # Caso alguma lógica não retorne resultado nem erro
             return jsonify({'error': 'Resultado da simulação não pôde ser determinado.'}), 500
        
        return jsonify({'data': results})

    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

if __name__ == '__main__':
    # Para teste local e para que o deploy_expose_port funcione corretamente:
    app.run(host='0.0.0.0', port=5000)

