#Создай собственный Шутер!

from pygame import *
from random import *
from time import time as timer
font.init()

window = display.set_mode((700, 500))
display.set_caption('Шутер')
galaxy = transform.scale(image.load('galaxy.jpg'), (700, 500))
game = True
finish = False
Fps = 60
clock = time.Clock()
font1 = font.SysFont('Times', 36)
font2 = font.SysFont('Times', 56)
font3 = font.SysFont('Times', 25)
lost = 0
score = 0
num_fire = 0
life = 5
rel_time = False
win = font2.render('YOU WIN!', True, (255, 255, 0))
lose = font2.render('YOU LOSE!', True, (255, 0, 0))
rel = font3.render('Wait, reload...', True, (255, 0, 0))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w, h):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 10:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 650:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 5, 5, 15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            global lost
            self.rect.x = randint(0, 630)
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y == 0:
            self.kill()

class Aster(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            global lost
            self.rect.x = randint(0, 630)

rocket = Player('rocket.png', 350, 420, 10, 50, 70)

monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(4):
    enemy = Enemy('ufo.png', randint(0, 630), 0, randint(1, 2),70, 40)
    monsters.add(enemy)
for i in range(2):
    asteroid = Aster('asteroid.png', randint(0, 630), 0, randint(1, 2),60, 60)
    asteroids.add(asteroid)



while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    rocket.fire()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    time1 = timer()
                

    if finish != True:
        window.blit(galaxy, (0, 0))
        rocket.update()
        rocket.reset()
        monsters.draw(window)
        monsters.update()
        text_lost = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        text_lost1 = font1.render('Счёт: ' + str(score), 1, (255, 255, 255))
        window.blit(text_lost, (10, 50))
        window.blit(text_lost1, (10, 20))
        bullets.update()
        bullets.draw(window)
        asteroids.draw(window)
        asteroids.update()
        sprites_list = sprite.spritecollide(rocket, monsters, False)
        monsters_list = sprite.groupcollide(monsters, bullets, True, True)
        asteroids_list = sprite.spritecollide(rocket, asteroids, False)
        if rel_time == True:
            time2 = timer()
            if time2 - time1 >= 3:
                num_fire = 0
                rel_time = False
            else:
                window.blit(rel, (320, 470))
        if len(sprites_list) > 0 :
            life -= 1
            
        if len(asteroids_list) > 0:
            life -= 1
            
        if life< 1 or lost > 100:
            finish = True
            window.blit(lose, (250, 240))

        for s in monsters_list:
            score += 1
            enemy = Enemy('ufo.png', randint(0, 630), 0, randint(2, 5),70, 30)
            monsters.add(enemy)
        if score >6:
            finish = True
            window.blit(win, (250, 240))

    display.update()
    clock.tick(Fps)