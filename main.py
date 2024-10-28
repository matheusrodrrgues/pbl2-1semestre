# /*****************************************************************************************/
# Autor: Matheus Silva Rodrigues
# Componente Curricular: MI Algoritmos
# Concluido em: 29/10/2024
# Declaro que este código foi elaborado por mim de forma individual e não contém nenhum
# trecho de código de outro colega ou de outro autor, tais como provindos de livros e
# apostilas, e páginas ou documentos eletrônicos da Internet. Qualquer trecho de código
# de outra autoria que não a minha está destacado com uma citação para o autor e a fonte
# do código, e estou ciente que estes trechos não serão considerados para fins de avaliação.
# ******************************************************************************************/
# SO utilizado: Windows 10
# Bibliotecas utilizadas: CURSES, RANDOM e TIME
# NÃO FUNCIONA EM CAPSLOOK
# Versão do Python: 3.12.7 em 64-bit
# ******************************************************************************************/

import curses  # biblioteca utilizada para mover e rotacionar as peças
import random  # biblioteca utilizada para sortear as peças ao descer
import time    # biblioteca utilizada para otimizar o tempo

# Tabuleiro Tetris
tabtetris = [['⬜' for _ in range(10)] for _ in range(20)]

# Definição das peças, onde cada peça tem uma formação padrão
I = [["🟥", "🟥", "🟥", "🟥"]]
T = [["🟥", "🟥", "🟥"], [" ", "🟥", " "]]
O = [["🟥", "🟥"], ["🟥", "🟥"]]
S = [[" ", "🟥", "🟥"], ["🟥", "🟥", " "]]
Z = [["🟥", "🟥", " "], [" ", "🟥", "🟥"]]
J = [["🟥", " ", " "], ["🟥", "🟥", "🟥"]]
L = [[" ", " ", "🟥"], ["🟥", "🟥", "🟥"]]
BMB = [["💣"]]

# Variável que armazena as as peças em formato de letra, para randomiza-las depois
letras = [I, T, O, S, Z, J, L, BMB]

# Essa função inicializa o tabuleiro e apresenta a pontuação
# A cada peça que caí, o tabuleiro reinicia em loop automático
def print_tabtetris(stdscr, pontos):
    stdscr.clear()
    # Imprime o tabuleiro do Tetris
    for linha in tabtetris:
        stdscr.addstr(''.join(linha) + '\n')
    
    stdscr.addstr("SCORE: {}\n".format(pontos))
    stdscr.addstr("\n")
    #Menu com os controles do jogo
    stdscr.addstr("Manual:\n")
    stdscr.addstr("CLIQUE [A] PARA MOVER PARA A ESQUERDA\n")
    stdscr.addstr("CLIQUE [D] PARA MOVER PARA A DIREITA\n")
    stdscr.addstr("CLIQUE [W] PARA GIRAR A PEÇA\n")
    stdscr.addstr("CLIQUE [S] PARA DESCER MAIS RÁPIDO\n")
    stdscr.addstr("AVISO: NÃO PRESSIONE AS TECLAS FIXAMENTE.\n")

    stdscr.refresh()

# Essa função inicializa a letra, sempre em loop, descendo uma linha e uma coluna1111
def colocar_letra(letra, linha, coluna):
    for i in range(len(letra)):
        for j in range(len(letra[i])):
            if letra[i][j] in "🟥💣" and 0 <= linha + i < 20 and 0 <= coluna + j < 10:
                tabtetris[linha + i][coluna + j] = letra[i][j]

# Remove a peça da posição, substituindo seus blocos por ⬜
def limpar_letra(letra, linha, coluna):
    for i in range(len(letra)):
        for j in range(len(letra[i])):
            if letra[i][j] in "🟥💣" and 0 <= linha + i < 20 and 0 <= coluna + j < 10:
                tabtetris[linha + i][coluna + j] = "⬜"

# Verifica se a peça irá bater com outra peça ou com o limite do tabuleiro ao se mover para uma posição específica. 
# Retorna True em caso de colisão.
def verificar_colisao(letra, linha, coluna):
    for i in range(len(letra)):
        for j in range(len(letra[i])):
            if letra[i][j] in "🟥💣":
                if linha + i >= 20 or coluna + j < 0 or coluna + j >= 10 or tabtetris[linha + i][coluna + j] == "🟥":
                    return True
    return False

