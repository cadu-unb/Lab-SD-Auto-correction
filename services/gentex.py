
## Bibliotecas Universais
import os
from pathlib import Path
from datetime import datetime

## Bibliotecas do Projeto
# Classe para estruturar um modelo de questão.
from question import Question

# KONSTANTES
from paths import DIR_FONTS, DIR_TEMPLATE, DIR_DOC 

## Informacoes:
# Na pasta template existem os arquivos 'logofootnote' e 'logoheader'.



# --- Exemplo de Uso ---
if __name__ == "__main__":
    print(datetime.now().strftime('%Y-%m-%d_%H'+'h'+'%M'))
