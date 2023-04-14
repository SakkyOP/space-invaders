import pygame as pg
import random

width,height = 800,600

pg.init()

font = pg.font.Font("Minecraft.ttf",20)

render = {
    "player": pg.image.load("spaceship.png"),
    "enemy" : pg.image.load("enemy.png"),
    "enemy_hit" : pg.image.load("enemy_hit.png"),
    "bullet" : pg.image.load("bullet.png")
}

pg.display.set_caption("Space Invaders!")
screen = pg.display.set_mode((width,height))

class Player:
    
    def __init__(self,x,y,img):
        self.x = x
        self.y = y
        self.img = img
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.left = False
        self.right = False
        self.fire = False
        self.score = 0
    
    def draw(self):
        if not gameover:
            screen.blit(self.img,(self.x,self.y))
        
    def move(self):
        if self.left:
            if (self.x > width/10):
                self.x -= width/50
        if self.right:
            if (self.x+self.width < (width-width/10)):
                self.x += width/50

class Enemy:
    
    def __init__(self,x,y,img):
        self.x = x
        self.y = y
        self.img = img
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.velocity = 0.5
        self.hp = 50

    def draw(self):
        screen.blit(self.img,(self.x,self.y))
    
    def hit(self,hp):
        self.hp -= hp

    def move(self):
        if not gameover:
            self.y += self.velocity

class Bullet:
    
    def __init__(self,x,y,img):
        self.x = x
        self.y = y
        self.img = img
        self.width = self.img.get_width()
        self.height = self.img.get_height()
    
    def move(self):
        self.y -= height/90
        
    def draw(self):
        if self.y>0:
            screen.blit(self.img,(self.x,self.y))
    
    def collision(self,object):
        if (self.y > object.y) and (self.y < (object.y+object.height)) and (self.x > object.x) and (self.x < (object.x+object.width)):
            return True
        # if (self.x > object.x) and (self.x < (object.x+object.width)):
        #     return True
        return False
  
def reDraw():
    
    screen.fill((0,0,0))
    
    for enemy in enemies:
        enemy.draw()
    
    spaceship.draw()
    for bullet in projectiles:
        bullet.draw()
    
    text = font.render("Score: "+str(spaceship.score),True,(255,255,255))
    textRect = text.get_rect()
    textRect.center = width-width/8,height/20
    
    screen.blit(text,textRect)
    
    if gameover:
        game_over_text = font.render("Game Over!",True,(255,255,255))
        textRect = game_over_text.get_rect()
        textRect.center = (width//2,height//2)
        screen.blit(game_over_text,textRect)
        
    pg.display.flip()
    





spaceship = Player(width//2,height-height//5,pg.transform.rotozoom(render["player"],0,0.13))

enemies = []

projectiles = []

level = 0

run = True
gameover = False

clock = pg.time.Clock()
    

  

while run:  
    
    dt = clock.tick(30)
    
    # if len(enemies)<4:
    #     enemies.append(Enemy(random.randrange(width//10,width-width//5),random.randrange(height//10,height//3),pg.transform.rotozoom(render["enemy"],0,0.1)))
    
    if len(enemies) == 0:
        level += 1
        for x in range(width//10,width-width//10,width//8):
            for y in range(height//20,height-height//2,height//level):
                enemies.append(Enemy(x,y,pg.transform.rotozoom(render["enemy"],0,0.1)))
    
        
    for event in pg.event.get():
        # print(event)
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.KEYDOWN:
            if event.key in [pg.K_LEFT, pg.K_a]:
                spaceship.left,spaceship.right = True,False
            elif event.key in [pg.K_RIGHT, pg.K_d]:
                spaceship.right , spaceship.left = True,False
            if event.key == pg.K_SPACE:
                spaceship.fire = True
            
        elif event.type == pg.KEYUP:
            if event.key in [pg.K_RIGHT, pg.K_d]:
                spaceship.right = False
            elif event.key in [pg.K_LEFT, pg.K_a]:
                spaceship.left = False
            if event.key == pg.K_SPACE:
                spaceship.fire = False
    
    if spaceship.fire and len(projectiles)<20:
        projectiles.append(Bullet(spaceship.x+spaceship.width//2,spaceship.y,pg.transform.rotozoom(render["bullet"],0,0.03)))
        spaceship.fire = False
    
    # if len(projectiles)>10:
    #     projectiles = []
    
    
    spaceship.move()
    for enemy in enemies:
        enemy.move()
        if (enemy.y > spaceship.y) and (enemy.y > (spaceship.y-spaceship.height)):
            gameover = True
    
        
    reDraw()
    
    for bullet in projectiles:
        bullet.move()
        if bullet.y<width/15:
            projectiles.remove(bullet)
        for enemy in enemies:
            if bullet.collision(enemy):
                enemy.hit(50)
                # if bullet in projectiles:
                #     projectiles.remove(bullet)
                projectiles.remove(bullet)
            if enemy.hp == 0:
                enemies.remove(enemy)
                spaceship.score += 10
