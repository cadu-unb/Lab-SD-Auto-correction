import os
import json
import subprocess
from pathlib import Path
# As constantes de caminho importadas do seu arquivo paths.py
from paths import DIR_QUESTIONS, DIR_LATEX_TEX, DIR_LATEX_OUT, DIR_IMAGE, DIR_TEMPLATE
from question import Question

# --- FUNÇÃO NOVA ---
def preparar_arquivos_latex_com_paths_absolutos() -> dict:
    """
    Prepara os arquivos de template LaTeX, inserindo caminhos absolutos para
    garantir que o compilador encontre todos os recursos.
    Retorna um dicionário com os caminhos para os arquivos prontos para uso.
    """
    # Garante que o LaTeX use barras normais (/) em vez de invertidas (\)
    path_pacotes = str(DIR_LATEX_TEX / "pacotes.tex").replace('\\', '/')
    
    # 1. Ler o conteúdo do cabeçalho original
    with open(DIR_LATEX_TEX / "cabecalho.tex", "r", encoding="utf-8") as f:
        conteudo_cabecalho = f.read()

    # 2. Substituir nomes de arquivos de imagem por seus caminhos absolutos
    path_unb = str(DIR_TEMPLATE / 'unb.pdf').replace('\\', '/')
    path_dep = str(DIR_TEMPLATE / 'dep.pdf').replace('\\', '/')
    path_adress = str(DIR_TEMPLATE / 'adress.pdf').replace('\\', '/')
    
    conteudo_cabecalho = conteudo_cabecalho.replace('unb.pdf', path_unb)
    conteudo_cabecalho = conteudo_cabecalho.replace('dep.pdf', path_dep)
    conteudo_cabecalho = conteudo_cabecalho.replace('adress.pdf', path_adress)

    # 3. Salvar o cabeçalho modificado em um novo arquivo para não alterar o original
    path_cabecalho_final = DIR_LATEX_TEX / "cabecalho_final.tex"
    with open(path_cabecalho_final, "w", encoding="utf-8") as f:
        f.write(conteudo_cabecalho)
        
    print(f"Cabeçalho com caminhos absolutos gerado em: {path_cabecalho_final}")

    return {
        "pacotes": path_pacotes,
        "cabecalho": str(path_cabecalho_final).replace('\\', '/')
    }


# --- FUNÇÕES GERADORAS DE CONTEÚDO (sem alteração, exceto pela correção de links) ---

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
    arquivos_questoes = sorted(DIR_QUESTIONS.glob('A*.txt'))
    if not arquivos_questoes:
        return "\\section*{Nenhuma questão encontrada}\n"
    for i, file_path in enumerate(arquivos_questoes, 1):
        try:
            q = Question.from_dict(file_path)
            questionario_latex += f"\\subsection*{{Questão {i:02d}}}\n"
            for parte in q.body['statement']:
                if "Dica:" in parte:
                    parte = parte.replace("Dica:", "\\textbf{Dica:}")
                questionario_latex += f"{parte}\n\n"
            if q.math_expression:
                questionario_latex += f"\\begin{{equation*}}\n\t{q.math_expression}\n\\end{{equation*}}\n\n"
            if q.illustration and q.illustration.get('fileName'):
                # Usar caminho absoluto para a imagem da questão também
                img_path = str(Path(q.illustration['fileName'])).replace('\\', '/')
                width = q.illustration.get('width', 10)
                questionario_latex += f"\\begin{{center}}\n    \\includegraphics[width={width}cm]{{{img_path}}}\n\\end{{center}}\n"
            if q.table:
                num_cols = len(q.table[0])
                cols_format = " ".join(["l" for _ in range(num_cols)])
                questionario_latex += f"\\begin{{center}}\n\\begin{{tabular}}{{{cols_format}}}\n\\hline\n"
                header = " & ".join([f"\\textbf{{{cell}}}" for cell in q.table[0]]) + " \\\\\n\\hline\n"
                questionario_latex += header
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
            link_escapado = link.replace('_', r'\_')
            links_latex += f"    \\item {nome}: \\href{{{link}}}{{{link_escapado}}}\n"
        links_latex += "\\end{itemize}\n"
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

