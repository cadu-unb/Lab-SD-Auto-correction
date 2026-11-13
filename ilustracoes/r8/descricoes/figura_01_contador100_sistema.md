# Figura 1 — interface do contador módulo 100

**Origem:** [Roteiro_08_v3.pdf](../Roteiro_08_v3.pdf), página 2, Figura 1 (Questão 1).

## O que a ilustração deve explicar

Apresentar a interface externa do sistema solicitado na Questão 1: um contador de `00` a `99`, com dois dígitos BCD de quatro bits. A figura é uma **caixa preta**; sua arquitetura interna não deve aparecer aqui. Ela deve permitir que alguém identifique cada porta, sua largura e o efeito das entradas de controle sem precisar ampliar o desenho.

## Composição da versão melhorada

- Usar um bloco central chamado **Contador módulo 100**. Colocar as entradas à esquerda, agrupadas em **controle** (`reset`, `clock`, `/enable`, `load`) e **valor de carga** (`dezload[3:0]`, `uniload[3:0]`). Colocar as saídas à direita, agrupadas em **BCD** (`cont_dezena[3:0]` e `cont_unidade[3:0]`).
- Marcar `clock` como **1 Hz**. Identificar `reset` e `load` como **síncronos**: seus efeitos são lidos no clock. Marcar `/enable` com a indicação textual **ativo em nível baixo**; o prefixo `/` sozinho não deve ser a única pista.
- Desenhar fios simples para sinais de um bit e barramentos mais grossos para os quatro bits. Escrever `4 bits` junto a cada barramento, sem deixar a largura implícita no nome.
- Abaixo do bloco, mostrar uma pequena amostra de saída, por exemplo `cont_dezena = 0100` e `cont_unidade = 0010` para `42`. Rotular a amostra como **exemplo**, não como estado fixo.
- Incluir uma nota curta: **a entidade é construída com dois contadores módulo 10 em cascata**, assunto detalhado nas figuras seguintes.

## Cuidados de fidelidade

Preservar os nomes das seis entradas e duas saídas da figura original. Não confundir o valor hexadecimal do barramento com o número decimal exibido: cada grupo de quatro bits representa um **dígito BCD**. Se houver uma legenda de prioridade, colocá-la como `reset > load > contagem`, conforme a descrição da Questão 1.

## Forma e acessibilidade

Produzir uma ilustração vetorial horizontal, com texto selecionável, contraste alto e setas rotuladas. Não depender de cor para diferenciar controle, dados e saída. Texto alternativo sugerido: “Caixa preta do contador módulo 100: entradas reset, clock de 1 Hz, enable ativo em nível baixo, load e dois valores BCD de carga; saídas BCD de dezena e unidade, quatro bits cada.”
