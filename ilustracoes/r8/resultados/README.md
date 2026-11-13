# Roteiro 08 — figuras redesenhadas

Fontes das ilustrações; os produtos compilados ficam em [`out/`](out/).
Classificação e auditoria: [`../CLASSIFICACAO_ILUSTRACOES.md`](../CLASSIFICACAO_ILUSTRACOES.md).

| Figura | Fonte | Formato | Saída em `out/` |
|---|---|---|---|
| 1 | `figura_01_contador100_sistema.tex` | TikZ | `.pdf` `.png` |
| 2(a) | `figura_02a_contador100.tex` | TikZ | `.pdf` `.png` |
| 2(b) | `figura_02b_contador10.tex` | TikZ | `.pdf` `.png` |
| 3(a) | `figura_03a_temporizador.tex` | TikZ | `.pdf` `.png` |
| 3(b) | `figura_03b_timeflags.tex` | TikZ | `.pdf` `.png` |
| 3(c) | `figura_03c_arquitetura_temporizador.tex` | TikZ | `.pdf` `.png` |
| 4 | `figura_04_cruzamento.svg` e `.html` | SVG/HTML | `.svg` `.png` |
| 5(a) | `figura_05a_exp8visto3.tex` | TikZ | `.pdf` `.png` |
| 5(b) | `figura_05b_maqestados.tex` | TikZ | `.pdf` `.png` |

## Compilar

```powershell
.\compilar.ps1
```

- Compila cada `figura_*.tex` com `pdflatex` em `out/` (PDF vetorial) e gera PNG com `pdftoppm`.
- Copia o SVG da Figura 4 para `out/`.

Requer MiKTeX. Todas as figuras TikZ usam o pacote [`caixapreta.sty`](caixapreta.sty), que define o estilo único das caixas pretas (`\caixa`, `\entrada`, `\saida`, `\constante`, `\rodape` …). Para mudar a aparência de todas ao mesmo tempo, edite só esse arquivo.

## Observações

- **`figura_04_cruzamento.html`** é o SVG com um seletor de estado dos semáforos (inclui o modo intermitente de 1 s). É **gerado**: edite o `.svg` e recopie o conteúdo para dentro do `<figure>`. O PNG em `out/` foi tirado dessa página, então o `compilar.ps1` não o refaz.
- **Correções do roteiro original**, registradas nos comentários dos `.tex`:
  - Figuras 5(a) e 5(b): a segunda saída de 3 bits era rotulada `semaforoA`; aqui é `semaforoB`.
  - Figura 3(a): o exemplo mostra os quatro flags (`T5=T6=T20=1`, `T60=0`).
  - Figura 3(c): acrescenta a derivação dos barramentos BCD até a borda do sistema.
- **Interpretação** (não está no PDF), só na legenda da Figura 5(b): `T6` ↔ amarelo, `T5` ↔ vermelho nos dois, `T20` ↔ troca antecipada, `T60` ↔ fim do verde.
