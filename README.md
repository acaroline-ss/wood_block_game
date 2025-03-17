# wood_block_game
Este projeto busca analisar o algoritmo do Wood Block, explorando sua lógica de movimentação e remoção de blocos. Além disso, investiga a implementação de IA para otimizar jogadas, prever posicionamentos e desenvolver estratégias eficientes dentro do jogo.


Ideia geral do trabalho: ao entrar no jogo, o utilizador poderá escolher entre user mode (ele é que joga) e pc mode (a IA é que joga). Se escolher o user mode: código da Alice. Se escolher pc mode, poderá novamente escolher entre diversos métodos de pesquisa (como breadth first; depth first; A*; etc.). 
Ideias adicionais: Caso o utilizador tente colocar uma peça de uma forma que ultrapassa os limites do tabuleiro, poderá aparecer uma mensagem como  ou "The piece doesn't fit within the limits of the board, duh"
. Também podemos colocar outras mensagens insultuosas ao longo do jogo, como "Of all the options, THAT'S the search method you choose?". Além disso, poderíamos fazer com que para cada método de pesquisa sejam apresentados dados que reflitam a sua eficácia, como a rapidez com que chegou à solução, o custo associado, a memória ocupada, etc.

Chekpoints:

- Trabalho até agora desenvolvido: parte da interface e jogo em user mode;
- Bibliografia: https://www.youtube.com/watch?v=RxWS5h1UfI4; https://www.youtube.com/watch?v=TnpoBCFDo88
- Formulação do jogo como um problema de pesquisa:
      (1) Representação dos estados: matriz + coordenadas?
      (2) Estado inicial: matriz vazia
      (3) Operadores: igualar a 1 ou igualar a 0? (definir peças)
      (4) Custo de cada jogada: nº de coordenadas que se preenchem com 1s ou nº de coordenadas que passam a 0s (custo de 1 cada?)
      (5) Objetivo: acabar com uma matriz (tabuleiro) completamente vazia
      (6) Opções de Métodos de pesquisa: breathd first; depth first; cost; A*; etc.
      (7)  


Comentários da Alice do código já escrito :
1) as diferentes imports para gerir as files no main não funcionam and I DON'T KNOW WHY. - enviar mail a miriam
2) No human mode está quase tudo bom, só (EASY TO FIX, SÓ UM LEMBRETE) as pecas estão a blink weirdly e é muito sensível... - CAROL VER ISSO !!!!
3) implementar os niveis !!! (initial state, have to be able to NOT be solvable, ...)
4) PC mode não funciona por enquanto - so figure it out... + discutir com professora, do objetivo do jogo (muito complicado para os algoritmos de procura ? infinito ?).
5) review if rotation or not ??
6) the three blocks need to be used before other are porposed ???
7) implement streaks (linha effacee de suite = multiplication des points
8) supprime pas seulement les lignes mais aussi carrées 3*3 dans niveaux tableux tailles 6*6
9) placer un bloc donnes des points ?
10) points = seulement in human mode ???

Organizacao (bia)
* fazemos essa parte a mao (garantindo que tenhamos um nivel de solucao
  * matriz preenchida
  * retiramos as pecas (que serao as geradas)
  * geramos algumas dessas pecas aleatoriamente em cada jogada

* estado inicial: matriz atribuida da 1 fase
* operadores: pecas disponibilizadas
* estado final: matriz vazia

* NIVEIS:
  * nivel 1: 4X4 (MENOS PECAS RETIRADAS E MENOS PROXIMAS)
  * nivel 2: 5x5 (mais pecas retiradas e mais proximas
  * nivel 3: 6x6 (ainda mais pecas retiradas e ainda mais pecas proximas


