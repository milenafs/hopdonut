import pygame
import sys
pygame.init()
width=800
height=525
white = (255,255,255)

screen = pygame.display.set_mode( (width, height ) )
background = pygame.image.load("img/HopDonut.png")
back = pygame.transform.scale(background, (800,525))
screen.blit(back, [0, 0])
pygame.display.flip()

 
running = True
while (running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y= event.pos
            print(x)
            print(y)
            print(x > 64 and x < 169 and y > 158 and y< 169)
            if x > 64 and x < 169 and y > 158 and y< 300:
                screen.fill(white)
                pygame.display.flip() 
                print('Clicou no Sair')
            #xJogar, yJogar= event.pos
            elif x > 298 and x < 501 and y > 158 and y < 300:
                screen.fill(white)
                pygame.display.flip() 
                print('Clicou no Jogar')
                #xTutorial, yTutorial= event.pos
            elif x > 552 and x < 749 and  y > 158 and y < 300:
                screen.fill(white)
                pygame.display.flip()
                print('Clicou no TUTORIAL')
#
#loop over, quite pygame
pygame.quit()