import warnings
import os
import json
from pathlib import Path

# Define o caminho para o "banco de dados" e garante que o diretório exista.
# As questões serão salvas em .../services/database/questions/
__pathing__ = Path(os.getcwd()) / 'services' / 'database'
QUESTIONS_DIR = __pathing__ / 'questions'
QUESTIONS_DIR.mkdir(parents=True, exist_ok=True)

class question:
    def __init__(self, R_n: int, statement: str, label: str, simulationTime: int, entries: dict = {}, 
                 illustration_fileName: str = '', illustration_width: int = 0, table: list = []):
        self.R_n = R_n
        self.body = {'statement'        : statement,
                     'label'            : label,
                     'simulationTime'   : simulationTime}
        self.entries = entries
        self.illustration = {'fileName': illustration_fileName,
                             'width': illustration_width}
        self.table = table
        # Atributo para guardar o nome do arquivo após ser salvo
        self.id_code = None

    def save(self):
        """
        Com base no método verify(), decide se deve salvar a questão.
        Para salvar, usa-se to_dict() para serializar os dados da questão para um
        arquivo .txt no formato JSON. O nome do arquivo é gerado por id_code_criation().
        Caso a questão já exista, uma mensagem de aviso é exibida.
        """
        if self.verify():
            self.id_code = self.id_code_criation()
            file_path = QUESTIONS_DIR / self.id_code

            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    # Usamos json.dump para escrever o dicionário no arquivo de forma legível
                    json.dump(self.to_dict(), f, ensure_ascii=False, indent=4)
                print(f"Questão salva com sucesso em '{file_path}'")
            except IOError as e:
                warnings.warn(f"Não foi possível salvar a questão em '{file_path}': {e}")
        else:
            warnings.warn(f"Atenção: Uma questão com o mesmo corpo (statement) já existe. A operação de salvar foi cancelada.")

    def verify(self) -> bool:
        """
        Verifica se já existe uma questão com o mesmo corpo (statement) no diretório QUESTIONS_DIR.
        Utiliza o método from_dict() para criar objetos a partir dos arquivos e __eq__() para comparar.
        Retorna True se a questão for única (pode ser salva) e False caso contrário.
        """
        for file_path in QUESTIONS_DIR.glob('*.txt'):
            try:
                # Cria uma instância de 'question' a partir do arquivo JSON
                other_question = question.from_dict(file_path)
                # Usa __eq__ para comparar. Se for igual, achou uma duplicata.
                if self == other_question:
                    return False  # Encontrou duplicata
            except (json.JSONDecodeError, KeyError, FileNotFoundError) as e:
                warnings.warn(f"Aviso: O arquivo '{file_path}' está corrompido, em formato inválido ou não foi encontrado e será ignorado. Erro: {e}")
                continue
        
        return True  # Nenhuma duplicata encontrada

    def id_code_criation(self) -> str:
        """
        Gera o nome do arquivo no formato 'A{R_n}E{n+1}'.
        Ex: Para R_n = 1 e arquivos 'A1E1.txt', 'A1E2.txt' existentes, o resultado será 'A1E3.txt'.
        """
        prefix = f'A{self.R_n}E'
        
        # Filtra os arquivos no diretório que começam com o prefixo desejado
        relevant_files = list(QUESTIONS_DIR.glob(f'{prefix}*.txt'))
        
        if not relevant_files:
            return f'{prefix}1.txt'

        max_n = 0
        for file in relevant_files:
            try:
                # Extrai o número do final do nome do arquivo (ex: de 'A1E12.txt' extrai '12')
                num_str = file.stem[len(prefix):]
                num = int(num_str)
                if num > max_n:
                    max_n = num
            except (ValueError, IndexError):
                # Ignora arquivos que não seguem o padrão numérico esperado
                continue
        
        new_n = max_n + 1
        return f'{prefix}{new_n}.txt'

    def __eq__(self, otherQuestion) -> bool:
        """
        Verifica se os corpos (statement) das questões são iguais.
        O método foi ajustado para seguir a convenção do Python:
        retornar True se os objetos forem iguais, e False caso contrário.
        """
        if not isinstance(otherQuestion, question):
            return NotImplemented  # Boa prática para tipos incompatíveis
        return self.body['statement'] == otherQuestion.statement

    def to_dict(self) -> dict:
        """
        Converte a instância da classe para um dicionário.
        Objetos do tipo Path são convertidos para string para serem serializáveis em JSON.
        """
        illustration_filename = self.illustration.get('fileName', '')
        return {
            'R_n': self.R_n,
            'statement': self.body['statement'],
            'label' : self.body['label'],
            'simulationTime' : self.body['simulationTime'],
            'entries': self.entries,
            'illustration_fileName': str(illustration_filename) if illustration_filename else '',
            'illustration_width': self.illustration.get('width', 0),
            'table': self.table
        }

    @classmethod
    def from_dict(cls, source):
        """
        Cria uma instância da classe a partir de um dicionário ou do caminho de um arquivo JSON.
        Usa .get() para extrair os dados, evitando erros caso uma chave não exista.
        """
        if isinstance(source, dict):
            data = source
        elif isinstance(source, (str, Path)):
             with open(source, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            raise TypeError("A fonte deve ser um dicionário ou o caminho para um arquivo.")

        return cls(
            R_n=data.get('R_n'),
            statement=data.get('statement'),
            entries=data.get('entries', {}),
            illustration_fileName=data.get('illustration_fileName', ''),
            illustration_width=data.get('illustration_width', 0),
            table=data.get('table', [])
        )

if __name__ == "__main__":
    # O diretório 'services/database/questions' será criado no mesmo
    # local do script, caso ainda não exista.

    # Exemplo 1: Questão com imagem
    q1 = question(
        R_n='2',
        statement='Descrever em VHDL e simular no ModelSim uma entidade com três bits de entrada (A, B e Cin) e dois bits de saída (S e Cout) que implemente um somador completo, descrito pelas seguintes funções lógicas.',
        entries={},
        illustration_fileName=str(__pathing__ / 'image' / 'E0F1.pdf')
    )

    # Exemplo 2: Questão com tabela
    q2 = question(
        R_n='3',
        statement='Utilizando atribuições condicionais (when-else), escrever em VHDL e simular uma entidade que descreva um multiplexador 8 para 1 (8x1). Essa entidade deve ter dois vetores de entrada (S com 3 bits e D com 8 bits) e um bit de saída (Y). A tabela verdade do multiplexador é apresentada abaixo.',
        table=[['Entrada (S)', 'Saida (Y)'], ['000', 'D0'], ['001', 'D1'], ['010', 'D2'], ['011', 'D3'], ['100', 'D4'], ['101', 'D5'], ['110', 'D6'], ['111', 'D7']]
    )
    
    # Exemplo 3: Questão duplicada para teste
    q3 = question(
        R_n='2',
        statement='Descrever em VHDL e simular no ModelSim uma entidade com três bits de entrada (A, B e Cin) e dois bits de saída (S e Cout) que implemente um somador completo, descrito pelas seguintes funções lógicas.'
    )

    # --- TESTES ---
    print("--- Testando Comparações ---")
    print(f"q1 e q2 têm o mesmo corpo? {q1 == q2}")  # False
    print(f"q1 e q3 têm o mesmo corpo? {q1 == q3}")  # True
    print("-" * 20)

    # Para um teste limpo, você pode apagar a pasta 'services/database/questions' antes de rodar.
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
    q4 = question(R_n='2', statement='Este é um corpo de questão completamente novo para o R_n 2.')
    print("\nTentando salvar q4 (nova questão para R_n=2)...")
    q4.save()  # Deve salvar como A2E2.txt