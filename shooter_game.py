from pygame import *
from random import randint

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

fire_sound = mixer.Sound("fire.ogg")

win_with = 700
win_height = 500

window = display.set_mode((win_with,win_height))
clock = time.Clock()

display.set_caption("Шутер")

background = transform.scale(image.load("galaxy.jpg"),(win_with,win_height))

run = True
finish = False
font.init()
lost = 0
score = 0
font1 = font.Font(None,36)
win = font1.render("YOU WIN" , True , (255, 255 , 255))
lose = font1.render("YOU LOSE" , True , (255, 255 , 255))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = background = transform.scale(image.load(player_image),(size_x,size_y))
        self.player_speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x , self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.player_speed

        if keys[K_d] and self.rect.x < win_with - 20:
            self.rect.x += self.player_speed

    def fire(self):
        bullet = Bullet("bullet.png" , ship.rect.x - 4 , ship.rect.y - 15, 15 , 20 , -10)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.player_speed

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_with - 80)
            self.rect.y =  - 40
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.player_speed
        if self.rect.y < 0:
            self.kill()

ship = Player("rocket.png", 5 , win_height - 100, 8 , 100 , 10)

monsters = sprite.Group()
bullets = sprite.Group()
rocks = sprite.Group()

for i in range(5):
    monster = Enemy("ufo.png", randint(80,win_with - 80), -40, 80 , 50, randint(1,5))
    monsters.add(monster)

    rock = Enemy("ufo.png", randint(80,win_with - 80), -40, 80 , 50, randint(1,5))
    rocks.add(rock)

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
                fire_sound.play()

    if not finish:
        window.blit(background,(0,0))


        ship.update()
        monsters.update()
        bullets.update()
        rocks.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        collides = sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            score += 1
            monster = Enemy("ufo.png", randint(80,win_with - 80), -40, 80 , 50, randint(1,5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= 3:
            finish = True
            window.blit(lose, (200,200))

        if score >= 10:
            finish = True
            window.blit(win, (200,200))

        text = font1.render("Счёт: " + str(score), 1, (255,255,255))
        window.blit(text, (10,20))
        

        text_lose = font1.render("Пропущено: " + str(lost), 1, (255,255,255))
        window.blit(text_lose, (10,50))



        display.update()
    clock.tick(60)
    time.delay(50)
        