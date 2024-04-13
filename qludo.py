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
from qiskit import Aer, QuantumCircuit
from qiskit import execute
import qiskit
#from qiskit_aer import Aer
from controls.circuit_grid import CircuitGrid
from data import globals
from model.circuit_grid_model import CircuitGridModel
pygame.init()
pygame.display.set_caption("Ludo")
screen = pygame.display.set_mode((1200, 875))


# Circuit Grid setting
circuit_grid = CircuitGrid(5, globals.FIELD_HEIGHT, CircuitGridModel(globals.NUM_QUBITS,16))

# Loading Images

board = pygame.image.load('ludo_utils/Board.jpg')
star  = pygame.image.load('ludo_utils/star.png')
one   = pygame.image.load('ludo_utils/1.png')
two   = pygame.image.load('ludo_utils/2.png')
three = pygame.image.load('ludo_utils/3.png')
four  = pygame.image.load('ludo_utils/4.png')
five  = pygame.image.load('ludo_utils/5.png')
six   = pygame.image.load('ludo_utils/6.png') 

red    = pygame.image.load('ludo_utils/red.png')
blue   = pygame.image.load('ludo_utils/blue.png')
green  = pygame.image.load('ludo_utils/green.png')
yellow = pygame.image.load('ludo_utils/yellow.png')

DICE  = [one, two, three, four, five, six]
color = [red, green, yellow, blue]

# Loading Sounds

killSound   = mixer.Sound("ludo_utils/Killed.wav")
tokenSound  = mixer.Sound("ludo_utils/Token Movement.wav")
diceSound   = mixer.Sound("ludo_utils/Dice Roll.wav")
winnerSound = mixer.Sound("ludo_utils/Reached Star.wav")

# Initializing Variables

number        = 1
currentPlayer = 0
playerKilled  = False
diceRolled    = False
winnerRank    = []

# Rendering Text

font = pygame.font.Font('freesansbold.ttf', 11)
FONT = pygame.font.Font('freesansbold.ttf', 16)
currentPlayerText = font.render('Current Player', True, (0, 0, 0))
line = font.render('------------------------------------', True, (0, 0, 0))

# Defining Important Coordinates

HOME = [[(110, 58),  (61, 107),  (152, 107), (110, 152)],  # Red
        [(466, 58),  (418, 107), (509, 107), (466, 153)],  # Green
        [(466, 415), (418, 464), (509, 464), (466, 510)],  # Yellow
        [(110, 415), (61, 464),  (152, 464), (110, 510)]]  # Blue

        # Red      # Green    # Yellow    # Blue
SAFE = [(50, 240), (328, 50), (520, 328), (240, 520),
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

def show_token(x, y):
    screen.blit(board, (0, 0))

    for i in SAFE[4:]:
        screen.blit(star, i)

    for i in range(len(position)):
        for j in position[i]:
            screen.blit(color[i], j)

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
    simulator = Aer.get_backend('statevector_simulator')
    circuit = circuit_grid.circuit_grid_model.compute_circuit()
    transpiled_circuit = qiskit.transpile(circuit, simulator)
    statevector = simulator.run(transpiled_circuit, shots = 100).result()

    # Measure the qubits
    circuit.measure_all()

    # Convert the binary result to a decimal number between 1 and 6
    dice_roll = int(list(statevector.get_counts(circuit).keys())[0], 2)
    if dice_roll > 6:
        return quantum_dice()
    else:
        return dice_roll

# Bliting in while loop

def blit_all():
    for i in SAFE[4:]:
        screen.blit(star, i)

    for i in range(len(position)):
        for j in position[i]:
            screen.blit(color[i], j)

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
        if not number == 6:
            currentPlayer = (currentPlayer+1) % 4

        # Way to WINNER position

        #  R2
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
                show_token()

        #  G2
        elif (position[x][y][0] == 284 and position[x][y][1] <= 202 and x == 1) \
                and (position[x][y][1] + 38*number <= WINNER[x][1]):
            for i in range(number):
                position[x][y][1] += 38
                show_token()
        #  B2
        elif (position[x][y][0] == 284 and position[x][y][1] >= 368 and x == 3) \
                and (position[x][y][1] - 38*number >= WINNER[x][1]):
            for i in range(number):
                position[x][y][1] -= 38
                show_token()

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


# Main LOOP

running = True
while(running):
    screen.fill((255, 255, 255))
    screen.blit(board, (0, 0)) # Bliting Board
    circuit_grid.draw(screen)
    check_winner()

    for event in pygame.event.get():

        # Event QUIT
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            circuit_grid.handle_input(event.key)

        # When MOUSEBUTTON is clicked
        if event.type == pygame.MOUSEBUTTONUP:
            coordinate = pygame.mouse.get_pos()

            # Rolling Dice
            if not diceRolled and (605 <= coordinate[0] <= 669) and (270 <= coordinate[1] <= 334):
                number = quantum_dice()
                diceSound.play()
                flag = True
                for i in range(len(position[currentPlayer])):
                    if tuple(position[currentPlayer][i]) not in HOME[currentPlayer] and to_home(currentPlayer, i):
                        flag = False
                if (flag and number == 6) or not flag:
                    diceRolled = True

                else:
                    currentPlayer = (currentPlayer+1) % 4

            # Moving Player
            elif diceRolled:
                for j in range(len(position[currentPlayer])):
                    if position[currentPlayer][j][0] <= coordinate[0] <= position[currentPlayer][j][0]+31 \
                            and position[currentPlayer][j][1] <= coordinate[1] <= position[currentPlayer][j][1]+31:
                        move_token(currentPlayer, j)
                        break
                    
        if event.type == pygame.MOUSEMOTION:
              x, y = pygame.mouse.get_pos()  # Get the mouse cursor position
              print(f"Mouse is at ({x}, {y})")

    blit_all()
    
    pygame.display.update()
