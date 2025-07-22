import os
import json
import subprocess
from pathlib import Path
from paths import DIR_QUESTIONS, DIR_LATEX_TEX, DIR_LATEX_OUT, DIR_IMAGE
from question import Question

# --- FUNÇÕES GERADORAS DE CÓDIGO LATEX ---

def gerar_capa(num_experimento: str, objetivos: list, instrucoes: list) -> str:
    """Gera o código LaTeX para a capa do documento."""
    
    objetivos_latex = "\\begin{itemize}\n" + "".join([f"\\item {obj}\n" for obj in objetivos]) + "\\end{itemize}"
    instrucoes_latex = "\\begin{itemize}\n" + "".join([f"\\item {inst}\n" for inst in instrucoes]) + "\\end{itemize}"
    
    avaliacao_latex = r"""
\begin{itemize}
    \item O relatório é individual e receberá uma nota de 0 a 10, considerando os seguintes aspectos:
    \begin{itemize}
        \item Documentação do código, contida no relatorio (pdf) e no codigo vhdl- 20\% da nota do projeto;
        \item Compilação do código, apresentada no relatorio do projeto econfirmado pelo codigo vhd -10\% da nota do projeto;
        \item Simulação do código, apresentada no relatório do projeto econfirmado pelo codigo vhd - 70\% da nota do projeto.
    \end{itemize}
\end{itemize}
    """

    return f"""
\\begin{{center}}
    {{\\fontsize{{16pt}}{{18pt}}\\selectfont \\textbf{{Laboratório de Sistemas Digitais\\\\Experimento {num_experimento}}}}}
\\end{{center}}

\\vspace{{1cm}}

\\noindent\\textbf{{OBJETIVO:}}
{objetivos_latex}

\\vspace{{0.5cm}}

\\noindent\\textbf{{INSTRUÇÕES:}}
{instrucoes_latex}

\\vspace{{0.5cm}}

\\noindent\\textbf{{AVALIAÇÃO:}}
{avaliacao_latex}

\\newpage
"""

def gerar_questionario() -> str:
    """Gera o código LaTeX para a seção de questionário."""
    questionario_latex = ""
    
    # Encontra todos os arquivos de questão na pasta
    arquivos_questoes = sorted(DIR_QUESTIONS.glob('A*.txt'))
    
    if not arquivos_questoes:
        return "\\section*{Nenhuma questão encontrada}\n"
        
    for i, file_path in enumerate(arquivos_questoes, 1):
        try:
            q = Question.from_dict(file_path)
            
            # Título da Questão
            questionario_latex += f"\\subsection*{{Questão {i:02d}}}\n"
            
            # Corpo da Questão (statement)
            for parte in q.body['statement']:
                # Verifica se há "Dica:" para aplicar negrito
                if "Dica:" in parte:
                    parte = parte.replace("Dica:", "\\textbf{Dica:}")
                questionario_latex += f"{parte}\n\n"

            # Expressão Matemática
            if q.math_expression:
                questionario_latex += f"\\begin{{equation*}}\n\t{q.math_expression}\n\\end{{equation*}}\n\n"
            
            # Ilustração (imagem)
            if q.illustration and q.illustration.get('fileName'):
                img_path = Path(q.illustration['fileName']).name # Pega apenas o nome do arquivo
                width = q.illustration.get('width', 10) # Largura padrão de 10cm
                questionario_latex += f"""
\\begin{{center}}
    \\includegraphics[width={width}cm]{{{str(DIR_IMAGE / img_path)}}}
\\end{{center}}
"""
            # Tabela
            if q.table:
                num_cols = len(q.table[0])
                cols_format = " ".join(["l" for _ in range(num_cols)])
                questionario_latex += f"\\begin{{center}}\n\\begin{{tabular}}{{{cols_format}}}\n\\hline\n"
                # Cabeçalho
                header = " & ".join([f"\\textbf{{{cell}}}" for cell in q.table[0]]) + " \\\\\n\\hline\n"
                questionario_latex += header
                # Corpo da tabela
                for row in q.table[1:]:
                    questionario_latex += " & ".join(map(str, row)) + " \\\\\n"
                questionario_latex += "\\hline\n\\end{tabular}\n\\end{center}\n\n"

        except Exception as e:
            print(f"Erro ao processar o arquivo {file_path}: {e}")
            
    questionario_latex += "\\newpage\n"
    return questionario_latex

def gerar_material_consulta(links_teoria: dict) -> str:
    """Gera o código LaTeX para a seção de material de consulta."""
    
    links_latex = ""
    if links_teoria:
        links_latex += "\\begin{itemize}\n"
        for nome, link in links_teoria.items():
            # A chave da solução é escapar o caractere '_'
            link_escapado = link.replace('_', r'\_')
            links_latex += f"    \\item {nome}: \\href{{{link}}}{{{link_escapado}}}\n"
        links_latex += "\\end{itemize}\n"

    # Escapando os underscores dos links fixos também
    link_template_1 = "link_do_modelo_de_relatorio_1".replace('_', r'\_')
    link_template_modelsim = "link_do_modelo_de_relatorio_ModelSim".replace('_', r'\_')

    return f"""
\\section*{{Material para Consulta}}

\\subsection*{{Modelo de Relatório}}
\\begin{{itemize}}
    \\item Para o Experimento 1, utilize este \\href{{{link_template_1}}}{{template}}.
    \\item Para os demais experimentos, utilize o \\href{{{link_template_modelsim}}}{{modelo para ModelSim}}.
\\end{{itemize}}

\\subsection*{{Arquivos de Teoria}}
{links_latex}
"""

