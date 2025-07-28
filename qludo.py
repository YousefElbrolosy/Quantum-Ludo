'''
                            _        __   __   ___       ___
                           / /     /  / /  /  / __ \   / __ \ 
                          / /     /  / /  /  / / / /  / / / /
                         / /_ _  /  / /  /  / /_/ /  / /_/ /
                        /_ _ _/  \_ _ _ /  /_ _ _/   \_ _ /
'''


       # 1- improve Capturing Mechanism (implemented)
       # 2- Go back to home when captured (implemented)
       # 3- Can't be captured in star areas nor safe zones (implemented)
       # 4- WHAT NEEDS TO BE IMPLEMENTED IS WHENEVER SAME COLOR PEACE IS ON ONE OF THE CELLS WITH ARROW WITH ITS COLOR (MOVE ALONG ITS SAME LINE
# Importing Modules

import pygame
from   pygame import mixer
import random
import time

# Initializing pygame
import numpy
import qiskit
from qiskit import *
from qiskit import QuantumCircuit

#from qiskit_aer import Aer
from controls.circuit_grid import CircuitGrid
from data import globals
from model.circuit_grid_model import CircuitGridModel
pygame.init()
pygame.display.set_caption("Ludo")
screen = pygame.display.set_mode((1200, 875))

from qiskit_aer import AerSimulator
from qiskit.circuit.library import *
from qiskit_aer.noise import (NoiseModel, depolarizing_error)


# Circuit Grid setting


# Loading Images

board = pygame.image.load('ludo_utils/Board.jpg')
star  = pygame.image.load('ludo_utils/star.png')
one   = pygame.image.load('ludo_utils/1.png')
two   = pygame.image.load('ludo_utils/2.png')
three = pygame.image.load('ludo_utils/3.png')
four  = pygame.image.load('ludo_utils/4.png')
five  = pygame.image.load('ludo_utils/5.png')
six   = pygame.image.load('ludo_utils/6.png') 
seven   = pygame.image.load('ludo_utils/7.png') 



red    = pygame.image.load('ludo_utils/red.png')
blue   = pygame.image.load('ludo_utils/blue.png')
green  = pygame.image.load('ludo_utils/green.png')
yellow = pygame.image.load('ludo_utils/yellow.png')


DICE  = [one, two, three, four, five, six, seven]
color = [red, green, yellow, blue]

# Loading Sounds

killSound   = mixer.Sound("ludo_utils/Killed.wav")
tokenSound  = mixer.Sound("ludo_utils/Token Movement.wav")
diceSound   = mixer.Sound("ludo_utils/Dice Roll.wav")
winnerSound = mixer.Sound("ludo_utils/Reached Star.wav")
background_music = mixer.music.load("utils/415804__sunsai__mushroom-background-music.wav")

# Initializing Variables

number        = 0
currentPlayer = 0
playerKilled  = False
diceRolled    = False
winnerRank    = []

# Rendering Text

font = pygame.font.Font('freesansbold.ttf', 11)
FONT = pygame.font.Font('freesansbold.ttf', 16)
currentPlayerText = font.render('Current Player', True, (0, 0, 0))
line = font.render('----------------------', True, (0, 0, 0))
rulesText = font.render('Rules:', True, (0,0,0))

# Defining Important Coordinates

HOME = [[(110, 58),  (61, 107),  (152, 107), (110, 152)],  # Red
        [(466, 58),  (418, 107), (509, 107), (466, 153)],  # Green
        [(466, 415), (418, 464), (509, 464), (466, 510)],  # Yellow
        [(110, 415), (61, 464),  (152, 464), (110, 510)]]  # Blue

        # Red      # Green    # Yellow    # Blue
SAFE = [(50, 240), (328, 50), (520, 328), (240, 520),   # the yellow paths (safe paths)
        (88, 328), (240, 88), (482, 240), (328, 482)]

