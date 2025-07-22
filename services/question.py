import warnings
import json
from pathlib import Path

# Assume que 'paths.py' está no mesmo diretório ou acessível
from paths import DIR_QUESTIONS, DIR_IMAGE

class Question:
    def __init__(self, R_n: int,
                 statement: list,
                 simulationTime: int = 0,
                 entries: dict = {},
                 modelsim_labels: dict = {},
                 illustration_fileName: str = '',
                 illustration_width: int = 0,
                 math_expression: str = '' ,
                 table: list = []):
        if type(statement) == str:
            statement = [statement]
        self.R_n = R_n
        self.body = {'statement'       : statement,
                     'modelsim_labels' : modelsim_labels,
                     'simulationTime'  : simulationTime}
        self.entries = entries
        
        # --- MODIFICAÇÃO (REQ 4) ---
        # Garante que apenas o NOME do arquivo seja armazenado, e não o caminho completo.
        # Isso torna os arquivos de questão (.txt) portáteis.
        final_fileName = ''
        if illustration_fileName:
            final_fileName = Path(illustration_fileName).name

        self.illustration = {'fileName': final_fileName,
                             'width'   : illustration_width}
                             
        self.math_expression = math_expression
        self.table = table
        self.id_code = None

    def save(self):
        """Salva a questão em um arquivo .txt no formato JSON."""
        if self.verify():
            self.id_code = self.id_code_criation()
            file_path = DIR_QUESTIONS / self.id_code
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.to_dict(), f, ensure_ascii=False, indent=4)
                print(f"Questão salva com sucesso em '{file_path}'")
            except IOError as e:
                warnings.warn(f"Não foi possível salvar a questão em '{file_path}': {e}")
        else:
            warnings.warn(f"Atenção: Uma questão com o mesmo corpo (statement) já existe. A operação de salvar foi cancelada.")

    def verify(self) -> bool:
        """Verifica se uma questão com o mesmo corpo já existe."""
        for file_path in DIR_QUESTIONS.glob('*.txt'):
            try:
                other_question = Question.from_dict(str(file_path))
                if self == other_question:
                    return False
            except (json.JSONDecodeError, KeyError, FileNotFoundError) as e:
                warnings.warn(f"Aviso: O arquivo '{file_path}' está corrompido ou em formato inválido e será ignorado. Erro: {e}")
                continue
        return True

    def id_code_criation(self) -> str:
        """Gera o nome do arquivo no formato 'A{R_n}E{n+1}'."""
        prefix = f'A{self.R_n}E'
        relevant_files = list(DIR_QUESTIONS.glob(f'{prefix}*.txt'))
        if not relevant_files:
            return f'{prefix}1.txt'
        max_n = 0
        for file in relevant_files:
            try:
                num_str = file.stem[len(prefix):]
                num = int(num_str)
                if num > max_n:
                    max_n = num
            except (ValueError, IndexError):
                continue
        new_n = max_n + 1
        return f'{prefix}{new_n}.txt'

    def __eq__(self, otherQuestion) -> bool:
        """Verifica se os corpos (statement) das questões são iguais."""
        if not isinstance(otherQuestion, Question):
            return NotImplemented
        # Compara apenas o primeiro elemento do statement para simplificar
        return self.body['statement'][0] == otherQuestion.body['statement'][0]

    def to_dict(self) -> dict:
        """Converte a instância da classe para um dicionário serializável."""
        return {
            'R_n': self.R_n,
            'statement': self.body['statement'],
            'modelsim_labels': self.body['modelsim_labels'],
            'simulationTime': self.body['simulationTime'],
            'entries': self.entries,
            'illustration_fileName': self.illustration.get('fileName', ''),
            'illustration_width': self.illustration.get('width', 0),
            'math_expression': self.math_expression,
            'table': self.table
        }

    @classmethod
    def from_dict(cls, source):
        """Cria uma instância da classe a partir de um dicionário ou arquivo JSON."""
        if isinstance(source, dict):
            data = source
        elif isinstance(source, (str, Path)):
            with open(source, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            raise TypeError("A fonte deve ser um dicionário ou o caminho para um arquivo.")
        return cls(**data)

if __name__ == "__main__":
    # O diretório 'services/database/questions' será criado no mesmo
    # local do script, caso ainda não exista.

    # Exemplo 1: Questão com imagem
    q1 = Question(
        R_n='2',
        statement=['Descrever em VHDL e simular no ModelSim uma entidade com três bits de entrada (A, B e Cin) e dois bits de saída (S e Cout) que implemente um somador completo, descrito pelas seguintes funções lógicas.'],
        entries={},
        illustration_fileName=str(DIR_IMAGE / 'E0F1.pdf')
    )

    # Exemplo 2: Questão com tabela
    q2 = Question(
        R_n='3',
        statement=['Utilizando atribuições condicionais (when-else), escrever em VHDL e simular uma entidade que descreva um multiplexador 8 para 1 (8x1). Essa entidade deve ter dois vetores de entrada (S com 3 bits e D com 8 bits) e um bit de saída (Y). A tabela verdade do multiplexador é apresentada abaixo.'],
        table=[['Entrada (S)', 'Saida (Y)'], ['000', 'D0'], ['001', 'D1'], ['010', 'D2'], ['011', 'D3'], ['100', 'D4'], ['101', 'D5'], ['110', 'D6'], ['111', 'D7']]
    )
    
    # Exemplo 3: Questão duplicada para teste
    q3 = Question(
        R_n='2',
        statement=['Descrever em VHDL e simular no ModelSim uma entidade com três bits de entrada (A, B e Cin) e dois bits de saída (S e Cout) que implemente um somador completo, descrito pelas seguintes funções lógicas.']
    )

    # --- TESTES ---
    print("--- Testando Comparações ---")
    print(f"q1 e q2 têm o mesmo corpo? {q1 == q2}")  # False
    print(f"q1 e q3 têm o mesmo corpo? {q1 == q3}")  # True
    print("-" * 20)

    # Para um teste limpo, você pode apagar a pasta 'services/database/Questions' antes de rodar.
    print("\n--- Testando Salvamento ---")
    print("Tentando salvar q1...")
    q1.save()  # Deve salvar como A2E1.txt (assumindo que a pasta está vazia)
    
    print("\nTentando salvar q2...")
    q2.save()  # Deve salvar como A3E1.txt
    
    print("\nTentando salvar q3 (duplicada de q1)...")
    q3.save()  # NÃO deve salvar, pois é duplicada. Deve emitir um aviso.
    
    print("\nTentando salvar q1 novamente...")
    q1.save()  # NÃO deve salvar, pois já existe. Deve emitir um aviso.
    
    # Criando mais uma questão para o R_n = 2 para testar id_code_criation
    q4 = Question(R_n='2', statement='Este é um corpo de questão completamente novo para o R_n 2.')
    print("\nTentando salvar q4 (nova questão para R_n=2)...")
    q4.save()  # Deve salvar como A2E2.txt