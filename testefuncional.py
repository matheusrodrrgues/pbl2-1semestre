# prompt: sem true e false

import random, os, time
import random
import os
import time


tabtetris = []
for i in range(20):
    linha = []
    for c in range(10):
        linha.append("⬜")
    tabtetris.append(linha)

#  peças
I = ["🟥", "🟥", "🟥", "🟥"]
T = [["🟥", "🟥", "🟥"],
    [" ", "🟥", " "],
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

letras = [I, T, O, S, Z, J, L]

def print_tabtetris():
    os.system('clear' if os.name == 'posix' else 'cls')
    for linha in tabtetris:
        print("".join(linha))
    print("\n")

def colocar_letra(letra, linha, coluna):
    if len(letra) > 0 and type(letra[0]) == list:
        for i in range(len(letra)):
            for j in range(len(letra[0])):
                if letra[i][j] == "🟥":
                    if linha + i < 20 and coluna + j < 10:
                        tabtetris[linha + i][coluna + j] = "🟥"
    else:
        for j in range(len(letra)):
            if coluna + j < 10:
                tabtetris[linha][coluna + j] = letra[j]
                
# Escolher uma peça aleatória
letra_atual = random.choice(letras)

# Inicializar a peça na primeira linha
linha_atual = 0
coluna_atual = 0

if type(letra_atual[0]) == list:  # Peças com várias linhas
    for i in range(len(letra_atual)):
        for j in range(len(letra_atual[0])):
            if letra_atual[i][j] == "🟥":
                if coluna_atual + j < 10 and linha_atual + i < 20:
                    tabtetris[linha_atual + i][coluna_atual + j] = "🟥"
else:
    for j in range(len(letra_atual)):
        if coluna_atual + j < 10:
            tabtetris[linha_atual][coluna_atual + j] = letra_atual[j]

# mover bloco por tempo
print_tabtetris()

while 1:
    # apagar posicao anterior
    if type(letra_atual[0]) == list:
        for k in range(len(letra_atual)):
            for l in range(len(letra_atual[0])):
                if letra_atual[k][l] == "🟥":
                    if linha_atual + k < 20 and coluna_atual + l < 10:
                        tabtetris[linha_atual + k][coluna_atual + l] = "⬜"
    else:
        for j in range(len(letra_atual)):
            if linha_atual < 20 and coluna_atual + j < 10:
                tabtetris[linha_atual][coluna_atual + j] = "⬜"

    # bloco pra proxima linha
    linha_atual += 1

    pode_descer = 1
    if type(letra_atual[0]) == list:
        for k in range(len(letra_atual)):
            for l in range(len(letra_atual[0])):
                if letra_atual[k][l] == "🟥":
                    if linha_atual + k >= 19 or tabtetris[linha_atual + k + 1][coluna_atual + l] == "🟥":
                        pode_descer = 0
                        break
            if pode_descer == 0:
                break
    else:
        for j in range(len(letra_atual)):
            if linha_atual >= 19 or tabtetris[linha_atual + 1][coluna_atual + j] == "🟥":
                pode_descer = 0
                break

    if pode_descer:
        if type(letra_atual[0]) == list:
            for k in range(len(letra_atual)):
                for l in range(len(letra_atual[0])):
                    if letra_atual[k][l] == "🟥":
                        if linha_atual + k < 20 and coluna_atual + l < 10:
                            tabtetris[linha_atual + k][coluna_atual + l] = "🟥"
        else:
            for j in range(len(letra_atual)):
                if linha_atual < 20 and coluna_atual + j < 10:
                    tabtetris[linha_atual][coluna_atual + j] = letra_atual[j]
    else:
        # A peça atingiu o fundo ou outra peça, parar de mover
        linha_atual -= 1
        if type(letra_atual[0]) == list:
            for k in range(len(letra_atual)):
                for l in range(len(letra_atual[0])):
                    if letra_atual[k][l] == "🟥":
                        if linha_atual + k < 20 and coluna_atual + l < 10:
                            tabtetris[linha_atual + k][coluna_atual + l] = "🟥"
        else:
            for j in range(len(letra_atual)):
                if linha_atual < 20 and coluna_atual + j < 10:
                    tabtetris[linha_atual][coluna_atual + j] = letra_atual[j]
        # Criar uma nova peça
        letra_atual = random.choice(letras)
        linha_atual = 0
        coluna_atual = 0
        if type(letra_atual[0]) == list:
            for i in range(len(letra_atual)):
                for j in range(len(letra_atual[0])):
                    if letra_atual[i][j] == "🟥":
                        if coluna_atual + j < 10 and linha_atual + i < 20:
                            if tabtetris[linha_atual + i][coluna_atual + j] == "⬜":
                                tabtetris[linha_atual + i][coluna_atual + j] = "🟥"


        else:
            for j in range(len(letra_atual)):
                if coluna_atual + j < 10:
                    if tabtetris[linha_atual][coluna_atual + j] == "⬜":
                        tabtetris[linha_atual][coluna_atual + j] = letra_atual[j]


    # Exibir o tabtetris final
    print_tabtetris()
    time.sleep(0.5)