position = [[[110, 58],  [61, 107],  [152, 107], [110, 152]],  # Red
            [[466, 58],  [418, 107], [509, 107], [466, 153]],  # Green
            [[466, 415], [418, 464], [509, 464], [466, 510]],  # Yellow
            [[110, 415], [61, 464],  [152, 464], [110, 510]]]  # Blue

jump = {(202, 240): (240, 202),  # R1 -> G3
        (328, 202): (368, 240),  # G1 -> Y3
        (368, 328): (328, 368),  # Y1 -> B3
        (240, 368): (202, 328)}  # B1 -> R3

         # Red        # Green     # Yellow    # Blue
WINNER = [[240, 284], [284, 240], [330, 284], [284, 330]]




# Blit Token Movement

def createGrid():

    circuit_grid = CircuitGrid(5, globals.FIELD_HEIGHT, CircuitGridModel(globals.NUM_QUBITS,16))
    circuit_grid.handle_input(pygame.K_h)
    circuit_grid.handle_input(pygame.K_s)
    circuit_grid.handle_input(pygame.K_h)
    circuit_grid.handle_input(pygame.K_s)
    circuit_grid.handle_input(pygame.K_h)
    circuit_grid.handle_input(pygame.K_w)
    circuit_grid.handle_input(pygame.K_w)
    circuit_grid.handle_input(pygame.K_d)
    globals.GATE_COUNT=3
    return circuit_grid
def show_token(x, y):
    screen.blit(board, (0, 0))

    for i in SAFE[4:]:
        screen.blit(star, i)

    for i in range(len(position)):
        for j in position[i]:
            screen.blit(color[i], j)
    if (number==0  or number==7):
        screen.blit(pygame.transform.scale(DICE[6],(64,64)), (605, 270))
    else:
        screen.blit(DICE[number-1], (605, 270))


    if position[x][y] in WINNER:
        winnerSound.play()
    else:
        tokenSound.play()

    screen.blit(color[currentPlayer], (620, 28))
    screen.blit(currentPlayerText, (600, 10))
    screen.blit(line, (592, 59))

    for i in range(len(winnerRank)):
        rank = FONT.render(f'{i+1}.', True, (0, 0, 0))
        screen.blit(rank, (600, 85 + (40*i)))
        screen.blit(color[winnerRank[i]], (620, 75 + (40*i)))

    pygame.display.update()
    time.sleep(0.5)


# Quantum Dice
def quantum_dice():
    #circuit
    simulator = AerSimulator(noise_model = noise())
    circuit = circuit_grid.circuit_grid_model.compute_circuit()
    full_circuit = QuantumCircuit(19, 3)


    full_circuit = full_circuit.compose(circuit, [0,9,18])
    full_circuit = full_circuit.compose(error_correcting_circuit(), range(9))
    full_circuit = full_circuit.compose(error_correcting_circuit(), range(9,18))

    full_circuit.measure(0,0)
    full_circuit.measure(9,1)
    full_circuit.measure(18,2)
    
    transpiled_circuit = qiskit.transpile(full_circuit, simulator)
    counts = simulator.run(transpiled_circuit, shots = 1).result().get_counts(transpiled_circuit)

    # Display the counts
    print("Counts:", counts)

    # Extract the bitstring from the counts
    bitstring = list(counts.keys())[0]

    # Convert the bitstring to an integer
    dice_roll = int(bitstring, 2)

    print("dice roll: ", dice_roll)
    # Return the dice roll
    return dice_roll

# Bliting in while loop


# Define the noise model
def noise():
    i_error = depolarizing_error(0.3, 1)
    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(i_error, "i_with_error")
    return noise_model

# Define the noisy gate
def noise_circuit():
    # This should be qc = QuantumCircuit(1)
    # Measuring for demostration purposes
    qc = QuantumCircuit(1)
    i_gate = IGate(label="i_with_error")
    qc.append(i_gate, [0])
    return qc

# 3 qubit encoding circuit
def encoding_circuit():
    qc = QuantumCircuit(3)
    qc.cx(0,1)
    qc.cx(0,2)
    return qc
