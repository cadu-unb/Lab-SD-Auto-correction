# Simulação de semáforos — como funciona

Arquivo: [`semaforos.html`](semaforos.html). Abre direto no navegador, sem servidor nem dependências.
Mostra uma via de mão dupla com canteiro central, retorno, acesso lateral, faixas de pedestres, cinco semáforos (A–E), três carros e três pedestres.

## 1. Modelo em três camadas

| Camada | O que é | Onde está |
|---|---|---|
| **Mapa** (estático) | Calçadas, pistas, canteiro, retorno, acesso, faixas, posição dos semáforos | objeto `MAPA` (`trechos`, `objetos`) |
| **Entidades** (dinâmicas) | Carros e pedestres que se movem | listas `cars` e `peds` |
| **Controlador** (lógica) | Ciclo que decide a cor de cada sinal | função `luzes(t)` |

A cada passo de tempo o programa atualiza o controlador, depois os carros e pedestres, e por fim redesenha tudo em um `<canvas>`.

## 2. Sistema de coordenadas

- Grade de **21 × 12 células** (`x` = 0..20, `y` = 0..11), origem no canto superior esquerdo.
- `pos_dim = [x, y, largura, altura]` em células.
- `pos`, `to`, `via` de uma rota são células; o centro da célula é `+0.5`.
- Cada célula é desenhada com 50 px.

```
y 0-1   calçada
y 2-4   pista OESTE (topo, carros vão para x=0)
y 5-6   canteiro (retorno em x=10..12)
y 7-9   pista LESTE (baixo, carros vão para x=20)
y 10-11 calçada (acesso em x=1..3)
```

Os trechos são pintados **na ordem da lista**; o último pinta por cima (por isso `pista_aces` vem depois da `calcada` de baixo).

## 3. Os sinais

| Sinal | Posição | Função | Regra |
|---|---|---|---|
| **A** | (2, 9) | Carros que **saem do acesso** (`carro_4`) | Segue o ciclo dos carros: verde 0–8 s |
| **B** | (1, 7) | Carros da **pista de baixo** em x ≈ 1 (`carro_2`, `carro_3`) | **Oposto de A**: verde só quando A está vermelho (+1 s de folga) |
| **C** | (17, 8) | Pista de baixo (leste), antes da faixa DC | **Assíncrono**: fica verde e só fecha quando um pedestre pede (ver 3.1). Fora do ciclo de 20 s |
| **D** | (11, 6) | Saída do retorno para a pista de topo | **Oposto de E**: abre quando E fecha. **Não depende de C** |
| **E** | (17, 4) | Pista de cima (oeste), antes da faixa ED | Segue o ciclo dos carros |
| **P** | pontas das faixas | Semáforos de pedestre | Verde / piscando / vermelho |

Abaixo da tela há uma **flag por sinal** (A, B, C, D, E, P) com a cor atual e o nome do estado. Elas atualizam a cada quadro.

### Ciclo de 20 s

| Tempo (s) | A / E | B | D | P (pedestres ED e AB) |
|---|---|---|---|---|
| 0 – 8 | verde | vermelho | vermelho | vermelho |

| 8 – 10 | amarelo | vermelho | vermelho | vermelho |
| 10 – 11 | vermelho | vermelho | verde | **verde** |
| 11 – 16 | vermelho | verde | verde | **verde** |
| 16 – 18 | vermelho | verde | verde | **piscando** |
| 18 – 20 | vermelho | verde | vermelho | vermelho |

Observações:
- **B nunca fica verde junto com A**; entre os dois há 1 s de tudo vermelho (10–11 s), para o carro do acesso terminar de entrar na pista (testado: 0 violações em 1 h simulada).
- **D abre no instante em que E fecha** (t = 10 s) e fecha 2 s depois dos pedestres terminarem.
- **P piscando** = quem já está na faixa termina de atravessar; quem espera **não** entra.
- O intervalo 18–20 s é "tudo vermelho": limpa as faixas antes de reabrir para os carros.

### 3.1 Semáforo C: assíncrono, sob pedido

C **não faz parte do ciclo de 20 s**. Tem uma máquina de estados própria (`stepC`), disparada por um botão:

```
verde ──(pedido && já passaram 4 s)──▶ amarelo 2 s ──▶ vermelho 1 s (limpa)
  ▲                                                          │
  │                                                          ▼
vermelho 1 s ◀── piscando 2 s ◀── pedestre verde 6 s ◀───────┘
```

- Em repouso C fica **verde** e os carros da pista de baixo passam livres.
- O **pedestre 3** aperta o botão ao chegar na borda da faixa DC com o sinal fechado. O botão (laranja) acende nas duas pontas da faixa e a flag de C mostra `pedido ✋`.
- Há um **verde mínimo de 4 s** antes de atender, para o trânsito não ficar travado por pedidos em sequência.
- Pedido feito durante o amarelo ou a travessia é atendido: o botão apaga quando o pedestre ganha o verde. Pedido feito depois da travessia espera o próximo ciclo.
- O sinal de pedestre da faixa DC é separado (`pedC`, flag **PC**). As faixas ED e AB continuam no ciclo de 20 s (flag **P**).
- Carros também param se ainda houver pedestre dentro da faixa, mesmo com C verde.
- **D não depende de C** (só de E).
- O pedestre 3 espera 8–16 s em cada calçada (`pausa`), por isso C fecha só de tempos em tempos.

