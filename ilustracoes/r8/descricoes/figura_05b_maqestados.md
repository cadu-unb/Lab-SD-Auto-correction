# Figura 5(b) — entidade `maqestados`

**Origem:** [Roteiro_08_v3.pdf](../Roteiro_08_v3.pdf), página 6, Figura 5(b) (Questão 3).

## O que a ilustração deve explicar

Mostrar a interface da máquina de estados que controla os semáforos e distinguir suas duas categorias de saída. `semaforoA` e `semaforoB` são saídas **Moore**, determinadas pelo estado atual. `resetcounter` é uma saída **Mealy**, ligada à decisão de mudar de estado e destinada a reinicializar o contador de tempo.

## Composição da versão melhorada

- Usar o nome `maqestados`, como no texto do roteiro. À esquerda, separar as entradas em **controle e tráfego** (`ligadesliga`, `clock`, `sensorA`, `sensorB`) e **marcos de tempo** (`T5`, `T6`, `T20`, `T60`). Todas são sinais de **1 bit**. Anotar A = norte–sul e B = leste–oeste.
- À direita, colocar `semaforoA[2:0]` e `semaforoB[2:0]` no grupo **Moore**; colocar `resetcounter` no grupo **Mealy**. Barramentos de luz com **3 bits** e `resetcounter` com **1 bit**. Uma linha explicativa deve associar `resetcounter` à condição `nextState ≠ currentState`, conforme o texto da Questão 3.
- Mostrar destinos conceituais em pequenas chamadas externas: os vetores vão para as luzes das respectivas vias; `resetcounter` vai para o reset síncrono de `contador100`. Os flags `T5`–`T60` vêm da entidade `timeflags`. Essas chamadas ajudam a localizar o bloco no sistema sem transformar a caixa preta em um diagrama de estado completo.
- Corrigir o segundo rótulo `semaforoA` repetido na imagem original para **`semaforoB`**. Não copiar a grafia ambígua do nome do bloco da imagem se ela diferir do nome `maqestados` usado pelo enunciado.
- Incluir uma legenda do ciclo esperado: verde por até `60 s` (ou troca antecipada após `20 s` nas condições descritas), amarelo por `6 s`, vermelho em ambas as vias por `5 s`; com o sistema desligado, alternância de amarelo e apagado a cada `1 s`. A legenda deve ser resumida e não desenhada como se cada duração fosse uma porta de entrada adicional.

## Cuidados de fidelidade

A figura original é de **interface**, não especifica todos os estados nem transições da máquina. Não inventar um diagrama de estados dentro do bloco. A saída Mealy depende do estado e das entradas que determinam `nextState`; os vetores de luz não devem ser rotulados como Mealy. Não supor a polaridade elétrica da chave `ligadesliga` sem consultar a implementação.

## Forma e acessibilidade

Preferir SVG horizontal com grupos de portas claramente delimitados, rótulos por extenso e diferenciação por texto além de cor. Texto alternativo sugerido: “Entidade maqestados recebe chave, clock, sensores A e B e flags T5, T6, T20 e T60; fornece semaforoA e semaforoB como saídas Moore e resetcounter como saída Mealy.”
