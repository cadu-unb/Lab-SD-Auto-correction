# Figura 2(a) — entidade `contador100` em operação livre

**Origem:** [Roteiro_08_v3.pdf](../Roteiro_08_v3.pdf), página 2, Figura 2(a) (Questão 1).

## O que a ilustração deve explicar

Mostrar como a entidade `contador100` aparece em uma instância usada para contar normalmente, sem carga de um valor inicial. A diferença em relação à Figura 1 deve ser visível: aqui, algumas entradas recebem **constantes**. A figura deve continuar sendo uma representação de interface, não um diagrama completo do circuito interno.

## Composição da versão melhorada

- Colocar `contador100` no centro. À esquerda, destacar `reset` e `clock` como sinais vindos do sistema; junto a `clock`, anotar **1 Hz**. À direita, desenhar `cont_dezena[3:0]` e `cont_unidade[3:0]` como dois barramentos BCD separados.
- Desenhar quatro pequenas fontes de constante, com fio e valor explícitos: `/enable = '0'` para habilitar a contagem, `load = '0'` para desabilitar a carga, `dezload = "0000"` e `uniload = "0000"`. Posicionar os valores junto ao ponto de conexão, sem parecer que fazem parte do nome da porta.
- Usar uma anotação lateral: **`reset` é síncrono**. Indicar que as saídas avançam de `00` a `99` e retornam a `00` na contagem de módulo 100. Mostrar a sequência `00 → 01 → … → 99 → 00` como resumo, não como tabela exaustiva.
- Acrescentar uma chamada discreta para a arquitetura: **dezena e unidade são implementadas por dois `contador10` em cascata**. A chamada não deve esconder as portas da caixa preta.

## Cuidados de fidelidade

O enunciado usa `/enable` ativo em nível baixo; portanto, `'0'` significa **habilitado**, não desligado. `dezload` e `uniload` permanecem ligados a zero, mas `load = '0'` faz com que esses valores não sejam carregados durante a contagem normal. Não desenhar uma saída de oito bits única: o documento separa dezena e unidade em dois vetores de quatro bits.

## Forma e acessibilidade

Usar SVG ou outro vetor com setas de fluxo da esquerda para a direita, tipografia uniforme e valores de constantes legíveis. Texto alternativo sugerido: “Instância do contador100 com enable ativo em zero, load desativado e entradas de carga zeradas; reset e clock externos; saídas BCD de dezena e unidade.”
