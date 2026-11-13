# Figura 5(a) — interface externa `exp8visto3`

**Origem:** [Roteiro_08_v3.pdf](../Roteiro_08_v3.pdf), página 6, Figura 5(a) (Questão 3).

## O que a ilustração deve explicar

Apresentar o **sistema completo** de controle dos semáforos como caixa preta: recebe a chave liga/desliga, os sensores A e B e o clock; fornece o tempo em BCD e os comandos das luzes dos semáforos A e B. A figura redesenhada deve deixar claras as larguras dos vetores e corrigir um rótulo repetido na saída da figura original.

## Composição da versão melhorada

- Nomear o bloco `exp8visto3`. Agrupar as quatro entradas à esquerda: `ligadesliga`, `sensorA`, `sensorB` e `clock`, todas de **1 bit**. Indicar junto aos sensores a direção respectiva: A = norte–sul; B = leste–oeste.
- Agrupar as saídas à direita em **tempo BCD** (`cont_dezena[3:0]`, `cont_unidade[3:0]`) e **luzes** (`semaforoA[2:0]`, `semaforoB[2:0]`). Escrever `4 bits` nos barramentos de tempo e `3 bits` nos dos semáforos.
- Corrigir a última saída da imagem original: ela aparece novamente como `semaforoA`, mas o texto da Questão 3 exige uma saída para o semáforo da direção leste–oeste, portanto a versão melhorada deve rotulá-la **`semaforoB`**. Fazer a correção de modo explícito na documentação da arte.
- Incluir uma legenda de três casas para cada vetor de luz: **vermelho, amarelo, verde**, ordem descrita no texto que acompanha a Figura 5. Se a arte indicar índices de bit, fazê-lo de acordo com a implementação VHDL; o PDF não fixa esses índices de forma inequívoca no desenho.
- Uma pequena legenda pode explicar que `ligadesliga` desativado leva à alternância entre amarelo e apagado, mas não inventar qual nível lógico de `ligadesliga` corresponde a “ligado”.

## Cuidados de fidelidade

Não acrescentar entradas não mostradas, como um `reset` externo. O contador exibido nas saídas é o mesmo usado para temporização, com dezena e unidade separadas. A figura é uma interface de alto nível; as entidades internas pertencem a outro diagrama.

## Forma e acessibilidade

Usar dois grupos de saídas bem separados, nomes selecionáveis, largura de barramento escrita e alto contraste. Texto alternativo sugerido: “Caixa preta exp8visto3 com liga/desliga, sensores A e B e clock como entradas; saídas BCD de dezena e unidade e vetores de três bits para os semáforos A e B.”