# --- FUNÇÃO DE COMPILAÇÃO (simplificada, sem CWD) ---
def compilar_latex(tex_file_path: Path):
    """Compila o arquivo .tex para .pdf usando pdflatex."""
    DIR_LATEX_OUT.mkdir(parents=True, exist_ok=True)
    command = [ "pdflatex", "-interaction=nonstopmode", f"-output-directory={DIR_LATEX_OUT}", str(tex_file_path) ]
    print(f"Compilando {tex_file_path.name}...")
    try:
        # Roda duas vezes para garantir que as referências sejam resolvidas
        subprocess.run(command, check=True, capture_output=True, text=True)
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"PDF gerado com sucesso em: {DIR_LATEX_OUT / tex_file_path.with_suffix('.pdf').name}")
    except FileNotFoundError:
        print("\nERRO: O comando 'pdflatex' não foi encontrado. Instale uma distribuição LaTeX.")
    except subprocess.CalledProcessError as e:
        log_path = DIR_LATEX_OUT / tex_file_path.with_suffix('.log').name
        print(f"\nERRO ao compilar o LaTeX. Verifique o log em: {log_path}")

# --- SCRIPT PRINCIPAL ---
if __name__ == "__main__":
    # 1. DADOS DE ENTRADA (Personalize aqui)
    NUM_EXPERIMENTO = "02"
    OBJETIVOS = [ "Aprender a descrever circuitos lógicos em VHDL.", "Simular um somador e um multiplexador.", "Familiarizar-se com o ModelSim." ]
    INSTRUCOES = [ "Leia atentamente cada questão.", "Implemente o código VHDL.", "Anexe ao relatório o código-fonte e a simulação." ]
    LINKS_TEORIA = { "Introdução ao VHDL": "http://seusite.com/intro_vhdl.pdf", "Guia do ModelSim": "http://seusite.com/guia_modelsim.pdf" }

    # 2. PREPARAR ARQUIVOS E GERAR CONTEÚDO
    
    # MODIFICAÇÃO: Chama a nova função para preparar os arquivos com caminhos absolutos
    paths_latex = preparar_arquivos_latex_com_paths_absolutos()
    
    capa_content = gerar_capa(NUM_EXPERIMENTO, OBJETIVOS, INSTRUCOES)
    questionario_content = gerar_questionario()
    material_consulta_content = gerar_material_consulta(LINKS_TEORIA)
    
    # 3. MONTAGEM DO DOCUMENTO LATEX COM \input{}
    
    # MODIFICAÇÃO: O documento agora é bem mais limpo, usando \input{} com caminhos absolutos
    documento_final_latex = f"""
\\documentclass{{article}}

% Usa \\input com o caminho absoluto para os pacotes
\\input{{{paths_latex['pacotes']}}}

\\begin{{document}}

% Usa \\input com o caminho absoluto para o cabeçalho já processado
\\input{{{paths_latex['cabecalho']}}}
\\vspace{{2cm}} % Espaço para não sobrepor o cabeçalho

{capa_content}
{questionario_content}
{material_consulta_content}

\\end{{document}}
"""
    
    # 4. SALVAR O ARQUIVO .TEX E COMPILAR PARA PDF
    nome_arquivo_saida = f"Experimento_{NUM_EXPERIMENTO}.tex"
    caminho_arquivo_tex = DIR_LATEX_TEX / nome_arquivo_saida
    
    with open(caminho_arquivo_tex, "w", encoding="utf-8") as f:
        f.write(documento_final_latex)
        
    print(f"Arquivo LaTeX principal gerado em: {caminho_arquivo_tex}")
    
    compilar_latex(caminho_arquivo_tex)