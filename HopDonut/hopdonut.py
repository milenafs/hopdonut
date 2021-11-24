'''
Grupo:
Isabela Clementino Ponciano Ferreira - 20138
Milena Furuta Shishito - 20148
'''

import random
import time
import os
from pygame.locals import(
    K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE, K_ESCAPE, KEYDOWN, QUIT)

import pygame as pg

#Tamanho tela do jogo
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 525

#contadores de inimgos, cenouras e tempo
cnt_enemy = 0
cnt_food = 0
counter, text = 100, '100'.rjust(1)

#criando cores no python
white = (255,255,255)
BLACK = (0,0,0)

pg.init()

#timer
clock = pg.time.Clock()
pg.time.set_timer(pg.USEREVENT, 1000)

# criando fontes para escrever na tela
font = pg.font.SysFont("Verdana",20)

#Criação da tela
screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pg.RESIZABLE )
posx = 100
posy = 100
pg.display.set_caption("HopDonut")

#Dados que vão ser mostrados ao final do jogo
qtdFood = 0
qtdDonuts = 0

#Sons
somJogo = pg.mixer.Sound('sounds/songgame.wav')
comeuCenoura = pg.mixer.Sound('sounds/comeuCenoura.wav')
perderVida = pg.mixer.Sound('sounds/perderVida.wav')
shot = pg.mixer.Sound('sounds/shot.wav')
comeuCenoura.set_volume(0.5)
somGanhou = pg.mixer.Sound('sounds/ganhou.wav')
somPerdeu = pg.mixer.Sound('sounds/GameOver.wav')
somMenu = pg.mixer.Sound('sounds/songmenu.wav')
somTutorial = pg.mixer.Sound('sounds/tutorial.wav')


#Classes que usamos 
class Tiro(pg.sprite.Sprite):
    def __init__(self, player):
        super(Tiro, self).__init__()
        self.imTiro = pg.image.load("img/bala.png")       
        self.imgP2 = pg.transform.scale(self.imTiro, (15,15))
        self.imgP = pg.transform.rotate(self.imgP2, 300)
        self.surf = pg.transform.flip(self.imgP,False,True) 
        self.rect = self.surf.get_rect(
            center=(
                player.rect.right, player.rect.centery                
            )
        )
        self.speed = 8
        
    def update(self, pressed_keys):
        self.rect.move_ip(self.speed,0)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()
            
    def draw(self, surface):
        surface.blit(self.surf, self.rect)

class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.imDonut = pg.image.load("img/donut.png")       
        self.imgP2 = pg.transform.scale(self.imDonut, (50,50))
        self.imgP = pg.transform.rotate(self.imgP2, 180)
        self.imgP = pg.transform.flip(self.imgP,False,True)       
        self.surf = self.imgP
  
      
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH+100),
                random.randint(50, SCREEN_HEIGHT),
            )
        )
        self.speed = 7
        
    def update(self, pressed_keys):
        global cnt_enemy
        self.rect.move_ip(-self.speed,0)
        if self.rect.right < 0:
            cnt_enemy = cnt_enemy + 1
            self.kill()
            
    def draw(self, surface):
        surface.blit(self.surf, self.rect)
           
class Food(pg.sprite.Sprite):
    def __init__(self):
        super(Food, self).__init__()
        self.imCenoura = pg.image.load("img/cenoura.png")       
        self.imgP2 = pg.transform.scale(self.imCenoura, (40,40))
        self.imgP = pg.transform.rotate(self.imgP2, 180)
        self.imgP = pg.transform.flip(self.imgP,False,True)       
        self.surf = self.imgP
  
      
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH+100),
                random.randint(50, SCREEN_HEIGHT),
            )
        )
        self.speed = 6
        
    def update(self, pressed_keys):
        global cnt_food
        self.rect.move_ip(-self.speed,0)
        if self.rect.right < 0:
            cnt_food = cnt_food + 1
            self.kill()
            
    def draw(self, surface):
        surface.blit(self.surf, self.rect)

