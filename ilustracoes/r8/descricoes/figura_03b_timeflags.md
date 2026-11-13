# Figura 3(b) — comparador combinacional `timeflags`

**Origem:** [Roteiro_08_v3.pdf](../Roteiro_08_v3.pdf), página 3, Figura 3(b) (Questão 2).

## O que a ilustração deve explicar

Esclarecer a função da entidade `timeflags`: receber a contagem em BCD e produzir quatro indicadores de marcos de tempo. O texto do roteiro a descreve como **circuito puramente combinacional**, implementável com atribuições condicionais e operadores de comparação em VHDL.

## Composição da versão melhorada

- Desenhar dois barramentos de entrada à esquerda, `cont_dezena[3:0]` e `cont_unidade[3:0]`, com a indicação “BCD; 4 bits cada”. Desenhar quatro fios de saída à direita, `T5`, `T6`, `T20` e `T60`, identificados como `1 bit`.
- Dentro do bloco ou em um painel imediatamente abaixo, apresentar a junção conceitual `dezena | unidade` e os quatro marcos `05`, `06`, `20` e `60`. A legenda deve dizer que a comparação é feita sobre **dígitos BCD válidos**, não sobre um número decimal armazenado diretamente.
- Explicitar que não há `clock`, `reset` nem memória nessa entidade. Uma faixa lateral “lógica combinacional” impede que o leitor confunda os flags com saídas registradas do contador.
- Se a arte trouxer condições lógicas, usar a leitura indicada por “já se passaram”: `T5: tempo ≥ 05`, `T6: tempo ≥ 06`, `T20: tempo ≥ 20`, `T60: tempo ≥ 60`. Mostrar que os limites são expressos em BCD e manter os quatro nomes originais.

## Cuidados de fidelidade

Não acrescentar portas que não existem na Figura 3(b). Não misturar o operador VHDL de comparação com a interpretação decimal: por exemplo, `x"35"` é um padrão de oito bits que representa `35` **em BCD**. O tratamento de nibbles inválidos de BCD não é definido pelo roteiro e não deve ser presumido na figura.

## Forma e acessibilidade

Usar alinhamento preciso, barramentos visualmente distintos de fios de um bit e rótulos legíveis sem depender de cor. Texto alternativo sugerido: “Bloco combinacional timeflags que compara dezena e unidade BCD e produz os indicadores T5, T6, T20 e T60.”
