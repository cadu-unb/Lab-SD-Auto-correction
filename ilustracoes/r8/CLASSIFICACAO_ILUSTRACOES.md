# Roteiro 08 — classificação das ilustrações e auditoria das descrições

Base: [`Roteiro_08_v3.pdf`](Roteiro_08_v3.pdf) (6 páginas) → [`Roteiro_08_v3.md`](Roteiro_08_v3.md).
Descrições auditadas: [`descricoes/`](descricoes/) (10 arquivos). Cada descrição foi conferida contra o PDF.

## 1. Resumo

| Formato | Quantidade | Figuras |
|---|---|---|
| **LaTeX (TikZ)** | 8 | 1 · 2(a) · 2(b) · 3(a) · 3(b) · 3(c) · 5(a) · 5(b) |
| **Mermaid** | 0 | 3(c) foi tentada em Mermaid e **trocada por TikZ** (ver nota abaixo) |
| **HTML/SVG** | 1 | 4 |
| **Markdown nativo** (não é figura) | 1 | exemplo dos comparadores VHDL |
| **Novas, opcionais** | 2 | diagrama de estados do semáforo (Mermaid) · anel de 10 estados do `contador10` (Mermaid) |

Cobertura: o PDF tem exatamente 10 elementos gráficos (Fig. 1, 2a, 2b, 3a, 3b, 3c, 4, 5a, 5b + a captura de código). Todos têm descrição. Nenhum ficou sem arquivo.

## 2. Critério de escolha

| Use… | Quando a figura… | Por quê |
|---|---|---|
| **TikZ** | é **caixa preta**: portas em lados fixos, larguras de barramento com traço `/4`, nomes de porta alinhados | Precisão geométrica. O repositório já usa TikZ (`services/database/LaTex/*/pacotes.tex`) e o roteiro original é gerado por LaTeX, então a figura entra no PDF sem conversão e com a mesma tipografia |
| **Mermaid** | é **grafo de fluxo ou estados**: o que importa é a topologia e o sentido das setas | Escreve-se como texto, renderiza dentro do `.md` (GitHub, VS Code) e dá diff legível. **Não** posiciona portas nem desenha barramentos |
| **HTML/SVG** | é **cena espacial** ou precisa de cor, estado, interação ou animação | Controle total do desenho; já existe trabalho de animação de semáforos no repositório (`animacao/`) para reaproveitar |
| **Markdown nativo** | é **texto**, código ou tabela disfarçado de imagem | Selecionável, pesquisável, acessível |

Mermaid **não** serve para as caixas pretas **nem para a Fig. 3(c)**, que é um diagrama de blocos com portas: não coloca entradas à esquerda e saídas à direita de forma garantida, e não tem símbolo de barramento. Por isso todas as figuras de bloco ficam em TikZ.

## 3. Classificação por figura

| Figura | O que é | Formato | Motivo |
|---|---|---|---|
| **1** | Caixa preta do contador módulo 100 | **TikZ** | Interface com 6 entradas, 2 saídas de 4 bits |
| **2(a)** | Mesma caixa, com constantes nas entradas | **TikZ** | Reaproveita o macro da Fig. 1; só acrescenta fontes de constante |
| **2(b)** | Caixa preta do `contador10` | **TikZ** | Interface; sinais ativos em baixo (`/enable`, `/RCI`, `/RCO`) |
| **3(a)** | Caixa preta do temporizador | **TikZ** | Interface; 4 flags de 1 bit + 2 barramentos |
| **3(b)** | Caixa preta do `timeflags` | **TikZ** | Interface; entradas BCD, 4 flags |
| **3(c)** | Dois blocos ligados dentro de uma moldura | **TikZ** | Era Mermaid na primeira versão, mas o resultado ficou ruim: o Mermaid não posiciona portas nem desenha barramentos, e a figura vira um emaranhado de setas. Em TikZ ela reaproveita as mesmas caixas pretas das Figs. 3(a)/(b) e fica coerente com o original |
| **4** | Cruzamento em vista superior, semáforos e sensores | **HTML/SVG** | Cena espacial; permite mostrar A verde / B vermelho e, se quiser, animar |
| **5(a)** | Caixa preta `exp8visto3` | **TikZ** | Interface com dois grupos de saída |
| **5(b)** | Caixa preta `maqestados` | **TikZ** | Interface; separar visualmente Moore e Mealy |
| **Código** | Seis atribuições `when-else` em captura de tela | **Markdown** | Já convertido em bloco `vhdl` no `.md` |

