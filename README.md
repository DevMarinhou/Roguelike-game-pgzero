Lula e Mito — Vote 13

Um jogo de ação roguelike com temática política brasileira, desenvolvido em Python com a engine Pygame Zero.

Você controla o Lula e precisa enfrentar hordas de Mito (Bolsonaro) em salas cada vez mais difíceis. Ao limpar cada sala, escolhe um boon (benção) para fortalecer seu personagem. O jogo é uma sátira divertida, com visuais vibrantes e mecânicas de dash, ataques em arco e sistema de partículas.

Jogabilidade

· Movimentação: WASD para andar.
· Dash: Espaço para dar um dash rápido (com invencibilidade).
· Ataque: Clique com o botão esquerdo do mouse para atacar na direção do cursor.
· Objetivo: Elimine todos os inimigos da sala, depois vá até a porta de saída (que brilha) para avançar.
· Upgrades: Ao limpar uma sala, escolha entre duas benções que aumentam dano, vida, velocidade, alcance ou dash.
· Game Over: Se a vida do Lula chegar a zero, o jogo acaba. Você pode recomeçar ou voltar ao menu.


Mecânicas Principais

Mecânica Descrição
Ataque em arco Golpe em cone na direção do mouse.
Dash Movimento rápido com invencibilidade temporária.
Sistema de vida Barra de HP com invencibilidade após levar dano.
Inimigos Cada sala gera inimigos com vida e velocidade crescentes.
Partículas e Juice Efeitos visuais (sparks, rastros, tremores de tela) para feedback.
Benções (Boons) Escolha entre dois upgrades aleatórios ao final de cada sala.

Requisitos

· Python 3.7 ou superior
· Pygame Zero (pgzero)
· Pygame (instalado automaticamente com pgzero)


Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/DevMarinhou/Roguelike-game-pgzero
   cd Roguelike-game-pgzero
   ```
2. Instale as dependências:
   ```bash
   pip install pgzero
   ```
3. Certifique-se de que os arquivos de imagem e som estão no diretório correto (veja a seção Assets abaixo).
4. Execute o jogo:
   ```bash
   python Lula e o mito.py
   ```
   ou, se preferir:
   ```bash
   pgzrun Lula e o mito.py
   ```

Assets Necessários

O jogo espera os seguintes arquivos na pasta images/ e sounds/ (ou no mesmo diretório, dependendo da configuração do Pygame Zero):

· Imagens:
  · bg_sala.png — fundo da sala.
  · lula.png — sprite do jogador (recomendado ~82x84).
  · bolsonaro.png — sprite do inimigo (recomendado ~72x74).
  · cane.png — sprite da arma (bengala).
· Sons (opcional, mas recomendado):
  · player_hit.wav / .ogg
  · player_attack.wav
  · enemy_hit.wav

Se algum arquivo estiver faltando, o jogo usa fallbacks (sem som ou com retângulos coloridos).

Dica: Você pode substituir os sprites por seus próprios desenhos, mantendo as proporções aproximadas.


Controles

Tecla / Ação Função
W A S D Movimentar
Espaço Dash
Clique esquerdo Atacar na direção do mouse
1 ou 2 (no menu de upgrade) Escolher a benção correspondente
R (no Game Over) Recomeçar o jogo
M (no Game Over) Voltar ao menu principal
Enter / Espaço (no menu) Iniciar o jogo

Estrutura do Código

· Player: classe do jogador (vida, ataque, dash, animações).
· Enemy: classe dos inimigos (perseguição, dano, knockback).
· Particle: sistema de partículas para explosões e rastros.
· JuiceSystem: gerenciador de shake de tela e textos "13!".
· Loop principal com estados: MENU, PLAYING, UPGRADE, GAME_OVER.

Contribuição

Sinta-se à vontade para abrir issues ou pull requests. Sugestões de novas benções, inimigos ou mecânicas são bem-vindas!

Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

Créditos

· Desenvolvimento: DevMarinhou
· Inspiração: Cultura de memes e política brasileira (com muito humor).

Divirta-se e Vote 13! 🧃🔥
