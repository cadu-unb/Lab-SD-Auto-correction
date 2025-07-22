from pathlib import Path
import os

__pathing__ = Path(os.getcwd())

# genTEX
DIR_FONTS       = __pathing__ / 'services' / 'database' / 'fonts'
DIR_TEMPLATE    = __pathing__ / 'services' / 'database' / 'template'
DIR_DOC         = __pathing__ / 'services' / 'database' / 'output_pdf'
DIR_LATEX       = __pathing__ / 'services' / 'database' / 'LaTex'
DIR_LATEX_TEX   = __pathing__ / 'services' / 'database' / 'LaTex' / 'tex'
DIR_LATEX_OUT   = __pathing__ / 'services' / 'database' / 'LaTex' / 'output'

# question
DIR_QUESTIONS   = __pathing__ / 'services' / 'database' / 'questions'
DIR_IMAGE       = __pathing__ / 'services' / 'database' / 'image'

# Existem
DIR_FONTS.mkdir(parents=True, exist_ok=True)   
DIR_TEMPLATE.mkdir(parents=True, exist_ok=True)
DIR_DOC.mkdir(parents=True, exist_ok=True)
DIR_QUESTIONS.mkdir(parents=True, exist_ok=True)

__all__ = ["DIR_FONTS", "DIR_TEMPLATE", "DIR_DOC", "DIR_LATEX", "DIR_LATEX_TEX", "DIR_LATEX_OUT", "DIR_QUESTIONS", "DIR_IMAGE"]

if __name__ == 'main':
    for name_adress, some_adress in zip(["DIR_FONTS", "DIR_TEMPLATE", "DIR_DOC", "DIR_LATEX", "DIR_LATEX_TEX", "DIR_LATEX_OUT", "DIR_QUESTIONS", "DIR_IMAGE"],[DIR_FONTS, DIR_TEMPLATE, DIR_DOC, DIR_LATEX, DIR_LATEX_TEX, DIR_LATEX_OUT, DIR_QUESTIONS, DIR_IMAGE]):
        print(f'{name_adress}: {some_adress}')