**Dica de produção (TikZ):** definir **um único macro** `\caixapreta{título}{entradas}{saídas}` e gerar as 7 figuras a partir dele. Garante mesmo estilo, mesma espessura de linha e mesma notação de barramento em todo o roteiro.

### Figuras novas, opcionais (não existem no PDF)

| Figura | Formato | Observação |
|---|---|---|
| Diagrama de estados do controle do cruzamento | Mermaid `stateDiagram-v2` | O texto da Questão 3 dá o ciclo completo, mas **deixa ambiguidades** (lista na seção 5). A descrição da Fig. 5(b) proíbe estados dentro da caixa preta; esta seria uma figura separada, rotulada como derivada do texto |
| Anel de 10 estados do `contador10` (Moore) | Mermaid `stateDiagram-v2` | O texto fala em 10 estados; o PDF não desenha. Útil para o aluno, mas é acréscimo |

## 4. Auditoria das descrições

Legenda: ✅ confere com o PDF · ⚠ corrigir ou registrar · ❌ erro.

### Fig. 1 — [`figura_01_contador100_sistema.md`](descricoes/figura_01_contador100_sistema.md) — ✅ com ressalvas

- ✅ Portas e larguras conferem: `reset`, `clock`, `/enable`, `load`, `dezload[4]`, `uniload[4]` → `cont_dezena[4]`, `cont_unidade[4]`.
- ✅ `reset` e `load` síncronos, clock 1 Hz, `/enable` ativo em baixo: todos no enunciado.
- ⚠ **Prioridade `reset > load > contagem`.** O PDF enuncia essa regra no parágrafo do `contador10`, não do `contador100`. Vale para o 100 por herança (ele é feito de dois 10), mas a figura deve dizer isso.
- ⚠ **Duplicata parcial da Fig. 2(a).** As duas mostram a mesma caixa. A diferença é só o que está ligado nas entradas. Sugestão: manter as duas, mas gerar a 2(a) a partir da 1.

### Fig. 2(a) — [`figura_02a_contador100.md`](descricoes/figura_02a_contador100.md) — ✅

- ✅ Constantes conferem com o original: `/enable='0'`, `load='0'`, `dezload="0000"`, `uniload="0000"`.
- ✅ Alerta correto de que `'0'` em `/enable` significa *habilitado*.

### Fig. 2(b) — [`figura_02b_contador10.md`](descricoes/figura_02b_contador10.md) — ✅

- ✅ Entradas `reset`, `clock`, `/enable`, `/RCI`, `load`, `D[4]`; saídas `Q[4]`, `/RCO`. Confere.
- ✅ `/RCO='0'` se e somente se `Q="1001"`; contagem ativa com `/enable='0'` **e** `/RCI='0'`. Confere.
- ⚠ A faixa `0000 → … → 1001 → 0000` é um **acréscimo** (o PDF não desenha os estados). Aceitável, mas rotular como resumo.

### Fig. 3(a) — [`figura_03a_temporizador.md`](descricoes/figura_03a_temporizador.md) — ❌ exemplo induz a erro

- ❌ **Exemplo `cont = 20 ⇒ T20 = 1`.** O enunciado define cada flag como “**já se passaram** N segundos”, ou seja, comparação `>=`. Em 20 s, os flags valem `T5=1`, `T6=1`, `T20=1`, `T60=0`. Mostrar só `T20=1` sugere que os flags são pulsos exclusivos.
  - **Correção:** exemplo com os quatro flags: `20 → T5=1, T6=1, T20=1, T60=0`.
- ✅ Portas e larguras conferem.
- ⚠ O nome “Temporizador do semáforo” é uma sugestão; no PDF o bloco se chama “QUESTÃO 2”. Registrar a troca como escolha editorial.

