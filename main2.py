# /*******************************************************************************
# Autor: Matheus Silva Rodrigues
# Componente Curricular: MI Algoritmos
# Concluido em: 29/10/2024
# Declaro que este código foi elaborado por mim de forma individual e não contém nenhum
# trecho de código de outro colega ou de outro autor, tais como provindos de livros e
# apostilas, e páginas ou documentos eletrônicos da Internet. Qualquer trecho de código
# de outra autoria que não a minha está destacado com uma citação para o autor e a fonte
# do código, e estou ciente que estes trechos não serão considerados para fins de avaliação.
# SO utilizado: Windows 10
# Bibliotecas utilizadas: CURSES, RANDOM e TIME
# ******************************************************************************************/

import curses
import random
import time

# Tabuleiro Tetris
tabtetris = [['⬜' for _ in range(10)] for _ in range(20)]

# Definição das peças
I = [["🟥", "🟥", "🟥", "🟥"]]
T = [["🟥", "🟥", "🟥"],
     [" ", "🟥", " "]]
O = [["🟥", "🟥"],
     ["🟥", "🟥"]]
S = [[" ", "🟥", "🟥"],
     ["🟥", "🟥", " "]]
Z = [["🟥", "🟥", " "],
     [" ", "🟥", "🟥"]]
J = [["🟥", " ", " "],
     ["🟥", "🟥", "🟥"]]
L = [[" ", " ", "🟥"],
     ["🟥", "🟥", "🟥"]]
BMB = [["💣"]]
letras = [I, T, O, S, Z, J, L, BMB]

def print_tabtetris(stdscr, pontos):
    stdscr.clear()
    for linha in tabtetris:
        stdscr.addstr("".join(linha) + "\n")
    stdscr.addstr("Pontuação: {}\n".format(pontos))
    stdscr.refresh()

def colocar_letra(letra, linha, coluna):
    for i in range(len(letra)):
        for j in range(len(letra[i])):
            if letra[i][j] == "🟥" and 0 <= linha + i < 20 and 0 <= coluna + j < 10:
                tabtetris[linha + i][coluna + j] = "🟥"

def limpar_letra(letra, linha, coluna):
    for i in range(len(letra)):
        for j in range(len(letra[i])):
            if letra[i][j] == "🟥" and 0 <= linha + i < 20 and 0 <= coluna + j < 10:
                tabtetris[linha + i][coluna + j] = "⬜"

def verificar_colisao(letra, linha, coluna):
    for i in range(len(letra)):
        for j in range(len(letra[i])):
            if letra[i][j] == "🟥":
                if linha + i >= 20 or coluna + j < 0 or coluna + j >= 10 or tabtetris[linha + i][coluna + j] == "🟥":
                    return True
    return False

def rotacionar_letra(letra):
    return [list(reversed(col)) for col in zip(*letra)]

def remover_linhas_completas():
    linhas_removidas = 0
    nova_tabtetris = [linha for linha in tabtetris if not all(celula == "🟥" for celula in linha)]
    linhas_removidas = 20 - len(nova_tabtetris)

    while len(nova_tabtetris) < 20:
        nova_tabtetris.insert(0, ['⬜' for _ in range(10)])

    for i in range(20):
        tabtetris[i] = nova_tabtetris[i]

    return linhas_removidas

def atualizar_pontuacao(linhas_removidas):
    return linhas_removidas * 100

def game_over(letra, linha, coluna):
    return verificar_colisao(letra, linha, coluna)

def jogartetris(stdscr):
    pontos = 0
    letra_atual = random.choice(letras)
    linha_atual = 0
    coluna_atual = 3
    tempo_descida = time.time()  # Controle de tempo para descida automática
    curses.curs_set(0)
    stdscr.nodelay(True)

    while True:
        print_tabtetris(stdscr, pontos)

        # Limpar a posição anterior
        limpar_letra(letra_atual, linha_atual, coluna_atual)

        # Verificar o tempo para descer automaticamente a peça
        if time.time() - tempo_descida > 0.5:
            linha_atual += 1
            tempo_descida = time.time()  # Resetar o temporizador de descida

        # Checar colisão após descer
        if verificar_colisao(letra_atual, linha_atual, coluna_atual):
            linha_atual -= 1  # Corrigir posição
            colocar_letra(letra_atual, linha_atual, coluna_atual)
            linhas_removidas = remover_linhas_completas()
            pontos += atualizar_pontuacao(linhas_removidas)

            # Checar se é Game Over após colocar a letra
            letra_atual = random.choice(letras)
            linha_atual = 0
            coluna_atual = 3

            # Verifica colisão com a nova letra
            if verificar_colisao(letra_atual, linha_atual, coluna_atual):
                stdscr.addstr(22, 0, "GAME OVER")
                stdscr.refresh()
                stdscr.nodelay(False)
                stdscr.getch()
                break

        # Controle do jogador
        key = stdscr.getch()
        if key == ord('d') and not verificar_colisao(letra_atual, linha_atual, coluna_atual + 1):
            coluna_atual += 1
        elif key == ord('a') and not verificar_colisao(letra_atual, linha_atual, coluna_atual - 1):
            coluna_atual -= 1
        elif key == ord('w'):
            nova_letra = rotacionar_letra(letra_atual)
            if not verificar_colisao(nova_letra, linha_atual, coluna_atual):
                letra_atual = nova_letra

        # Colocar a peça no tabuleiro
        colocar_letra(letra_atual, linha_atual, coluna_atual)

        # Pequeno delay para o loop, para garantir que o programa não consuma CPU excessivamente
        curses.napms(50)

def menu(stdscr):
    while True:
        stdscr.clear()
        stdscr.addstr("Bem-vindo ao Tetris\n")
        stdscr.addstr("Pressione 1 para iniciar o jogo\n")
        stdscr.addstr("Pressione 0 para sair\n")
        stdscr.refresh()
        
        key = stdscr.getch()
        if key == ord('1'):
            jogartetris(stdscr)
        elif key == ord('0'):
            print("Programa encerrado. Até logo!")
            break

if __name__ == "__main__":
    curses.wrapper(menu)