class Player(pg.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.imPluto = pg.image.load("img/aviao.png")
        self.imgP2 = pg.transform.scale(self.imPluto, (100,100))
        self.imgP = pg.transform.rotate(self.imgP2, 180)
        self.imgP = pg.transform.flip(self.imgP,False,True)
        
        self.surf = self.imgP
        
        self.rect = self.surf.get_rect()
        
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
           self.rect.move_ip(0,-5)       
        if pressed_keys[K_DOWN]:
           self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
           self.rect.move_ip(-5, 0) 
        if pressed_keys[K_RIGHT]:
           self.rect.move_ip(5, 0)
        # manten o individuo dentro da tela   
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > (SCREEN_WIDTH):
            self.rect.right = (SCREEN_WIDTH)
        if self.rect.top < 30:
            self.rect.top = 30
        if self.rect.bottom > (SCREEN_HEIGHT):
            self.rect.bottom = (SCREEN_HEIGHT)            
           
           
    def draw(self, surface):
        surface.blit(self.surf, self.rect)


#Método para jogar 
def jogar():
    #zera as variavéis que usamos ao longo do jogo
    qtdFood = 0
    qtdVida = 5
    qtdDonuts = 0
    
    #timer
    counter, text = 100, '100'.rjust(1)
    
    # criar um novo evento
    ADDENEMY = pg.USEREVENT + 1
    pg.time.set_timer(ADDENEMY,1000)

    # criar um novo evento
    ADDFOOD = pg.USEREVENT + 2
    pg.time.set_timer(ADDFOOD,1200)

    #Paramos possíveis sons antigos
    pg.mixer.Sound.stop(somMenu)
    pg.mixer.Sound.stop(somGanhou)
    pg.mixer.Sound.stop(somPerdeu)
    
    #Sound de fundo
    pg.mixer.Sound.play(somJogo)
    pg.mixer.Sound.set_volume(somJogo,0.3)

    player = Player()

    enemies  = pg.sprite.Group()
    foods    = pg.sprite.Group()
    tiros    = pg.sprite.Group()

    all_sprites = pg.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(enemies)
    all_sprites.add(foods)
    all_sprites.add(tiros)
    running = True
    while running:
    # pegar evento do X de fechar janela
        for event in pg.event.get():
            if event.type == KEYDOWN:
            # verifico qual tecla apertada 
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_SPACE: #Atirou
                    new_tiro = Tiro(player)
                    tiros.add(new_tiro)
                    all_sprites.add(tiros)
                    pg.mixer.Sound.play(shot)
                    pg.mixer.Sound.set_volume(shot,0.7)                  
            elif event.type == pg.QUIT:
                running = False        
            elif event.type == ADDENEMY: # crio um novo inimigo
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy) 
            elif event.type == ADDFOOD: # crio um novo food
                new_food = Food()
                foods.add(new_food)
                all_sprites.add(new_food)
            elif event.type == pg.USEREVENT: 
                counter -= 1
                text = str(counter).rjust(1) 
                if counter == 0: #Acabou o tempo e jogador não perdeu
                    abrirtelaVenceu(qtdDonuts,qtdFood, counter)
                
        #Tela de fundo
        keyp = pg.key.get_pressed()
        screen.fill(white)
        background = pg.image.load("img/bk.jpeg")
        back = pg.transform.scale(background, (800,525))                 
        screen.blit(back, [0, 0])
        
        text = str(counter).rjust(1)      
        screen.blit(font.render(text, True, (0, 0, 0)), (760, 10))
        relogio = pg.image.load("img/timer.png")
        relogio = pg.transform.scale(relogio, (35,35))
        screen.blit(relogio,(730,5))        
        all_sprites.update(keyp)
        #Atualiza a quantidade de corações na tela
        atualizarVida(qtdVida,qtdDonuts,qtdFood, counter)  
        
        for inimigo in enemies:
            if pg.sprite.spritecollideany(inimigo, tiros):
                for tiro in tiros:
                    if pg.sprite.spritecollideany(tiro, enemies):
                        qtdDonuts = qtdDonuts + 1 #Destruiu um donut
                        tiro.kill()
                        inimigo.kill()
            if pg.sprite.collide_rect(inimigo, player):
                qtdVida= qtdVida - 1 #personagem colidiu com um donut
                atualizarVida(qtdVida,qtdDonuts,qtdFood, counter)
                inimigo.kill()
                pg.mixer.Sound.play(perderVida)
                
        
        for food in foods: 
            if pg.sprite.spritecollideany(food, tiros): #tiro matou a comida
                for tiro in tiros:
                    if pg.sprite.spritecollideany(tiro, foods):
                        tiro.kill()
                        food.kill()       
            if pg.sprite.collide_rect(food, player): #Coletou a cenoura/food
                qtdFood = qtdFood + 1
                food.kill()
                pg.mixer.Sound.play(comeuCenoura)
                
        #Desenha as sprites        
        for entity in all_sprites:
            entity.draw(screen)
        
        pg.display.flip()
        clock.tick(60)
    pg.quit()



