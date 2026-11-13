# Laboratório de Sistemas Digitais — Experimento 07

## Objetivos

- Projetar e implementar uma máquina de estados síncrona Moore em VHDL e simular no ModelSim.

## Instruções

- O experimento deve ser realizado utilizando o ModelSim;
- Cada experimento será avaliado por meio do relatório técnico e dos códigos submetidos pelo aluno, por meio da plataforma Aprender. Os códigos devem ser submetidos comprimidos em um único arquivo.
- A sua simulação deve incluir o arquivo vhdl contendo a entidade (*entity*), a arquitetura (*architecture*) do circuito e o arquivo vhdl do *test bench* desenvolvido para simulá-los Conforme descrito no guia de uso, o seu relatório deve conter os códigos, as telas de compilação e simulação do ModelSim e as formas de ondas obtidas com a simulação.
- O relatório é individual e receberá uma nota de 0 a 10, considerando os seguintes aspectos:
  - Documentação do código, contida no relatorio (pdf) e no codigo vhdl- 20% da nota do projeto;
  - Compilação do código, apresentada no relatorio do projeto econfirmado pelo codigo vhd -10% da nota do projeto;
  - Simulação do código, apresentada no relatório do projeto econfirmado pelo codigo vhd - 70% da nota do projeto.
- Os códigos VHDL das entidades e arquiteturas desenvolvidas neste experimento e no experimento anterior serão utilizadas em experimentos futuros para construir sistemas mais complexos.

## Questão 01

Implementar em VHDL e simular no ModelSim uma máquina de estado síncrona do tipo Moore para controlar uma máquina de refrigerantes que aceita moedas de R$ 0,25 e R$ 0,50. A cada transição do clock, a máquina deve contar o dinheiro inserido e liberar o refrigerante (e o troco) assim que a soma totalizar ou exceder R$ 1,00. A máquina deve aceitar qualquer combinação de moedas de R$ 0,25 e R$ 0,50, independentemente da ordem em que as moedas foram inseridas. A qualquer momento (desde que a contagem ainda não tenha alcançado R$ 1,00) o usuário poderá cancelar a compra e a máquina deve, também na transição do clock, devolver a quantia inserida.

Considere que a máquina só dispõe de um sabor de refrigerante (ou que a escolha do refrigerante é feita antes da máquina de estados iniciar). Logo, o refrigerante é liberado automaticamente (mas na transição do clock) após a inserção do valor de R$ 1,00 com ou sem troco, não sendo necessário pressionar nenhum botão após a inserção do montante para receber o refrigerante. Isto impede a possibilidade, por exemplo, da inserção do valor de R$ 1,50.

A entidade VHDL deverá ter como entrada um vetor A de 2 bits que indicará se foi inserida uma moeda de R$ 0,25 (se A = 01), se foi inserida uma moeda de R$ 0,50 (se A = 10), se foi solicitada o cancelamento da compra (se A = 11) ou se não houve nenhuma ação por parte do usuário (se A = 00).

Deverá ter como entrada também um clock de 1 bit que fará com que a máquina leia as entradas e mude (ou não) o estado e as saídas. A leitura das entradas, assim como a mudança de estado e das saídas, deverá acontecer exclusivamente na borda de subida do clock.

A entidade VHDL deverá ter três saídas de 1 bit cada que indicarão, respectivamente, se a máquina liberou (ou não) um refrigerante, devolveu (ou não) uma moeda de R$ 0,25 e(ou) devolveu (ou não) uma moeda de R$ 0,50.

Na estrutura `process` que descreve a lógica dos registradores (memória da máquina de estados), inclua uma condição de “reset” (associada a uma entrada da entidade, ligada a um botão ou a uma chave do kit de desenvolvimento) que leve, de forma assíncrona (isto é, independentemente do sinal de clock) a máquina de estados de volta ao estado inicial. Isto facilitará o processo de teste da máquina implementada. Um exemplo deimplementação de condição de “reset” é mostrada no documento tutorial fornecido em conjunto a este roteiro.

## Dicas

1. Antes de começar, certifique-se de que você sabe a diferença entre uma máquina de estados do tipo Moore e uma do tipo Mealy.
2. Em cada estado, haverá quatro possíveis combinações de entrada que devem ser consideradas: inseriu 25 centavos, inseriu 50 centavos, solicitou cancelamento da compra ou não fez nenhuma ação. Assim, para cada estado, haverá até quatro transições possíveis. Ao elaborar o diagrama de estados, lembre-se de considerar todas as quatro possibilidades em cada um dos vários estados!
3. Note que, após a liberação do refrigerante e(ou) devolução de moedas, nem sempre a máquina retornará ao estado inicial.
   1. Imagine que, na transição do clock, o usuário solicitou o cancelamento da compra, levando a máquina ao estado que indica a devolução de R$ 0,75; é possível que, na próxima transição do clock, o usuário já esteja inserindo uma moeda de R$ 0,50. Neste caso, a máquina de estados não deve retornar ao estado inicial, mas sim ir direto ao estado que indica que a quantia inserida alcançou R$ 0,50.
   2. Entretanto, se a máquina liberou o refrigerante e(ou) devolveu moedas e, na próxima transição do clock, o usuário não inseriu moedas, ou então se ele solicitou um novo cancelamento de compra, a máquina deve sim retornar ao estado inicial. Pois, se a máquina permanecesse no mesmo estado, isso significaria liberar mais refrigerante (ou devolver mais moedas) indevidamente.
4. Seguindo estas especificações e dicas, é possível implementar a máquina com somente 9 estados.