def compilar_latex(tex_file_path: Path):
    """Compila o arquivo .tex para .pdf usando pdflatex."""
    if not tex_file_path.exists():
        print(f"Arquivo não encontrado: {tex_file_path}")
        return

    # Garante que o diretório de saída exista
    DIR_LATEX_OUT.mkdir(parents=True, exist_ok=True)
    
    # Define o diretório de trabalho como a pasta onde o .tex está localizado
    working_directory = tex_file_path.parent
    
    command = [
        "pdflatex",
        "-interaction=nonstopmode",
        f"-output-directory={DIR_LATEX_OUT}",
        tex_file_path.name # Usar apenas o nome do arquivo, pois já estamos no diretório correto
    ]
    
    print(f"Compilando {tex_file_path.name}...")
    try:
        # É necessário rodar duas vezes para garantir que referências sejam resolvidas
        # A chave da solução é o 'cwd' (current working directory)
        subprocess.run(command, check=True, capture_output=True, text=True, cwd=working_directory)
        process = subprocess.run(command, check=True, capture_output=True, text=True, cwd=working_directory)
        print(f"PDF gerado com sucesso em: {DIR_LATEX_OUT / tex_file_path.with_suffix('.pdf').name}")
    except FileNotFoundError:
        print("\nERRO: O comando 'pdflatex' não foi encontrado.")
        print("Por favor, instale uma distribuição LaTeX (como MiKTeX, TeX Live ou MacTeX) e garanta que ela esteja no PATH do sistema.")
    except subprocess.CalledProcessError as e:
        print(f"\nERRO ao compilar o LaTeX. Verifique o arquivo de log para mais detalhes:")
        log_path = DIR_LATEX_OUT / tex_file_path.with_suffix('.log').name
        print(f"Log de erro em: {log_path}")
        # Para depuração, você pode descomentar as linhas abaixo para ver a saída completa do erro
        # print("\n--- SAÍDA DO COMPILADOR ---")
        # print(e.stdout)


# --- SCRIPT PRINCIPAL ---

if __name__ == "__main__":
    
    # 1. DADOS DE ENTRADA (Personalize aqui)
    NUM_EXPERIMENTO = "02"
    OBJETIVOS = [
        "Aprender a descrever circuitos lógicos em VHDL.",
        "Simular o funcionamento de um somador completo e um multiplexador.",
        "Familiarizar-se com o ambiente de simulação ModelSim."
    ]
    INSTRUCOES = [
        "Leia atentamente o enunciado de cada questão.",
        "Implemente o código VHDL conforme solicitado.",
        "Anexe ao relatório o código-fonte, a forma de onda da simulação e uma breve explicação dos resultados."
    ]
    LINKS_TEORIA = {
        "Introdução ao VHDL": "http://seusite.com/intro_vhdl.pdf",
        "Guia do ModelSim": "http://seusite.com/guia_modelsim.pdf"
    }
    
    # 2. MONTAGEM DO DOCUMENTO LATEX
    
    # Carrega os pacotes e o cabeçalho
    with open(DIR_LATEX_TEX / "pacotes.tex", "r", encoding="utf-8") as f:
        pacotes = f.read()
    with open(DIR_LATEX_TEX / "cabecalho.tex", "r", encoding="utf-8") as f:
        cabecalho = f.read()

    # Gera o conteúdo de cada seção
    capa_content = gerar_capa(NUM_EXPERIMENTO, OBJETIVOS, INSTRUCOES)
    questionario_content = gerar_questionario()
    material_consulta_content = gerar_material_consulta(LINKS_TEORIA)
    
    # Concatena todas as partes para formar o documento final
    documento_final_latex = f"""
\\documentclass{{article}}
{pacotes}

\\begin{{document}}
{cabecalho}
\\vspace{{2cm}} % Espaço para não sobrepor o cabeçalho

{capa_content}
{questionario_content}
{material_consulta_content}

\\end{{document}}
"""
    
    # 3. SALVAR O ARQUIVO .TEX E COMPILAR PARA PDF
    
    # Define o nome do arquivo de saída .tex
    nome_arquivo_saida = f"Experimento_{NUM_EXPERIMENTO}.tex"
    caminho_arquivo_tex = DIR_LATEX_TEX / nome_arquivo_saida
    
    # Salva o conteúdo no arquivo .tex
    with open(caminho_arquivo_tex, "w", encoding="utf-8") as f:
        f.write(documento_final_latex)
        
    print(f"Arquivo LaTeX gerado em: {caminho_arquivo_tex}")
    
    # Compila o arquivo .tex para gerar o PDF
    compilar_latex(caminho_arquivo_tex)