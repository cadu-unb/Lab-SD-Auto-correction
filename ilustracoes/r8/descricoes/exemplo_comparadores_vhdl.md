# Exemplo de operadores de comparação em VHDL

**Origem:** [Roteiro_08_v3.pdf](../Roteiro_08_v3.pdf), página 4, imagem com as seis atribuições condicionais após a Figura 3.

## O que a ilustração deve explicar

A imagem original é uma captura de código de baixa legibilidade. A versão melhorada deve ser um **quadro de referência tipográfico**, ou um bloco de código selecionável, que compare os seis operadores usados no exemplo `A` versus `x"35"`. Ela não representa uma nova entidade: serve para explicar como escrever flags com `when-else`.

## Composição da versão melhorada

- Dar ao quadro o título **Comparações com um valor BCD** e uma linha de contexto: `A` é um vetor de oito bits que contém dois dígitos BCD válidos; `x"35"` é o padrão `0011 0101`, interpretado como **35 em BCD**.
- Organizar seis linhas em uma tabela: saída (`Ya` a `Yf`), condição (`>`, `>=`, `<`, `<=`, `=`, `/=`), significado em português e um exemplo curto. Usar fonte monoespaçada para os operadores e destacar a diferença entre `>` e `>=`, e entre `=` e `/=`.
- Abaixo da tabela, mostrar uma atribuição completa e selecionável, por exemplo `Ya <= '1' when (A > x"35") else '0';`, em um bloco de código `vhdl`. Indicar que as outras cinco linhas seguem a mesma estrutura, trocando o operador e o nome da saída. Se o objetivo for preservar todas as linhas do original, exibir as seis atribuições completas, não uma imagem rasterizada.
- Separar visualmente **representação** de **significado**: o literal hexadecimal `x"35"` vale `0x35` em bits, mas os dois nibbles representam os dígitos decimais `3` e `5` em BCD. Evitar a afirmação de que `0x35` é o inteiro binário 35.
- Uma nota pequena pode repetir o segundo exemplo do texto, `x"13F7" = 0001 0011 1111 0111`, deixando claro que ele demonstra a escrita compacta de bits e não um valor BCD válido em todos os nibbles.

## Cuidados de fidelidade

Preservar exatamente os seis operadores VHDL e as saídas `Ya`–`Yf`. A versão redesenhada não deve introduzir nomes `T5`–`T60` no código ilustrativo sem explicar que seriam uma aplicação posterior. Se for mostrado código compilável, declarar o tipo e a biblioteca de comparação usados; a imagem original não especifica esses detalhes.

## Forma e acessibilidade

Preferir texto Markdown ou SVG com texto legível a uma captura de tela. Usar realce de sintaxe moderado, sem depender apenas da cor para identificar operadores. Texto alternativo, caso a versão final seja imagem: “Tabela com os operadores VHDL maior, maior ou igual, menor, menor ou igual, igual e diferente, aplicados à comparação de A com o valor BCD 35.”