# Gira as peças utilizando o zip do curses
def rotacionar_letra(letra):
    return [list(reversed(col)) for col in zip(*letra)]

# Remove as linhas completamente preenchidas com blocos 🟥 e insere novas linhas vazias no topo.
# Calcula e retorna o número de linhas removidas.
def remover_linhas_completas():
    linhas_removidas = 0
    nova_tabtetris = [linha for linha in tabtetris if not all(celula == "🟥" for celula in linha)]
    linhas_removidas = 20 - len(nova_tabtetris)

    while len(nova_tabtetris) < 20:
        nova_tabtetris.insert(0, ['⬜' for _ in range(10)])

    for i in range(20):
        tabtetris[i] = nova_tabtetris[i]

    return linhas_removidas

# Essa função gera a pontuação com base no número de linhas removidas. 
# Uma linha removida vale 100, duas linhas removidas vale o 4x mais.
def atualizar_pontuacao(linhas_removidas):
    if linhas_removidas == 1:
        return 100
    elif linhas_removidas == 2:
        return 400
    elif linhas_removidas == 3:
        return 600
    elif linhas_removidas == 4:
        return 800
    else:
        return 0

# Verifica se o jogo acabou, chamando 'verificar_colisao' para checar se a nova peça bate de início.
def game_over(letra, linha, coluna):
    return verificar_colisao(letra, linha, coluna)

# Caso a peça BMB caia, ela elimina as peças ao seu redor (3x3) e se elimina logo após
# Se a peça cair e não tiver nada ao redor, ela se auto-elimina.
# Caso a bomba elimine outras peças, após verificar que não tem mais nenhuma, ela se elimina.
def explodir_bomba(linha, coluna):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= linha + i < 20 and 0 <= coluna + j < 10:
                tabtetris[linha + i][coluna + j] = "⬜"

# Função principal do programa, onde ele gera as peças, gera a pontuação, gera os comandos
# Essa função desenvolve todo o game e entra no loop infinito até o game chamar a função game over.
def jogartetris(stdscr):
    pontos = 0
    letra_atual = random.choice(letras)
    linha_atual = 0
    coluna_atual = 3
    tempo_descida = time.time()
    curses.curs_set(0)
    stdscr.nodelay(True)

    while True:
        print_tabtetris(stdscr, pontos)
        limpar_letra(letra_atual, linha_atual, coluna_atual)

        if time.time() - tempo_descida > 0.1:
            linha_atual += 1
            tempo_descida = time.time()

        if verificar_colisao(letra_atual, linha_atual, coluna_atual):
            linha_atual -= 1

            if letra_atual == BMB:
                explodir_bomba(linha_atual, coluna_atual)
            else:
                colocar_letra(letra_atual, linha_atual, coluna_atual)

            linhas_removidas = remover_linhas_completas()
            pontos += atualizar_pontuacao(linhas_removidas)

            letra_atual = random.choice(letras)
            linha_atual = 0
            coluna_atual = 3

            if verificar_colisao(letra_atual, linha_atual, coluna_atual):
                stdscr.addstr(22, 0, "GAME OVER")
                stdscr.refresh()
                stdscr.nodelay(False)
                stdscr.getch()
                break

        key = stdscr.getch()
        if key == ord('d') and not verificar_colisao(letra_atual, linha_atual, coluna_atual + 1):
            coluna_atual += 1
        elif key == ord('a') and not verificar_colisao(letra_atual, linha_atual, coluna_atual - 1):
            coluna_atual -= 1
        elif key == ord('w'):
            nova_letra = rotacionar_letra(letra_atual)
            if not verificar_colisao(nova_letra, linha_atual, coluna_atual):
                letra_atual = nova_letra
        elif key == ord('s'):
            while not verificar_colisao(letra_atual, linha_atual + 1, coluna_atual):
                linha_atual += 1

        colocar_letra(letra_atual, linha_atual, coluna_atual)
        curses.napms(160)

# Menu iniciaizador do jogo
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
