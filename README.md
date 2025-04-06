# Wood_block_game
* Este projeto foi desenvolvido no âmbito da unidade curricular de EIACD (Elementos de Inteligência Artificial e Ciência de Dados), sob orientação dos professores Luís Paulo Reis e Miriam Santos.
* O jogo Wood Block é um puzzle de estratégia e raciocínio espacial, inspirado em clássicos como o Tetris e o Blokus.
* O objetivo principal é posicionar peças de madeira num tabuleiro limitado, sem sobreposições, até preencher todo o espaço disponível.
* Regras básicas:
  * Cada jogador recebe peças com formatos geométricos diferentes.
  * As peças devem ser colocadas de forma a maximizar o espaço ocupado e evitar bloqueios futuros.
  * O jogo termina o tabuleiro é completamente preechido pelas peças disponíveis e forma uma matriz vazia.
 <img width="692" alt="Captura de Tela 2025-04-06 às 12 32 06" src="https://github.com/user-attachments/assets/38851a86-5502-4b6f-b2e7-31f24cb7136f" />

<img width="407" alt="Captura de Tela 2025-04-06 às 12 40 32" src="https://github.com/user-attachments/assets/04d09c48-f8f5-49e1-bb6b-876d62893f35" />

# Descrição
* Este projeto desenvolveu um algoritmo para o jogo Wood Block, implementando diferentes métodos de pesquisa de IA.
* Funcionalidades:
  * 👤 Modo Jogador: O jogador escolhe o movimento das peças manualmente
  * 🤖 Modo IA: Escolha entre algoritmos:
     * Breadth-First (BFS)
     * Depth-First (DFS)
     * A*
     * Greedy Search
  * Computer Assistent Mode: A IA fornece dicas ao jogador do posicionamento estrategico das peças
* Objetivos:
  * Simular o Wood Block com IA
  * Comparar eficiência dos algoritmos

 # Dependências
 * Este projeto requer as seguintes dependências:
   * Python ou Anaconda
   * Pygame
* Biblotecas usadas
  * import pygame: desenha os recursos gráficos.
  * import random: Gera números aleatórios e seleções aleatórias.
  * import time: Controlar tempo, velocidade e pausas no jogo.
  * import os: Gerenciar arquivos/pastas.
  * import sys: Acessa parâmetros e funções específicas do sistema

# Iniciando o jogo
* **Passo 1 - Certifique-se de ter o VS code instalado**
  
* **Passo 2 - Para iniciar o jogo é necessário ter algum interpretador python em sua máquina. Ex: python ou anaconda**
  * Acesse o site oficial: https://www.python.org/downloads/
  * Clique em "Download Python 3.x.x" (versão mais recente, ex: 3.12). O Windows/macOS/Linux serão detectados automaticamente.
  * Localize o arquivo baixado (ex: python-3.12.1-amd64.exe) e dê duplo clique.
  * Na primeira tela:
     * ✅ Marque a opção "Add python.exe to PATH" (CRUCIAL para rodar Python no CMD).
     * ✅ Recomendado: Selecione "Install Now" (instalação padrão para usuários iniciantes).
  * Clique em "Install" > Aguarde a conclusão (> barra de progresso azul).
* **Passo 3 - Instalar o pygame**
  * No Prompt de Comando , digite:
    ```bash
    pip install pygame
    ```
* **Passo 3 - Clonar o repósitório do projeto no seu VS Code**
  * No terminal do seu VS code, digite:
    ```bash
    git clone https://github.com/acaroline-ss/wood_block_game.git
    ```
* **Passo 4 - Abrir o jogo**
  * Para iniciar o jogo, navegue até o diretório que contém o arquivo **main.py** e execute o seguinte comando no terminal:
    ```bash
    python main.py
    ```
  * Obs: Este comando pode variar dependendo do interpretador ou versão que o utilizador estiver usando. Ex: Se estiver usando Python 3 e o comando acima não funcionar, tente:
    ```bash
    python3 main.py
    ```
  # Team T1B_G9
  * Alice de Azevedo Silva
  * Ana Caroline Soares Silva
  * Beatriz Morais Vieira