### Fig. 3(b) — [`figura_03b_timeflags.md`](descricoes/figura_03b_timeflags.md) — ✅

- ✅ Entradas `cont_dezena[4]`, `cont_unidade[4]`; saídas `T5`, `T6`, `T20`, `T60`. Confere.
- ✅ “Puramente combinacional, sem `process`”: está no texto.
- ✅ A leitura `T5: tempo ≥ 05` etc. é coerente com “já se passaram”.
- 💡 *Opcional:* acrescentar que, **para dígitos BCD válidos**, a ordem numérica coincide com a ordem binária. É por isso que `A >= x"60"` funciona. Isso não está no PDF.

### Fig. 3(c) — [`figura_03c_arquitetura_temporizador.md`](descricoes/figura_03c_arquitetura_temporizador.md) — ⚠ desvio editorial

- ⚠ **Divergência do original, assumida na descrição, mas precisa de registro.** No PDF, a Fig. 3(c) só leva `T5..T60` para fora da moldura. Já a Fig. 3(a) promete também `cont_dezena` e `cont_unidade` como saídas. A descrição resolve isso desenhando uma derivação dos barramentos BCD até a borda. A correção está certa; deve constar como **“inconsistência do original 3(a) × 3(c), resolvida na redesenho”**, do mesmo jeito que o erro de rótulo da Fig. 5.
- ✅ Constantes `/enable='0'`, `load='0'`, `"0000"`, `"0000"` conferem.
- ✅ Clock **não** vai a `timeflags` (combinacional). Confere.

### Exemplo dos comparadores — [`exemplo_comparadores_vhdl.md`](descricoes/exemplo_comparadores_vhdl.md) — ⚠

- ⚠ **Perde os comentários.** O código original traz `-- operador "maior que"` etc. em cada linha. A descrição propõe `Ya <= '1' when (A > x"35") else '0';` sem eles. Manter as seis linhas completas com os comentários (feito em `Roteiro_08_v3.md`).
- ⚠ Para compilar, comparar `std_logic_vector` com `>` exige `ieee.numeric_std` (com conversão para `unsigned`) ou `ieee.std_logic_unsigned`. A descrição já avisa que o PDF não especifica a biblioteca. Coerente.
- ✅ A observação de que `x"13F7"` não é BCD válido (o nibble `F`) está correta.
- ✅ Dispensa figura: bloco `vhdl` + tabela no Markdown.

### Fig. 4 — [`figura_04_cruzamento.md`](descricoes/figura_04_cruzamento.md) — ❌ link quebrado

- ❌ **Link morto.** Referencia `../cruzamento_semaforos.svg` como “ilustração vetorial já criada”. Esse arquivo **não existe**: a pasta `ilustracoes/` só contém `r8/`. Ou o SVG não foi commitado, ou o caminho está errado. Localizar ou remover a frase.
- ⚠ **“`1` quando há veículo”.** O enunciado diz “1 bit que indica se há carros na direção…”, e a lógica de espera confirma. A polaridade está implícita, não literal. Marcar como inferência segura.
- ✅ A = norte–sul, B = leste–oeste; sensores antes da interseção. Confere.
- ✅ Os tempos 60/20/6/5/1 s ficam fora do mapa. Decisão correta.

### Fig. 5(a) — [`figura_05a_exp8visto3.md`](descricoes/figura_05a_exp8visto3.md) — ✅

- ✅ **Erro do original confirmado:** a figura mostra `semaforoA` duas vezes. A segunda deve ser `semaforoB`.
- ✅ Entradas `ligadesliga`, `sensorA`, `sensorB`, `clock`; saídas `cont_dezena[4]`, `cont_unidade[4]`, `semaforoA[3]`, `semaforoB[3]`. Confere.
- ✅ Ordem das cores (vermelho, amarelo, verde) está no texto da p. 6: “1 bit para cada cor, nessa ordem”. A descrição acerta ao não fixar o índice de bit (`2 downto 0` ou `0 to 2`), que o PDF não define.
- ✅ Sem `reset` externo. Confere: o `reset` do `contador100` vem de `resetcounter`.

