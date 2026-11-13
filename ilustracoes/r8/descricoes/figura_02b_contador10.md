# Figura 2(b) — entidade `contador10`

**Origem:** [Roteiro_08_v3.pdf](../Roteiro_08_v3.pdf), página 2, Figura 2(b) (Questão 1).

## O que a ilustração deve explicar

Especificar a caixa preta do contador de um dígito decimal que serve de componente para o módulo 100. O contador é uma máquina de estados Moore com dez estados, associados às saídas BCD de `0000` a `1001`. A figura redesenhada deve tornar evidente quais sinais permitem a contagem e qual sinal permite o cascateamento.

## Composição da versão melhorada

- Desenhar um bloco `contador10` com entradas `reset`, `clock`, `/enable`, `/RCI`, `load` e `D[3:0]` à esquerda; saídas `Q[3:0]` e `/RCO` à direita. Usar linhas simples para sinais de um bit e barramentos identificados como `4 bits` para `D` e `Q`.
- Escrever junto às portas `/enable`, `/RCI` e `/RCO`: **ativo em nível baixo**. Explicar em uma legenda compacta que a contagem é habilitada quando `/enable = '0'` **e** `/RCI = '0'`.
- Representar os dez valores válidos de `Q` como uma faixa `0000 (0) → … → 1001 (9) → 0000 (0)`. Não sugerir que os estados BCD `1010` a `1111` participam da contagem normal.
- Mostrar a regra de prioridade em uma caixa lateral: **`reset` síncrono > `load` síncrono > contagem**. `load = '1'` leva ao estado indicado por `D`, conforme o enunciado.
- Para explicar a cascata sem poluir a interface, acrescentar um pequeno detalhe à direita: `/RCO` de um dígito pode alimentar `/RCI` do dígito seguinte. Indicar `/RCO = '0'` **se e somente se** `Q = "1001"`, conforme o roteiro.

## Cuidados de fidelidade

Não trocar os nomes `RCI` e `RCO`, nem inverter o sentido da conexão de cascata. Não substituir o barramento BCD por um número decimal sem mostrar a codificação de quatro bits. O roteiro não define, nesta figura, o tratamento de um `D` inválido para BCD; a arte não deve inventar esse comportamento.

## Forma e acessibilidade

Preferir diagrama vetorial claro, sem fios cruzados e com todas as condições ativas escritas por extenso. Texto alternativo sugerido: “Contador módulo 10 com reset e load síncronos, enable e ripple carry-in ativos em zero, entrada e saída BCD de quatro bits e ripple carry-out ativo em zero quando Q vale nove.”