def atualizarVida(qtdVidas,qtdDonutsPegou,qtdFoodPegou, counterTempo): 
    if qtdVidas == 0:  #morreu, está sem vidas
        abrirtelaPerdeu(qtdDonutsPegou,qtdFoodPegou, counterTempo)
    
    #Vai desenhando os corações de acordo com a qtdVidas
    aux = 0
    while (aux <= qtdVidas):
        if(aux == 5):
            coracao5 = pg.image.load("img/coracaozinho.png")
            coracao5 = pg.transform.scale(coracao5, (30,30))
            screen.blit(coracao5 ,  ( 125,5))
        if(aux == 4):
            coracao4 = pg.image.load("img/coracaozinho.png")
            coracao4 = pg.transform.scale(coracao4, (30,30))
            screen.blit(coracao4 ,  (95,5))
        if(aux == 3):
            coracao3 = pg.image.load("img/coracaozinho.png")
            coracao3 = pg.transform.scale(coracao3, (30,30))
            screen.blit(coracao3 ,  ( 65,5))
        if(aux == 2):
            coracao2 = pg.image.load("img/coracaozinho.png")
            coracao2 = pg.transform.scale(coracao2, (30,30))
            screen.blit(coracao2 ,  ( 35,5))
        if(aux == 1):
            coracao1 = pg.image.load("img/coracaozinho.png")
            coracao1 = pg.transform.scale(coracao1, (30,30))
            screen.blit(coracao1 ,  ( 5,5))
        aux = aux + 1
        
        #pg.display.flip()



def abrirtelaVenceu(qtdDonutsPegou,qtdFoodPegou, counterTempo):
    # Para sons antigos
    pg.mixer.Sound.stop(somJogo)
    #Música tela vitória
    pg.mixer.Sound.play(somGanhou)
    #Imagem fundo
    background = pg.image.load("img/telaVenceu.png")
    back = pg.transform.scale(background, (800,525))
    screen.blit(back, [0, 0])
    pg.display.flip()   

    #colocar os textos no espaço correto
    tempoJogo = 100 - counterTempo
    txtTempo=str(tempoJogo).rjust(1)                          
    txtDonuts = str(qtdDonutsPegou)
    txtFood = str(qtdFoodPegou)
    pg.font.init()                                     
    fonte=pg.font.get_default_font()                   
    fontesys=pg.font.SysFont("Verdanda", 50)           
    txttela = fontesys.render(txtTempo, 1, (0,0,0))   
    txttela2 = fontesys.render(txtDonuts, 1, (0,0,0))
    txttela3 = fontesys.render(txtFood, 1, (0,0,0))
    screen.blit(txttela,(95,250))                       
    screen.blit(txttela2,(360,250))  
    screen.blit(txttela3,(610,250))  
    pg.display.update()                               

    # Vẽ opção escolhida
    naoclicou = True
    while (naoclicou):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                x, y= event.pos
                if x > 180 and x < 299 and y > 411 and y < 470: #SIM 
                   jogar()
                if x > 493 and x < 619 and y > 411 and y < 470: #NÃO
                   abrirtelainicial()




