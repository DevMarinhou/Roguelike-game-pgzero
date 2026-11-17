# 🎲 Lula e o Mito — Vote 13

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Pygame Zero](https://img.shields.io/badge/Pygame%20Zero-FF0000?style=flat-square&logo=pygame&logoColor=white)](https://www.pygamezero.io/)
[![Gênero](https://img.shields.io/badge/Gênero-Roguelike-c25e00?style=flat-square)](#mecânicas)

> ⚠️ **Aviso:** esta é uma **obra de ficção e sátira**, criada como projeto de estudo de game dev. Não representa opinião política de ninguém, não tem vínculo com candidatos, partidos ou campanhas e não pretende desinformar ninguém — é só um jogo. Divirta-se com humor. 🎉

Um **roguelike de ação** em Python com a engine [Pygame Zero](https://www.pygamezero.io/): você controla o Lula e enfrenta hordas de Mito (Bolsonaro) em salas cada vez mais difíceis. Ao limpar cada sala, escolhe um **boon** (benção) para fortalecer seu personagem.

Com visuais vibrantes e "juice" de sobra — dash com invencibilidade, ataque em arco, partículas, tremores de tela e textos "13!" — o jogo é uma sátira divertida feita com muito humor.

## 🎮 Jogabilidade

| Controle | Ação |
|---|---|
| `W` `A` `S` `D` | Movimentar |
| `Espaço` | Dash rápido (com invencibilidade) |
| Clique esquerdo | Atacar na direção do cursor |
| `1` / `2` (no upgrade) | Escolher a benção correspondente |
| `Enter` / `Espaço` (no menu) | Iniciar o jogo |
| `R` (no *Game Over*) | Reiniciar |
| `M` (no *Game Over*) | Voltar ao menu |

**Objetivo:** elimine todos os inimigos da sala e vá até a **porta de saída** (que brilha) para avançar. Se a vida chegar a zero, o jogo acaba.

## ⚙️ Mecânicas

| Mecânica | Descrição |
|---|---|
| **Ataque em arco** | Golpe em cone na direção do mouse |
| **Dash** | Movimento rápido com invencibilidade temporária |
| **Sistema de vida** | Barra de HP com invencibilidade após levar dano |
| **Inimigos** | Cada sala gera inimigos com vida e velocidade crescentes |
| **Partículas e juice** | Sparks, rastros e tremores de tela para feedback |
| **Benções (boons)** | Dois upgrades aleatórios ao fim de cada sala: dano, vida, velocidade, alcance ou dash |

## 🚀 Requisitos e execução

- **Python 3.7+**
- **Pygame Zero** (instala o Pygame automaticamente)

```bash
git clone https://github.com/DevMarinhou/Roguelike-game-pgzero.git
cd Roguelike-game-pgzero
pip install pgzero
python "Lula e o mito.py"
# ou: pgzrun "Lula e o mito.py"
```

## 📁 Estrutura do código

```
├── Lula e o mito.py   # jogo completo (arquivo único, ~32 KB)
├── images/            # sprites: lula, bolsonaro, fundo da sala, arma
├── sounds/            # efeitos: ataque, acerto do jogador, acerto do inimigo
└── README.md
```

**Arquitetura:** `Player` (vida, ataque, dash), `Enemy` (perseguição, dano, knockback), `Particle` (explosões e rastros), `JuiceSystem` (shake de tela e textos) e um loop principal com estados `MENU → PLAYING → UPGRADE → GAME_OVER`.

Se algum asset estiver faltando, o jogo usa **fallbacks** (retângulos coloridos e silêncio) — nunca quebra por causa de arquivo ausente.

## 🤝 Contribuir

Issues e pull requests são bem-vindos! Sugestões de novas benções, inimigos ou mecânicas são ótimas.

## 📄 Licença

Este é um projeto de **estudo e humor** sem licença formal definida. Créditos: desenvolvimento por [DevMarinhou](https://github.com/DevMarinhou), inspirado na cultura de memes e política brasileira.

---

*Divirta-se e vote 13! 🧃🔥*
