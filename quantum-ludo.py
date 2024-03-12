import pygame
pygame.init()
screen = pygame.display.set_mode((1200,750))
pygame.display.set_caption('Quantum Ludo')
clock = pygame.time.Clock()

def main():
  exit = False
  while not exit:
    #exit when the exit button is pressed
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
          exit = True

    #set framerate
    clock.tick(60)

#This allows the script to be imported and its functions to be used without running the main functionality defined within the main() function.
if __name__ == '__main__':
    main()