### Fig. 5(b) — [`figura_05b_maqestados.md`](descricoes/figura_05b_maqestados.md) — ✅ com sugestão

- ✅ **Mesmo erro de rótulo** (duas saídas `semaforoA`). A correção está prevista.
- ✅ Entradas (8) e saídas (3) conferem. `resetcounter` = Mealy; `semaforoA/B` = Moore; `resetcounter='1'` quando `nextState ≠ currentState`.
- 💡 **Falta mapear os flags à função.** Pelas durações do texto: `T6` ↔ amarelo (6 s), `T5` ↔ vermelho-vermelho (5 s), `T20` ↔ troca antecipada, `T60` ↔ fim do verde. É inferência forte e ajudaria muito o aluno. Marcar como *interpretação*.
- ⚠ O resumo “verde até 60 s, ou troca antecipada após 20 s” omite que a troca antecipada tem **duas condições**: há carro esperando na outra via **e** não há carro atravessando na via atual.

## 5. Problemas transversais

1. **Convenção `[3:0]`.** As descrições escrevem `cont_dezena[3:0]`. O PDF só informa a largura (`4` com traço). `[3:0]` é convenção VHDL, não dado do roteiro. Aceitável, mas padronizar em todas as figuras.
2. **Idioma das legendas.** Os rótulos originais estão em inglês (“Figure 1…”). O `.md` usa “Figura”.
3. **Ambiguidades do enunciado** (a resolver antes de desenhar um diagrama de estados):
   - Depois do vermelho-vermelho (5 s), a via liberada é **sempre a oposta**, ou depende dos sensores?
   - Ao reativar a chave, o sistema volta a **qual estado**?
   - “Nenhuma luz acesa” no intermitente vale para os **dois** semáforos ao mesmo tempo?
   - Polaridade de `ligadesliga` (nível 1 = ligado?). O PDF não diz.
4. **Arquivos de saída.** Sugestão de pasta e nomes:

   ```
   ilustracoes/r8/figuras/
     figura_01_contador100_sistema.tex   (TikZ)
     figura_02a_contador100.tex
     figura_02b_contador10.tex
     figura_03a_temporizador.tex
     figura_03b_timeflags.tex
     figura_03c_arquitetura_temporizador.tex
     figura_04_cruzamento.html   (HTML/SVG)
     figura_05a_exp8visto3.tex
     figura_05b_maqestados.tex
   ```

## 6. Decisões que dependem de você

1. ~~Destino do `.md`~~ — resolvido: a Fig. 3(c) já está em TikZ, então serve tanto para o `.md` (PNG) quanto para o PDF.
2. **Fig. 4:** onde está `cruzamento_semaforos.svg`? Se não existir, parto do zero (ou da animação em `animacao/`).
3. **Figuras novas** (diagrama de estados do cruzamento; anel do `contador10`): quer incluir? A primeira exige resolver as ambiguidades da seção 5.3.

## Apêndice A — Inventário do PDF

| Página | Conteúdo | Elemento gráfico |
|---|---|---|
| 1 | Objetivos e instruções | — |
| 2 | Questão 01 | Fig. 1; Fig. 2(a); Fig. 2(b) |
| 3 | Questão 02 | Fig. 3(a); Fig. 3(b); Fig. 3(c) |
| 4 | Operadores de comparação | Captura de código (6 linhas) |
| 5 | Questão 03 | Fig. 4 |
| 6 | Questão 03 (cont.) | Fig. 5(a); Fig. 5(b) |

## Apêndice B — Correções de digitação feitas na conversão

| Original | Convertido |
|---|---|
| “formasíncrona” | “forma síncrona” |
| “econfirmado”, “relatorio”, “codigo vhd” | “e confirmado”, “relatório”, “código vhd” |
| “nota do projeto;” sem travessão | travessão adicionado |
| “quatro primeiro bits” | “quatro primeiros bits” |
| “(norte/sul),” com parêntese sobrando | parêntese removido |
| “Esta saída usada para cascatear” | “Esta saída é usada para cascatear” |
| “Este contador de módulo 10, deve ser implementado” | vírgula removida |
| “simulá-los Conforme descrito” | ponto antes do “Conforme” |