# 3 qubit decoding circuit
def decoding_circuit():
    qc = QuantumCircuit(3)
    qc.cx(0,1)
    qc.cx(0,2)
    qc.ccx(2, 1, 0)   
    return qc

# 3 qubit hadamard addition
def phase_correction():
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.h(1)
    qc.h(2)
    return qc

def error_correcting_circuit():
    qc = QuantumCircuit(9)
    
    qc = qc.compose(encoding_circuit(), [0,3,6])
    qc = qc.compose(phase_correction(), [0,3,6])
    
    qc = qc.compose(encoding_circuit(), [0,1,2])
    qc = qc.compose(encoding_circuit(), [3,4,5])
    qc = qc.compose(encoding_circuit(), [6,7,8])
    
    qc.barrier()
    qc = qc.compose(noise_circuit(), [0])
    qc.barrier()

    
    qc = qc.compose(decoding_circuit(), [0,1,2])
    qc = qc.compose(decoding_circuit(), [3,4,5])
    qc = qc.compose(decoding_circuit(), [6,7,8])
        
    qc = qc.compose(phase_correction(), [0,3,6])
    qc = qc.compose(decoding_circuit(), [0,3,6])
    
    return qc

def blit_all():
    for i in SAFE[4:]:
        screen.blit(star, i)

    for i in range(len(position)):
        for j in position[i]:
            screen.blit(color[i], j)
    if (number==0  or number==7):
        screen.blit(pygame.transform.scale(DICE[6],(64,64)), (605, 270))
    else:
        screen.blit(DICE[number-1], (605, 270))

    screen.blit(color[currentPlayer], (620, 28))
    screen.blit(currentPlayerText, (600, 10))
    screen.blit(line, (592, 59))

    for i in range(len(winnerRank)):
        rank = FONT.render(f'{i+1}.', True, (0, 0, 0))
        screen.blit(rank, (600, 85 + (40*i)))
        screen.blit(color[winnerRank[i]], (620, 75 + (40*i)))

# Is token move possible?

def to_home(x, y):
    #  R2
    if (position[x][y][1] == 284 and position[x][y][0] <= 202 and x == 0) \
            and (position[x][y][0] + 38*number > WINNER[x][0]):
        return False

    #  Y2
    elif (position[x][y][1] == 284 and 368 < position[x][y][0] and x == 2) \
            and (position[x][y][0] - 38*number < WINNER[x][0]):
        return False
    #  G2
    elif (position[x][y][0] == 284 and position[x][y][1] <= 202 and x == 1) \
            and (position[x][y][1] + 38*number > WINNER[x][1]):
        return False
    #  B2
    elif (position[x][y][0] == 284 and position[x][y][1] >= 368 and x == 3) \
            and (position[x][y][1] - 38*number < WINNER[x][1]):
        return False
    return True

# Moving the token

