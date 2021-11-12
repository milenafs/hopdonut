# programa simples de jogo
'''
No unix - linux  fim de linha \n
DOs - Windows    fim de linha \r\n


'''
import random
import time
import os
from pygame.locals import(
    K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE, K_ESCAPE, KEYDOWN, QUIT)

import pygame as pg

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 525
cnt_enemy = 0
cnt_food = 0
counter, text = 100, '100'.rjust(1)


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
        self.speed = 4
        
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
        self.speed = 3
        
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
        self.speed = 4
        
    def update(self, pressed_keys):
        global cnt_food
        self.rect.move_ip(-self.speed,0)
        if self.rect.right < 0:
            cnt_food = cnt_food + 1
            self.kill()
            
    def draw(self, surface):
        surface.blit(self.surf, self.rect)

# definindo sprites
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
  
 

# inicia a tela em um determinada posicao....
x = 10
y = 10
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

#criando cores no python
white = (255,255,255)
BLACK = (0,0,0)
pg.init()
clock = pg.time.Clock()
pg.time.set_timer(pg.USEREVENT, 1000)

# criando fontes para escrever na tela
font = pg.font.SysFont("Verdana",20)
font_small = pg.font.SysFont("Verdana",20)
jogo_str = font.render("Donut War II", True, BLACK)



screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pg.RESIZABLE )
posx = 100
posy = 100

pg.display.set_caption("HopDonut")

# carregar uma imagem


# criar um novo evento
ADDENEMY = pg.USEREVENT + 1
pg.time.set_timer(ADDENEMY,1000);

# criar um novo evento
ADDFOOD = pg.USEREVENT + 2
pg.time.set_timer(ADDFOOD,1200);

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
      print(event.type)
      if event.type == KEYDOWN:
      # verifico qual tecla apertada 
          if event.key == K_ESCAPE:
              running = False
          if event.key == K_SPACE:
              new_tiro = Tiro(player)
              tiros.add(new_tiro)
              all_sprites.add(tiros)
      elif event.type == pg.QUIT:
          running = False    
     
      elif event.type == ADDENEMY:
          # crio um novo inimigo
          new_enemy = Enemy()
          enemies.add(new_enemy)
          all_sprites.add(new_enemy) 
      elif event.type == ADDFOOD:
           # crio um novo food
          new_food = Food()
          foods.add(new_food)
          all_sprites.add(new_food)
      elif event.type == pg.USEREVENT: 
           counter -= 1
           text = str(counter).rjust(1) 
           if counter == 0:
            screen.fill((white))
            
      
  
 
  keyp = pg.key.get_pressed()
  screen.fill(white)
  background = pg.image.load("img/bk.jpeg")
  back = pg.transform.scale(background, (800,525))
  screen.blit(back, [0, 0]) 
  text = str(counter).rjust(1)      
  screen.blit(font.render(text, True, (0, 0, 0)), (760, 10))        
  #pg.display.flip()
  #player.update(keyp)
  #enemies.update(keyp)
  all_sprites.update(keyp)
  
    # create surface

  
  coracao = pg.image.load("img/coracaozinho.png")
  coracao = pg.transform.scale(coracao, (30,30))  
  screen.blit(coracao ,  ( 5,5))
  screen.blit(coracao ,  ( 35,5))
  screen.blit(coracao ,  ( 65,5))
  screen.blit(coracao ,  ( 95,5))
  screen.blit(coracao ,  ( 125,5))


  for inimigo in enemies:
      if pg.sprite.spritecollideany(inimigo, tiros):
          for tiro in tiros:
              if pg.sprite.spritecollideany(tiro, enemies):
                  tiro.kill()
                  inimigo.kill()
                  
  for food in foods: 
    if pg.sprite.spritecollideany(food, tiros): #tiro matou a comida
        for tiro in tiros:
            if pg.sprite.spritecollideany(tiro, foods):
                tiro.kill()
                food.kill()              
    '''elif pg.sprite.spritecollideany(food, player): #tiro matou a comida
        if pg.sprite.spritecollideany(player, foods):
            food.kill()
            print("COMEU!!!")
  for food in foods: 
    if player. spritecollideany(food): #coelho comeu a comida
        food.kill()
        '''
        #tem q ver qtdHearts e +1

            


  for entity in all_sprites:
    entity.draw(screen)
  

  #pg.display.update()
  pg.display.flip()
  clock.tick(60)


pg.quit()