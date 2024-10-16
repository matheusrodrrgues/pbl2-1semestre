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
BMB = ["💣"]
letras = [I, T, O, S, Z, J, L, BMB]

def print_tabtetris(stdscr, pontos):
    stdscr.clear()
    stdscr.addstr("Pontuação: {}\n".format(pontos))
    for linha in tabtetris:
        stdscr.addstr("".join(linha) + "\n")
    stdscr.refresh()

def colocar_letra(letra, linha, coluna):
    for i in range(len(letra)):
        for j in range(len(letra[0])):
            if letra[i][j] == "🟥" and 0 <= linha + i < 20 and 0 <= coluna + j < 10:
                tabtetris[linha + i][coluna + j] = "🟥"

def limpar_letra(letra, linha, coluna):
    for i in range(len(letra)):
        for j in range(len(letra[0])):
            if letra[i][j] == "🟥" and 0 <= linha + i < 20 and 0 <= coluna + j < 10:
                tabtetris[linha + i][coluna + j] = "⬜"

def verificar_colisao(letra, linha, coluna):
    for i in range(len(letra)):
        for j in range(len(letra[0])):
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
    curses.curs_set(0)
    stdscr.nodelay(1)

    # Mostrar o tabuleiro pela primeira vez
    print_tabtetris(stdscr, pontos)

    while True:
        time.sleep(0.3)

        # Limpar a posição anterior
        limpar_letra(letra_atual, linha_atual, coluna_atual)

        # Movimento para baixo
        linha_atual += 1
        if verificar_colisao(letra_atual, linha_atual, coluna_atual):
            linha_atual -= 1
            colocar_letra(letra_atual, linha_atual, coluna_atual)
            linhas_removidas = remover_linhas_completas()
            pontos += atualizar_pontuacao(linhas_removidas)

            # Checar se é Game Over
            letra_atual = random.choice(letras)
            linha_atual = 0
            coluna_atual = 3
            
            # Checar se a nova letra pode ser colocada
            if game_over(letra_atual, linha_atual, coluna_atual):
                stdscr.addstr(22, 0, "GAME OVER")
                stdscr.refresh()
                time.sleep(2)
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

        colocar_letra(letra_atual, linha_atual, coluna_atual)
        print_tabtetris(stdscr, pontos)  # Atualizar o tabuleiro após cada movimento

if __name__ == "__main__":
    curses.wrapper(jogartetris)
