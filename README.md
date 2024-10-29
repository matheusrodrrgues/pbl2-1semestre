# Tetris Game

Bem-vindo ao Tetris! Este é um jogo de Tetris implementado em Python usando a biblioteca `curses` para o terminal, com algumas peças especiais como uma bomba (`💣`) que adiciona uma dinâmica interessante ao gameplay.

## Informações do Projeto

- **Autor:** Matheus Silva Rodrigues
- **Componente Curricular:** MI Algoritmos
- **Data de Conclusão:** 29/10/2024
- **SO utilizado:** Windows 10
- **Bibliotecas utilizadas:** `curses`, `random`, `time`
- **Versão do Python:** 3.12.7 (64-bit)

## Descrição

Este projeto implementa o jogo Tetris, onde peças caem do topo do tabuleiro e devem ser posicionadas pelo jogador para completar linhas. Linhas completas são removidas e pontuam. Caso a peça especial "Bomba" (`💣`) seja sorteada, ela eliminará peças ao seu redor em uma área de 3x3 ao tocar no tabuleiro.

## Requisitos

- Python 3.12.7 ou superior
- Biblioteca `curses` (pré-instalada na maioria dos sistemas UNIX, como Linux e macOS; pode exigir instalação especial no Windows)
  
## Instalação e Execução

1. **Instale o Python 3.12.7** (se necessário).
2. **Instale a biblioteca `windows-curses`** (somente no Windows):
   ```bash
   pip install windows-curses
