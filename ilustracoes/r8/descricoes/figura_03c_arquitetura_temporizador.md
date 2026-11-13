# Figura 3(c) — arquitetura do sistema de temporização

**Origem:** [Roteiro_08_v3.pdf](../Roteiro_08_v3.pdf), página 3, Figura 3(c) (Questão 2).

## O que a ilustração deve explicar

Mostrar a ligação entre `contador100` e `timeflags` dentro do sistema da Questão 2. Esta é a figura que deve revelar o **fluxo dos dados**: o contador produz dezena e unidade BCD; `timeflags` lê esses barramentos e gera `T5`, `T6`, `T20` e `T60`.

## Composição da versão melhorada

- Usar uma moldura externa **Sistema de temporização**. Colocar `contador100` à esquerda e `timeflags` à direita, em duas colunas com setas horizontais, sem linhas sobrepostas.
- Ligar `reset` e `clock (1 Hz)` externos ao contador; rotular o reset como síncrono. Mostrar, em pequenos nós de constante, `/enable = '0'`, `load = '0'`, `dezload = "0000"` e `uniload = "0000"`.
- Ligar `cont_dezena[3:0]` do contador à entrada homônima de `timeflags`; fazer o mesmo com `cont_unidade[3:0]`. Escrever `4 bits, BCD` em cada ligação. Os quatro flags saem de `timeflags` para a borda direita da moldura, com um fio e rótulo próprios.
- Para reconciliar a caixa preta da Figura 3(a) com a arquitetura, mostrar uma **derivação** dos dois barramentos BCD também até a borda externa, com o rótulo “saídas BCD expostas”. Essa derivação deve partir dos mesmos fios que alimentam `timeflags`, sem duplicar contadores.
- Acrescentar uma legenda de direção: **contagem → comparação → flags**. Não desenhar realimentação dos flags ao contador, pois ela não aparece nessa arquitetura.

## Cuidados de fidelidade

`timeflags` é combinacional; o clock não deve ser ligado diretamente a ele. `/enable = '0'` habilita o contador porque a entrada é ativa em nível baixo. Os valores constantes da carga não devem ser confundidos com saídas. Manter os nomes `cont_dezena` e `cont_unidade` iguais nas duas entidades.

## Forma e acessibilidade

Produzir um SVG em paisagem, com no máximo dois níveis de moldura, largura dos barramentos explícita e contraste alto. Texto alternativo sugerido: “Sistema de temporização: contador100 recebe reset e clock de 1 Hz, envia dezena e unidade BCD a timeflags; este gera T5, T6, T20 e T60.”
