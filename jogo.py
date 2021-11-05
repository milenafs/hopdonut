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



'''class Frase(pg.sprite.Sprite):
    def __init__(self):
        super(Frase,self).__init__()
        self.contagem = font_small.render("Teste", True, (255,0,0))
        self.rect = self.contagem.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH+100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(1,5)
        
    def update(self, pressed_keys):
        global cnt_enemy
        self.rect.move_ip(-self.speed,0)
        self.small = pg.font.SysFont("Verdana",60 -(self.rect.right%20))
        self.contagem = self.small.render("Teste", True, (255,0,0))
        if self.rect.right < 0:
            cnt_enemy = cnt_enemy + 1
            self.kill()
            
    def draw(self, surface):
        surface.blit(self.contagem, self.rect)'''





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
        self.speed = random.randint(1,5)
        
    def update(self, pressed_keys):
        self.rect.move_ip(self.speed,0)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()
            
    def draw(self, surface):
        surface.blit(self.surf, self.rect)


class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.imPluto = pg.image.load("img/donut.png")       
        self.imgP2 = pg.transform.scale(self.imPluto, (50,50))
        self.imgP = pg.transform.rotate(self.imgP2, 180)
        self.imgP = pg.transform.flip(self.imgP,False,True)       
        self.surf = self.imgP
  
      
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH+100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(1,5)
        
    def update(self, pressed_keys):
        global cnt_enemy
        self.rect.move_ip(-self.speed,0)
        if self.rect.right < 0:
            cnt_enemy = cnt_enemy + 1
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
        if self.rect.top < 0:
            self.rect.top = 0
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



# criando fontes para escrever na tela
font = pg.font.SysFont("Verdana",60)
font_small = pg.font.SysFont("Verdana",20)
jogo_str = font.render("Donut War II", True, BLACK)




screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pg.RESIZABLE )
posx = 100
posy = 100

pg.display.set_caption("Donut War II")

# carregar uma imagem


# criar um novo evento
ADDENEMY = pg.USEREVENT + 1
pg.time.set_timer(ADDENEMY,1000);

player = Player()

enemies  = pg.sprite.Group()
tiros    = pg.sprite.Group()

all_sprites = pg.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemies)
all_sprites.add(tiros)

frase1 = Frase()

running = True
while running:
  # pegar evento do X de fechar janela
  for event in pg.event.get():
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
          
          
  keyp = pg.key.get_pressed()
  screen.fill(white)
  background = pg.image.load("img/bk.jpeg")
  back = pg.transform.scale(background, (800,525))
  screen.blit(back, [0, 0])
  #player.update(keyp)
  #enemies.update(keyp)
  all_sprites.update(keyp)

    # create surface
  contagem = font_small.render(str(cnt_enemy), True, (255,0,0))
  screen.blit(contagem,(5,5))

  for inimigo in enemies:
      if pg.sprite.spritecollideany(inimigo, tiros):
          for tiro in tiros:
              if pg.sprite.spritecollideany(tiro, enemies):
                  tiro.kill()
                  inimigo.kill()
  


  for entity in all_sprites:
    entity.draw(screen)
  

  #pg.display.update()
  pg.display.flip()
  clock.tick(100)


pg.quit()