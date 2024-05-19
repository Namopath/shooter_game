#Create your own shooter

from pygame import *
from random import randint

width = 700
height = 500
window = display.set_mode((width,height))
background = transform.scale(image.load('galaxy.jpg'), (width,height))
display.set_caption("Shooter game")
player = 'rocket.png'
enemy = 'ufo.png'
bullet = 'bullet.png'
asteroid_sprite = 'asteroid.png'

font.init()

font1 = font.SysFont("Arial", 36)
font2 = font.SysFont("Arial", 80)
lost = font2.render("You lost", True, (180,0,0))
win = font2.render("You won", True, (255,255,255))
run = True
clock = time.Clock()


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
shot = mixer.music.load('fire.ogg')

miss = 0
score = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < width-80:
            self.rect.x += self.speed
    def fire(self):
        bullet1 = Bullet(bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet1)
class Enemy(GameSprite):
    
    def update(self):
        self.rect.y += self.speed
        global miss
        if self.rect.y > height:
            self.rect.x = randint(80,width-80)
            self.rect.y = 0
            miss += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
        
bullets = sprite.Group()       

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy(enemy, randint(80,width-80), -40, 80, 50, randint(1,5))
    monsters.add(monster) 

asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy(asteroid_sprite, randint(80,width-80), -40, 80, 50, randint(1,7))
    asteroids.add(asteroid)

rocket = Player(player, 5, height-100, 80, 100, 10)

finish = False




while run:
    
    
    
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
        
                rocket.fire()
    if not finish:
        window.blit(background, (0,0))
        
        text_loss = font1.render('Missed:' + str(miss), 1, (255,255,255))
        text_score = font1.render('Score:'+ str(score), 1, (255,255,255))
        window.blit(text_loss, (10,20))
        window.blit(text_score, (10,40))
        rocket.update()
        bullets.update()
        monsters.update()
        asteroids.update()
        rocket.reset()
        asteroids.draw(window)
        monsters.draw(window)
        bullets.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        asteroid_collide = sprite.spritecollide(rocket, asteroids, False)
        player_collide = sprite.spritecollide(rocket, monsters, False)
        
        for i in collides:
            score += 1
            monster = Enemy(enemy, randint(80,width-80), -40, 80, 50, randint(1,5))
            monsters.add(monster)
        
        if miss >= 10:
            finish = True
            window.blit(lost, (200,200))
            
        if score >= 10:
            finish = True
            window.blit(win, (200,200))
        
        if player_collide or asteroid_collide:
            finish = True
            window.blit(lost, (200,200))
    
        
        
        display.update()
    
        
    clock.tick(60)
    
    