def move_token(x, y):
    global currentPlayer, diceRolled

    # Taking Token out of HOME
    if tuple(position[x][y]) in HOME[currentPlayer] and number == 6:
        position[x][y] = list(SAFE[currentPlayer])
        tokenSound.play()
        diceRolled = False

    # Moving token which is not in HOME 
    elif tuple(position[x][y]) not in HOME[currentPlayer]:
        diceRolled = False
        #switching player
        if not number == 6:
            currentPlayer = (currentPlayer+1) % 4
            globals.GATE_COUNT = 4
            global circuit_grid
            circuit_grid = createGrid()


        # Way to WINNER position

        #  R2

                  #yel checker num
        if (position[x][y][1] == 284 and position[x][y][0] <= 202 and x == 0) \
                and (position[x][y][0] + 38*number <= WINNER[x][0]):
            for i in range(number):
                position[x][y][0] += 38
                show_token(x, y)

        #  Y2
        elif (position[x][y][1] == 284 and 368 < position[x][y][0] and x == 2) \
                and (position[x][y][0] - 38*number >= WINNER[x][0]):
            for i in range(number):
                position[x][y][0] -= 38
                show_token(x,y)

        #  G2
        elif (position[x][y][0] == 284 and position[x][y][1] <= 202 and x == 1) \
                and (position[x][y][1] + 38*number <= WINNER[x][1]):
            for i in range(number):
                position[x][y][1] += 38
                show_token(x,y)
        #  B2
        elif (position[x][y][0] == 284 and position[x][y][1] >= 368 and x == 3) \
                and (position[x][y][1] - 38*number >= WINNER[x][1]):
            for i in range(number):
                position[x][y][1] -= 38
                show_token(x,y)

        # Other Paths
        else:
            for _ in range(number):

                #  R1, Y3
                if (position[x][y][1] == 240 and position[x][y][0] < 202) \
                        or (position[x][y][1] == 240 and 368 <= position[x][y][0] < 558):
                    position[x][y][0] += 38
                # R3 -> R2 -> R1
                elif (position[x][y][0] == 12 and position[x][y][1] > 240):
                    position[x][y][1] -= 44

                #  R3, Y1
                elif (position[x][y][1] == 328 and 12 < position[x][y][0] <= 202) \
                        or (position[x][y][1] == 328 and 368 < position[x][y][0]):
                    position[x][y][0] -= 38
                #  Y3 -> Y2 -> Y1
                elif (position[x][y][0] == 558 and position[x][y][1] < 328):
                    position[x][y][1] += 44

                #  G3, B1
                elif (position[x][y][0] == 240 and 12 < position[x][y][1] <= 202) \
                        or (position[x][y][0] == 240 and 368 < position[x][y][1]):
                    position[x][y][1] -= 38
                # G3 -> G2 -> G1
                elif (position[x][y][1] == 12 and 240 <= position[x][y][0] < 328):
                    position[x][y][0] += 44

                #  B3, G1
                elif (position[x][y][0] == 328 and position[x][y][1] < 202) \
                        or (position[x][y][0] == 328 and 368 <= position[x][y][1] < 558):
                    position[x][y][1] += 38
                #  B3 -> B2 -> B1
                elif (position[x][y][1] == 558 and position[x][y][0] > 240):
                    position[x][y][0] -= 44
                
                else:
                    for i in jump:
                        if position[x][y] == list(i):
                            position[x][y] = list(jump[i])
                            break

                show_token(x, y)

        # Killing Player
        if tuple(position[x][y]) not in SAFE:
            for i in range(len(position)):
                for j in range(len(position[i])):
                    if position[i][j] == position[x][y] and i != x:
                        position[i][j] = list(HOME[i][j])
                        killSound.play()
                        currentPlayer = (currentPlayer+3) % 4
                        globals.GATE_COUNT = 4
                        circuit_grid = createGrid()


# Checking Winner
def check_winner():
    global currentPlayer
    if currentPlayer not in winnerRank:
        for i in position[currentPlayer]:
            if i not in WINNER:
                return
        winnerRank.append(currentPlayer)
    else:
        currentPlayer = (currentPlayer + 1) % 4
        globals.GATE_COUNT = 4
        global circuit_grid
        circuit_grid = createGrid()


# Main LOOP

circuit_grid = createGrid()
mixer.music.set_volume(0.1)
#mixer.music.play(-1)