def abrirtelaPerdeu(qtdDonutsPegou,qtdFoodPegou, counterTempo):
    #Para som antigo
    pg.mixer.Sound.stop(somJogo)
    #Som de fundo
    pg.mixer.Sound.play(somPerdeu)
    #Fundo
    background = pg.image.load("img/telaPerdeu.png")
    back = pg.transform.scale(background, (800,525))
    screen.blit(back, [0, 0])
    pg.display.flip()   
    #colocar os textos
    tempoJogo = 100 - counterTempo
    txtTempo=str(tempoJogo).rjust(1)                          
    txtDonuts = str(qtdDonutsPegou)
    txtFood = str(qtdFoodPegou)
    pg.init()                                     
    fonte=pg.font.get_default_font()                   
    fontesys=pg.font.SysFont("Verdanda", 50)           
    txttela = fontesys.render(txtTempo, 1, (0,0,0))   
    txttela2 = fontesys.render(txtDonuts, 1, (0,0,0))
    txttela3 = fontesys.render(txtFood, 1, (0,0,0))
    screen.blit(txttela,(95,250))                       
    screen.blit(txttela2,(360,250))  
    screen.blit(txttela3,(610,250))  
    pg.display.update()                                

    #Vê a escolha do jogador
    naoclicou = True
    while (naoclicou):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                x, y= event.pos
                if x > 180 and x < 299 and y > 411 and y < 470: #SIM
                   jogar()
                if x > 493 and x < 619 and y > 411 and y < 470: #NÃO
                   abrirtelainicial()



def abrirtelainicial():
    #Para sons antigos
    pg.mixer.Sound.stop(somGanhou)
    pg.mixer.Sound.stop(somPerdeu)
    pg.mixer.Sound.stop(somTutorial)
    #Música para a tela munu
    pg.mixer.Sound.play(somMenu)
    pg.mixer.Sound.set_volume(somMenu,0.3)
    #Imagem de fundo
    background = pg.image.load("img/HopDonut.png")
    back = pg.transform.scale(background, (800,525))
    screen.blit(back, [0, 0])
    pg.display.flip()
    #Vê a opção que foi escolhida
    running = True
    while (running):
        for event in pg.event.get():
            if event.type == pg.QUIT:
               pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                x, y= event.pos
                if x > 64 and x < 269 and y > 158 and y < 300: # Clicou no sair
                    pg.quit()
                elif x > 298 and x < 501 and y > 158 and y < 300: # Clicou no jogar
                    jogar()
                elif x > 552 and x < 749 and  y > 158 and y < 300: # Clicou no tutorial
                    abrirtelatutorial()


def abrirtelatutorial():
    #Para música antiga
    pg.mixer.Sound.stop(somMenu)
    #Começa música da tela
    pg.mixer.Sound.play(somTutorial)
    pg.mixer.Sound.set_volume(somTutorial,0.6)
    #Imagem de fundo
    background = pg.image.load("img/telaTutorial.png")
    back = pg.transform.scale(background, (800,525))
    screen.blit(back, [0, 0])
    pg.display.flip()
    #Vẽ se clicou no botão
    naoclicou = True
    while (naoclicou):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                naoclicou = False
            if event.type == pg.MOUSEBUTTONDOWN:
                x, y= event.pos
                if x > 341 and x < 453 and y > 435 and y < 494: #Clicou no Voltar
                    abrirtelainicial()
                    
                    
abrirtelainicial() #Já começa no menu / tela inicial