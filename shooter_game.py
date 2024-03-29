
from pygame import *
from random import randint
from time import time as timer

class Celestial(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = speed #скорость

        #хитбокс
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class SpaceShip(Celestial):
    def move(self):
        action = key.get_pressed()
        if action[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        elif action[K_d] and self.rect.x < 1100:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('111.jpg', self.rect.centerx, self.rect.top, 40, 50, -20)
        bullets.add(bullet)


class Enemy(Celestial):
    def update(self):
        global missed_enemy
        self.rect.y += self.speed
        if self.rect.y >= 700:
            self.rect.y = 0
            self.rect.x = randint(0, width-100)
            self.speed = randint(4, 8)
            missed_enemy += 1


class Bullet(Celestial):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 0:
            self.kill()


bullets = sprite.Group()

width = 1200
height = 700
window = display.set_mode((width, height))
display.set_caption('War Thunder 3')
background = transform.scale(image.load('444.jpeg'), (width, height))

mixer.init()
mixer.music.load('music.mp3')
mixer.music.play()
shoot_sound = mixer.Sound('fire.ogg')
player = SpaceShip('232.jpeg', 600, 570, 100, 100, 25)
aliens = sprite.Group()
font.init()
font2 = font.SysFont('Arial', 40)
font1 = font.SysFont('Arial', 100)
win = font1.render('да ты снайпер', True, (0, 0,250))
lose = font1.render('ну ты лось', True, (0, 0, 0))
crash = font1.render("Столкновение", True, (255, 0, 0))

for i in range(10):
    alien = Enemy('323.jpg', randint(0, width - 100), -50, 80, 80, randint(4, 8))
    aliens.add(alien)



asteroids = sprite.Group()
for i in range(3):
    aster = Enemy('asteroid.png', randint(0, width - 100), -50, 100, 100, randint(2, 6))
    asteroids.add(aster)



lose_score = 3
hp = 3
score = 0
missed_enemy = 0
reload_capacity = False
count_fire = 0
game = True
run = True
while game == True:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if count_fire < 8 and reload_capacity == False:
                    count_fire += 1
                    player.fire()
                    shoot_sound.play()
                elif count_fire >= 8 and reload_capacity == False:
                    reload_time = timer()
                    reload_capacity = True





    if run == True:
        window.blit(background, (0, 0))
        player.reset()
        player.move()
        aliens.update()
        aliens.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)


        if reload_capacity == True:
            temp_time = timer()
            if temp_time - reload_time < 2:
                rel_text = font2.render('Перезарядка орудия...', True, (255, 255, 255))
                window.blit(rel_text, (400, 650))
            else:
                count_fire = 0
                reload_capacity = False




        collides = sprite.groupcollide(aliens, bullets, True, True)
        for i in collides:
            score += 1
            alien = Enemy('323.jpg', randint(0, width - 100), -50, 80, 80, randint(4, 8))
            aliens.add(alien)

        if sprite.spritecollide(player, aliens, False) or sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(player, aliens, True)
            sprite.spritecollide(player, asteroids, True)
            hp -= 1

        if hp == 0 or missed_enemy >= lose_score:
            run = False
            window.blit(lose, (500, 300))

        if score >= 10:
            run = False
            window.blit(win, (500, 300))
 


        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render("Пропущено: " + str(missed_enemy), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        text_life = font1.render('Кол-во жизней' + str(hp), True, (237, 71, 151))
        window.blit(text_lose, (10, 50))
        window.blit(text_life, (10, 80))



        display.update()

    time.delay(60)


