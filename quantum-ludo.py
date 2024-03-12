import pygame
import numpy
from controls.circuit_grid import CircuitGrid
from data import globals
from model.circuit_grid_model import CircuitGridModel

pygame.init()
screen = pygame.display.set_mode((globals.WINDOW_WIDTH,globals.WINDOW_HEIGHT))
pygame.display.set_caption('Quantum Ludo')
clock = pygame.time.Clock()

def main():
  #initialize game
  circuit_grid = CircuitGrid(5, globals.FIELD_HEIGHT, CircuitGridModel(globals.NUM_QUBITS,16))


  exit = False
  while not exit:
    #exit when the exit button is pressed
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
          exit = True

    #update game
    

    #draw game
    circuit_grid.draw(screen)
    pygame.display.flip()

    #set framerate
    clock.tick(60)

#This allows the script to be imported and its functions to be used without running the main functionality defined within the main() function.
if __name__ == '__main__':
    main()
