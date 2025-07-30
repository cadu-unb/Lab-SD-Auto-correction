import subprocess
from pathlib import Path
from paths import DIR_QUESTIONS, DIR_LATEX_TEX, DIR_LATEX_OUT, DIR_IMAGE, DIR_TEMPLATE
from question import Question

def preparar_arquivos_latex_com_paths_absolutos() -> dict:
    path_pacotes = str(DIR_LATEX_TEX / "pacotes.tex").replace('\\', '/')
    with open(DIR_LATEX_TEX / "cabecalho.tex", "r", encoding="utf-8") as f:
        conteudo_cabecalho = f.read()

    path_unb = str(DIR_TEMPLATE / 'unb.pdf').replace('\\', '/')
    path_dep = str(DIR_TEMPLATE / 'dep.pdf').replace('\\', '/')
    path_adress = str(DIR_TEMPLATE / 'adress.pdf').replace('\\', '/')
    
    conteudo_cabecalho = conteudo_cabecalho.replace('unb.pdf', path_unb)
    conteudo_cabecalho = conteudo_cabecalho.replace('dep.pdf', path_dep)
    conteudo_cabecalho = conteudo_cabecalho.replace('adress.pdf', path_adress)

    path_cabecalho_final = DIR_LATEX_TEX / "cabecalho_final.tex"
    with open(path_cabecalho_final, "w", encoding="utf-8") as f:
        f.write(conteudo_cabecalho)
        
    print(f"Cabeçalho com caminhos absolutos gerado em: {path_cabecalho_final}")

    return {
        "pacotes": path_pacotes,
        "cabecalho": str(path_cabecalho_final).replace('\\', '/')
    }

def gerar_capa(num_experimento: str, objetivos: list, instrucoes: list) -> str:
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
\\vspace{{-0.25cm}}
\\begin{{center}}
    {{\\fontsize{{16pt}}{{18pt}}\\selectfont \\textbf{{Laboratório de Sistemas Digitais\\\\Experimento {num_experimento}}}}}
\\end{{center}}
\\vspace{{0.3cm}}
\\hrule

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

    

def gerar_questionario(lista_questoes: list, diretorio_questoes: Path = DIR_QUESTIONS) -> str:
    questionario_latex = ""
    if not lista_questoes:
        return "\\section*{Nenhuma questão selecionada}\n"
    
    for i, nome_arquivo in enumerate(lista_questoes, 1):
        file_path = diretorio_questoes / nome_arquivo
        if not file_path.exists():
            print(f"Aviso: Arquivo de questão '{nome_arquivo}' não encontrado. Pulando.")
            continue
        try:
            q = Question.from_dict(file_path)
            questionario_latex += f"\\subsection*{{Questão {i:02d}}}\n"
            
            # --- MODIFICAÇÃO (REQ 1) ---
            # Lógica para adicionar espaçamentos e processar elementos
            
            # Parte 1 do enunciado
            if q.body['statement'] and q.body['statement'][0]:
                statement_part1 = q.body['statement'][0]
                if "Dica:" in statement_part1:
                    statement_part1 = statement_part1.replace("Dica:", "\\textbf{Dica:}")
                questionario_latex += f"{statement_part1}\n"

            has_elements = q.math_expression or (q.illustration and q.illustration.get('fileName')) or q.table
            
            # Adiciona espaço ANTES dos elementos, se houver algum
            if has_elements:
                questionario_latex += "\n\\vspace{1cm}\n"

            # Processa os elementos (matemática, ilustração, tabela)
            if q.math_expression:
                questionario_latex += f"\\begin{{equation*}}\n\t{q.math_expression}\n\\end{{equation*}}\n"
            
            if q.illustration and q.illustration.get('fileName'):
                # --- MODIFICAÇÃO (REQ 4) ---
                # Reconstrói o caminho completo da imagem usando DIR_IMAGE
                img_filename = q.illustration['fileName']
                img_path = str(DIR_IMAGE / img_filename).replace('\\', '/')
                print('\n', '\n', '\n', img_path, '\n', '\n', '\n')
                width = q.illustration.get('width', 10)
                questionario_latex += f"\\begin{{center}}\n    \\includegraphics[width={width}cm]{{{img_path}}}\n\\end{{center}}\n"

            if q.table:
                num_cols = len(q.table[0])
                cols_format = " ".join(["l"] * num_cols)
                questionario_latex += f"\\begin{{center}}\n\\begin{{tabular}}{{{cols_format}}}\n\\hline\n"
                header = " & ".join([f"\\textbf{{{cell}}}" for cell in q.table[0]]) + " \\\\\n\\hline\n"
                questionario_latex += header
                for row in q.table[1:]:
                    questionario_latex += " & ".join(map(str, row)) + " \\\\\n"
                questionario_latex += "\\hline\n\\end{tabular}\n\\end{center}\n"

            # Parte 2 do enunciado (se existir)
            if len(q.body['statement']) > 1 and q.body['statement'][1]:
                # Adiciona espaço DEPOIS dos elementos, se a parte 2 do texto existir
                if has_elements:
                    questionario_latex += "\n\\vspace{1cm}\n"
                
                statement_part2 = q.body['statement'][1]
                if "Dica:" in statement_part2:
                    statement_part2 = statement_part2.replace("Dica:", "\\textbf{Dica:}")
                questionario_latex += f"{statement_part2}\n"

            questionario_latex += "\n" # Espaço extra para o próximo item
                
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

def compilar_latex(tex_file_path: Path):
    """Compila o arquivo .tex para .pdf usando pdflatex."""
    DIR_LATEX_OUT.mkdir(parents=True, exist_ok=True)
    command = [ "pdflatex", "-interaction=nonstopmode", f"-output-directory={DIR_LATEX_OUT}", str(tex_file_path) ]
    print(f"Compilando {tex_file_path.name}...")
    try:
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
    
    # --- MODIFICAÇÃO PRINCIPAL ---
    # Defina aqui a lista de questões que você quer incluir no documento.
    # Os nomes devem corresponder exatamente aos arquivos na pasta 'database/questions'.
    QUESTOES_SELECIONADAS = [
        'A2E1.txt', 
        'A3E1.txt'
    ]

    # 2. PREPARAR ARQUIVOS E GERAR CONTEÚDO
    paths_latex = preparar_arquivos_latex_com_paths_absolutos()
    
    capa_content = gerar_capa(NUM_EXPERIMENTO, OBJETIVOS, INSTRUCOES)
    
    # Chamada da função atualizada, passando a lista de questões selecionadas
    questionario_content = gerar_questionario(QUESTOES_SELECIONADAS)
    
    material_consulta_content = gerar_material_consulta(LINKS_TEORIA)
    
    # 3. MONTAGEM DO DOCUMENTO LATEX COM \input{}
    documento_final_latex = f"""
\\documentclass{{article}}
\\input{{{paths_latex['pacotes']}}}

\\begin{{document}}
\\input{{{paths_latex['cabecalho']}}}

{capa_content}

\\input{{{paths_latex['cabecalho']}}}

{questionario_content}

\\input{{{paths_latex['cabecalho']}}}

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