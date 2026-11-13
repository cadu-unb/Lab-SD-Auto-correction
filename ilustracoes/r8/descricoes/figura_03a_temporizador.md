# Figura 3(a) — interface do temporizador

**Origem:** [Roteiro_08_v3.pdf](../Roteiro_08_v3.pdf), página 3, Figura 3(a) (Questão 2).

## O que a ilustração deve explicar

Mostrar o sistema de temporização como uma única caixa preta. O bloco recebe `reset` síncrono e `clock` de 1 Hz; entrega quatro indicadores de tempo e os dois dígitos BCD do contador. A versão melhorada deve permitir distinguir imediatamente **flags de um bit** de **barramentos de quatro bits**.

## Composição da versão melhorada

- Nomear o bloco **Temporizador do semáforo**. Entradas à esquerda: `reset` com a nota “síncrono” e `clock` com a nota “1 Hz”.
- Organizar as saídas à direita em dois grupos visuais. Grupo **marcos de tempo**: `T5`, `T6`, `T20`, `T60`, cada um com `1 bit` e uma legenda de `5 s`, `6 s`, `20 s` ou `60 s`. Grupo **tempo em BCD**: `cont_dezena[3:0]` e `cont_unidade[3:0]`, cada um com `4 bits`.
- Inserir uma pequena chave explicativa de que os flags sinalizam que o respectivo marco de tempo foi alcançado. Um exemplo legível pode mostrar `cont_dezena:cont_unidade = 20` e `T20 = 1`, rotulado claramente como **exemplo**, sem sugerir que os demais flags dependem de um registrador próprio.
- Usar uma linha divisória entre flags e dígitos BCD, mantendo todos os sinais do enunciado no mesmo bloco.

## Cuidados de fidelidade

Não reduzir as saídas `T5` a `T60` a um único vetor sem rótulos individuais. Não representar os dígitos BCD como saída decimal pronta para um display. A figura descreve a interface; a ligação entre `contador100` e `timeflags` pertence à Figura 3(c).

## Forma e acessibilidade

O desenho deve ser vetorial, horizontal e legível em largura de página, com sinais de entrada e saída nomeados também por texto. Texto alternativo sugerido: “Temporizador com reset síncrono e clock de 1 Hz; saídas de um bit T5, T6, T20 e T60 e saídas BCD de quatro bits para dezena e unidade.”
