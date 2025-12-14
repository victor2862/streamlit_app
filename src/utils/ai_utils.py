import json
from pathlib import Path

def modelos_disponiveis():
    """
    Lê o arquivo src/ai/models.json e retorna a lista de modelos disponíveis.
    Retorna uma lista vazia em caso de erro.
    """
    try:
        # Caminho relativo: src/utils/.. -> src -> ai/models.json
        current_dir = Path(__file__).parent
        models_file_path = current_dir.parent / 'ai' / 'models.json'
        
        if not models_file_path.exists():
            print(f"Arquivo de modelos não encontrado: {models_file_path}")
            return []
            
        with open(models_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('models', [])
            
    except Exception as e:
        print(f"Erro ao carregar modelos: {e}")
        return []
