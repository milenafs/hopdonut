import pygame
import sys

pygame.init()
width=800
height=525
white = (255,255,255)

#musica de fundo
pygame.mixer.music.load('sounds/songmenu.wav')
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.3)



screen = pygame.display.set_mode( (width, height ) )
def abrirtelainicial():
    background = pygame.image.load("img/HopDonut.png")
    back = pygame.transform.scale(background, (800,525))
    screen.blit(back, [0, 0])
    pygame.display.flip()
    running = True
    while (running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y= event.pos
                if x > 64 and x < 269 and y > 158 and y < 300: # Clicou no sair
                    pygame.quit()
                elif x > 298 and x < 501 and y > 158 and y < 300: # Clicou no jogar
                    import jogo
                elif x > 552 and x < 749 and  y > 158 and y < 300: # Clicou no tutorial
                    abrirtelatutorial()

def abrirtelatutorial():
    background = pygame.image.load("img/telaTutorial.png")
    back = pygame.transform.scale(background, (800,525))
    screen.blit(back, [0, 0])
    pygame.display.flip()   
    naoclicou = True
    while (naoclicou):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                naoclicou = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y= event.pos
                if x > 341 and x < 453 and y > 435 and y < 494:
                    abrirtelainicial()



#Jogo - fluxo 

abrirtelainicial()

#loop over, quite pygame
#pygame.quit()