def settings():
    x=-50
    font_title = pygame.font.Font('data/fonts/pong.ttf',50)
    font_title_border = pygame.font.Font('data/fonts/pong.ttf',50)
    game_controls_txt = font_title.render("How to Play",True,'gold')
    game_controls_border = font_title_border.render("How to PLAY",True,'black')
    pygame.draw.rect(screen,'gray', pygame.Rect(705, 150+x, 475, 400),550,50)
    text_1 = font.render("1- YOU HAVE UP TO 3 GATES TO USE PER TURN.    ",True,'black')
    text_1_1 = font.render("GATES ARE:                       X, Y, Z, H, I, CNOT(X+C), CH(H+C), CY(Y+C), CZ(Z+C)",True,'black')
    text_2 = font.render("2- MOVE BETWEEN THE DIFFERENT WIRES BY (W A S D) KEYBOARD KEYS",True,'black')
    text_3 = font.render("3- YOU CAN APPLY ROTATION ON THE X, Y, Z GATES BY",True,'black')
    text_4 = font.render("(LEFT AND RIGHT) ARROW KEYS",True,'black')
    text_4_1 = font.render("4- AFTER USING YOUR 3 GATES TO BIAS THE DICE, CLICK ON THE DICE TO ROLL!",True,'black')
    #text_5 = font.render("5- BY DEFAULT WITHOUT ADDING ANY GATES, DICE HAS EQUAL PROBABILITY OF",True,'black')
    #text_6 = font.render("0 TO 7 ",True,'black')
    text_6_1 = font.render("5- TRY TO AVOID LANDING YOUR DICE ON 0 OR 7 THEY WASTE YOUR TURN!",True,'black')
    text_7 = font.render("6- AFTER THAT IT IS A NORMAL LUDO GAME ENJOY!",True,'black')


    screen.blit(game_controls_border,(798,x+88))
    screen.blit(game_controls_border,(802,x+88))
    screen.blit(game_controls_border,(800,x+91))
    screen.blit(game_controls_border,(800,x+85))
    screen.blit(game_controls_txt,((800,x+88)))
    screen.blit(text_1,(720,x+180))
    screen.blit(text_1_1,(720,x+200))
    screen.blit(text_2,(720,x+250))
    screen.blit(text_3,(720,x+300))
    screen.blit(text_4,(720,x+320))
    screen.blit(text_4_1,(720,x+370))
    #screen.blit(text_5,(720,x+420))
    #screen.blit(text_6,(720,x+440))
    screen.blit(text_6_1,(720,x+470))
    screen.blit(text_7,(720,x+520))





running = True
while(running):
    #screen.blit(background,(0,0))
    screen.fill((255, 255, 255))

    settings()

    
























    screen.blit(board, (0, 0)) # Bliting Board
    circuit_grid.draw(screen)
    check_winner()

    for event in pygame.event.get():
        
        # Event QUIT
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            circuit_grid.handle_input(event.key)
            print(globals.GATE_COUNT)

                

        # When MOUSEBUTTON is clicked
        if event.type == pygame.MOUSEBUTTONUP:
            coordinate = pygame.mouse.get_pos()

            # Rolling Dice
            if not diceRolled and (605 <= coordinate[0] <= 669) and (270 <= coordinate[1] <= 334):

                number = quantum_dice()
                
                diceSound.play()
                if (number!= 0 and number!=7):
                    flag = True
                    for i in range(len(position[currentPlayer])):
                        if tuple(position[currentPlayer][i]) not in HOME[currentPlayer] and to_home(currentPlayer, i):
                            flag = False
                    if (flag and number == 6) or not flag:
                        diceRolled = True

                    else:
                        currentPlayer = (currentPlayer+1) % 4
                        globals.GATE_COUNT = 4
                        circuit_grid = createGrid()
                else:
                    currentPlayer = (currentPlayer+1) % 4
                    globals.GATE_COUNT = 4
                    circuit_grid = createGrid()

            # Moving Player
            elif diceRolled:
                for j in range(len(position[currentPlayer])):
                    if position[currentPlayer][j][0] <= coordinate[0] <= position[currentPlayer][j][0]+31 \
                            and position[currentPlayer][j][1] <= coordinate[1] <= position[currentPlayer][j][1]+31:
                        move_token(currentPlayer, j)
                        break
                    
        # if event.type == pygame.MOUSEMOTION:
        #       x, y = pygame.mouse.get_pos()  # Get the mouse cursor position
        #       print(f"Mouse is at ({x}, {y})")

    blit_all()
    
    pygame.display.update()