As cores do ciclo vêm de `luzes(t)`; as de C vêm de `estados()`; o mapa letra → estado está em `LUZ_DE`:

```js
const LUZ_DE = {A:'carro', B:'oposto', C:'carroC', D:'retorno', E:'carro'};
```

## 4. Carros

Rotas definidas em `MAPA.rotas`. Cada rota vira uma **polilinha** (`pos → via… → to`), estendida 1,5 célula nas pontas para o carro nascer e sumir fora da tela.

| Rota | Caminho | Para em |
|---|---|---|
| `carro_1` | pista de topo, x 21 → 0 | linha em x = 18,1, obedece **E** e faixa ED |
| `carro_2` | pista de baixo, x 0 → 21 | linha em x = 0,95 (**B**) e linha em x = 16,9 (**C**, faixa DC) |
| `carro_3` | pista de baixo até x = 11, sobe pelo retorno, volta pelo topo até x = 0 | linha em x = 0,95 (**B**) e linha em y = 5,7 (**D**) |
| `carro_4` | sai do acesso (x = 2,5, de baixo para cima), cruza a faixa AB e entra na pista de baixo rumo a x = 21 | linha em y = 11,2 (**A**), antes da faixa AB |

Uma rota pode ter **várias linhas de parada** (`parar` é uma lista).

Cada carro guarda a distância `s` percorrida na sua polilinha e uma velocidade `v`. Em cada passo ele calcula uma **folga** (`gap`), a distância livre à frente, como o **mínimo** de:

1. **Linha de parada**, se o sinal está vermelho, **ou** há pedestre na faixa, **ou** (para `carro_3`) há carro do topo na zona de cruzamento, **ou** o sinal está amarelo e ainda dá tempo de frear.
2. **Carro à frente** na mesma direção (a menos de 0,5 célula de distância lateral).

Depois a velocidade tende a `min(VMAX, √(2·DEC·folga))` com aceleração limitada. Isso gera frenagem suave e filas sem sobreposição. A luz de freio acende quando o carro está freando ou parado.

Regras extras:
- Se o carro já passou a linha de parada, ignora o sinal (não para no meio da faixa).
- Carro **parado** diante do amarelo continua parado (só passa no amarelo quem não consegue frear).
- **Acesso × pista:** A verde ⇒ B vermelho. Os carros da pista esperam em B enquanto o `carro_4` entra. Como reforço, o `carro_4` também espera se ainda houver carro da pista em x ∈ [0,9; 4,5].
- No amarelo, o carro só passa se não consegue frear antes da linha.
- `carro_3` cede passagem aos carros do topo (zona x ∈ [9, 17,9]); os carros do topo ignoram `carro_3` enquanto ele sobe.
- Pedestre também espera se houver **carro dentro da faixa** antes de entrar.
- Novos carros só nascem se não houver outro a menos de 2,2 células do ponto de entrada.

## 5. Pedestres

| Pedestre | Trajeto | Faixa |
|---|---|---|
| `pedestre_1` | (0,5; 10,5) ↔ (4,5; 10,5), cruza o acesso | `faixa_AB` |
| `pedestre_2` | calçada de cima ↔ canteiro, x ≈ 17,3 | `faixa_ED` |
| `pedestre_3` | canteiro ↔ calçada de baixo, x ≈ 17,3 | `faixa_DC` |

Vão e voltam em loop, esperando 1,5–3,5 s em cada ponta. Antes de entrar na faixa, só avançam se **P = verde**; caso contrário ficam parados na borda. Velocidade: 1,2 célula/s (cruzar 3 células leva ≈ 2,5 s, dentro da janela de 6 s de verde).

## 6. Laço principal

```
a cada quadro:
    dt = tempo real × velocidade escolhida
    divide dt em passos de 0,025 s            (estabilidade)
    para cada passo:
        t += dt
        L = luzes(t)                          (estado de todos os sinais)
        gera carros novos (timer por rota)
        move carros   (linha de parada, fila, aceleração)
        move pedestres (espera verde antes da faixa)
    desenha mapa → faixas → semáforos → carros → pedestres
    atualiza flags
```

## 7. Controles

- **Pausar / Continuar** e **Reiniciar**.
- **Velocidade** de 0,5× a 4×.
- Linha de status: tempo total, posição no ciclo e fase atual.

## 8. Como alterar

| Quero… | Mexo em |
|---|---|
| Mudar tempos do ciclo | `luzes(t)` e `CICLO` |
| Mudar tempos de C (sob demanda) | `MIN_VERDE`, `SEQ_C` |
| Pedestre pedir com mais/menos frequência | `pausa` da rota do pedestre |
| Mudar quem segue quem | `luzes(t)` (novos estados) e `LUZ_DE` |
| Mudar o mapa | `MAPA.trechos` / `MAPA.objetos` |
| Nova rota de carro | `MAPA.rotas` (`pos`, `to`, `via`, `parar`) |
| Carros mais rápidos / freio | `VMAX`, `ACC`, `DEC` |
| Velocidade dos pedestres | `PV` |

## 9. Pontos em aberto

- Posição dos semáforos é só visual: a linha de parada de cada rota é definida em `parar.pt`, não pela posição do desenho.
- O mapa é espelho do YAML escrito à mão em JS; a animação não lê o arquivo YAML.
- Os carros viram nas curvas com rotação suavizada, não com raio real.
