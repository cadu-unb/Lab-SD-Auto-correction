# Diagramas de estados — simulação de semáforos

Complemento de [`FUNCIONAMENTO.md`](FUNCIONAMENTO.md). Cada diagrama espelha o código de [`semaforos.html`](semaforos.html).
Os blocos `mermaid` renderizam no GitHub e no preview do VS Code (extensão *Markdown Preview Mermaid Support*).

O sistema são **4 máquinas de estado** rodando em paralelo:

| # | Máquina | Gatilho | Controla |
|---|---|---|---|
| 1 | Ciclo fixo de 20 s | tempo | A, B, D, E e pedestres das faixas ED e AB |
| 2 | Semáforo C | botão do pedestre | C e pedestre da faixa DC |
| 3 | Carro | sinais, faixas, outros carros | cada veículo |
| 4 | Pedestre | sinal de pedestre, carros na faixa | cada pedestre |

---

## 1. Ciclo fixo de 20 s (A, B, D, E, P)

`t` = tempo dentro do ciclo. O ciclo reinicia sozinho (`t mod 20`).

```mermaid
stateDiagram-v2
    direction LR
    [*] --> F1

    F1 : F1 · 0 a 8 s
    F1 : A e E verde
    F1 : B vermelho · D vermelho
    F1 : P vermelho

    F2 : F2 · 8 a 10 s
    F2 : A e E amarelo
    F2 : B vermelho · D vermelho
    F2 : P vermelho

    F3 : F3 · 10 a 11 s
    F3 : A e E vermelho
    F3 : B vermelho · D verde
    F3 : P verde

    F4 : F4 · 11 a 16 s
    F4 : A e E vermelho
    F4 : B verde · D verde
    F4 : P verde

    F5 : F5 · 16 a 18 s
    F5 : A e E vermelho
    F5 : B verde · D verde
    F5 : P piscando

    F6 : F6 · 18 a 20 s
    F6 : A e E vermelho
    F6 : B verde · D vermelho
    F6 : P vermelho

    F1 --> F2 : t = 8
    F2 --> F3 : t = 10
    F3 --> F4 : t = 11
    F4 --> F5 : t = 16
    F5 --> F6 : t = 18
    F6 --> F1 : t = 20 reinicia
```

Invariantes (testados em 1 h simulada):
- **B nunca verde junto com A** (B é o oposto de A, com 1 s de folga em F3).
- **D abre quando E fecha** (F3) e **não depende de C**.
- Pedestre só entra na faixa em **P verde**; em **P piscando** só termina quem já está dentro.

---

## 2. Semáforo C — assíncrono, sob pedido

Fora do ciclo de 20 s. Em repouso fica verde; só fecha se um pedestre apertar o botão.

```mermaid
stateDiagram-v2
    [*] --> Verde

    Verde : C verde
    Verde : carros da pista de baixo passam
    Verde : PC vermelho

    Amarelo : C amarelo · 2 s
    Amarelo : PC vermelho

    Limpa1 : C vermelho · 1 s
    Limpa1 : PC vermelho
    Limpa1 : esvazia a faixa

    PedVerde : C vermelho · 6 s
    PedVerde : PC verde
    PedVerde : pedido atendido, botão apaga

    Piscando : C vermelho · 2 s
    Piscando : PC piscando

    Limpa2 : C vermelho · 1 s
    Limpa2 : PC vermelho

    Verde --> Amarelo : pedido E verde há pelo menos 4 s
    Amarelo --> Limpa1 : 2 s
    Limpa1 --> PedVerde : 1 s
    PedVerde --> Piscando : 6 s
    Piscando --> Limpa2 : 2 s
    Limpa2 --> Verde : 1 s

    note right of Verde
        pedido = pedestre chega na borda
        da faixa DC com PC não verde.
        Pedido feito fora do verde
        fica guardado para o próximo ciclo.
    end note
```

---

## 3. Carro

Vale para `carro_1` a `carro_4`. Cada carro tem uma ou mais **linhas de parada** (`parar`). Antes de cada linha ele checa os sinais e o que está à frente.

```mermaid
stateDiagram-v2
    [*] --> Andando : nasce fora da tela

    Andando --> Freando : obstáculo à frente
    Freando --> Andando : obstáculo sumiu
    Freando --> Parado : velocidade chega a zero
    Parado --> Andando : obstáculo sumiu
    Andando --> PassouLinha : frente do carro cruza a linha
    PassouLinha --> Andando : próxima linha ou fim do trajeto
    Andando --> [*] : sai da tela

    Andando : acelera até 3,2 células por s
    Freando : frenagem suave
    Parado : luz de freio acesa
    PassouLinha : ignora o sinal desta linha
```

**Obstáculo à frente** é qualquer um destes:

```mermaid
flowchart TD
    O{{"Obstáculo à frente?"}}
    O --> S1["Sinal da linha vermelho"]
    O --> S2["Sinal amarelo e o carro<br/>consegue frear, ou já está parado"]
    O --> S3["Pedestre dentro da faixa"]
    O --> S4["Zona de cruzamento ocupada<br/>por carro de outra rota (ceder)"]
    O --> S5["Outro carro à frente<br/>na mesma direção"]
```

| Rota | Linhas de parada | Cede para |
|---|---|---|
| `carro_1` (topo, oeste) | **E** + faixa ED | — |
| `carro_2` (baixo, leste) | **B** · **C** + faixa DC | — |
| `carro_3` (retorno) | **B** · **D** | `carro_1` em x de 9 a 17,9 |
| `carro_4` (acesso) | **A** + faixa AB | `carro_2` e `carro_3` em x de 0,9 a 4,5 |

---

## 4. Pedestre

Vai e volta entre dois pontos. Cada pedestre tem uma faixa e uma pausa configurável (`pausa`).

```mermaid
stateDiagram-v2
    [*] --> Pausa : nasce com atraso

    Pausa --> Caminhando : tempo de pausa acabou
    Caminhando --> NaBorda : prestes a entrar na faixa
    NaBorda --> EsperaVerde : sinal não está verde
    EsperaVerde --> NaBorda : sinal ficou verde
    NaBorda --> EsperaCarro : sinal verde mas há carro na faixa
    EsperaCarro --> NaBorda : faixa livre
    NaBorda --> Atravessando : sinal verde e faixa livre
    Atravessando --> Caminhando : saiu da faixa
    Caminhando --> Pausa : chegou ao destino e inverte o sentido

    Pausa : espera de 1,5 a 3,5 s
    Pausa : pedestre 3 espera de 8 a 16 s
    EsperaVerde : na faixa DC aperta o botão
    EsperaVerde : pedirC
    Atravessando : 1,2 células por s
    Atravessando : piscando não impede quem já entrou
```

---

## 5. Como as máquinas se conversam

```mermaid
flowchart LR
    T(("tempo t")) --> M1["1 · Ciclo 20 s"]
    BT["botão"] --> M2["2 · Semáforo C"]

    M1 -->|"A"| M3["3 · Carros"]
    M1 -->|"B, D, E"| M3
    M1 -->|"P"| M4["4 · Pedestres"]
    M2 -->|"C"| M3
    M2 -->|"PC"| M4

    M4 -->|"pedestre na borda da faixa DC"| BT
    M4 -->|"pedestre dentro da faixa"| M3
    M3 -->|"carro dentro da faixa"| M4
```

Leitura: sinais fluem das máquinas 1 e 2 para carros e pedestres. Carros e pedestres se **travam mutuamente** (carro espera pedestre na faixa; pedestre espera carro sair da faixa). Só o pedestre da faixa DC realimenta o controlador, através do botão.
