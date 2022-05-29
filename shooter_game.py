from pygame import *
from random import randint
main_win = display.set_mode((750, 500))
galaxy = image.load("galaxy.jpg")
galaxy = transform.scale(galaxy,(750, 500))
win_x_length = 750
win_y_length = 500
score = 0
goal = 10
lost = 0
max_lost = 5

run = True

class GameSprite(sprite.Sprite):
    def __init__ (self, file, x_length, y_length, pos_x, pos_y, speed):
        super().__init__()
        self.image = transform.scale(image.load(file), (250,250))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.speed = speed
        self.x_length = x_length
        self.y_length = y_length
    def draw_sprite(self):
        main_win.blit(self.image, (self.rect.x, self.rect.y))
class Rocket(GameSprite):
    def move_key(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_x_length:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", 25, 50, self.rect.centerx, self.rect.top, 10)
        Bullet_group.add(bullet)
rocket = Rocket("rocket.png", 80, 100, 75, win_x_length / 2, 2.5)
class UFO(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_y_length:
            lost += 1
            self.rect.x = randint(0, win_x_length - self.x_length)
            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
Bullet_group = sprite.Group()

UFO_group = sprite.Group()
for i in range(1,5):
    ufo = UFO("ufo.png", 80, 80, randint(0,win_x_length - 375), 0, randint(1,5))
    UFO_group.add(ufo)

font.init()
font1 = font.Font(None, 50)
win_text = font1.render("You Won, L + Ratio", True, (255, 255, 255))
font2 = font.Font(None, 50)
lose_text = font2.render("You Lose, L + Bozo", True, (255, 255, 255))

clock = time.Clock()
FPS = 69

while run:
    for e in event.get():
            if e.type == QUIT:
                run = False
            elif e.type == KEYDOWN:
                if e.key == K_SPACE:
                    rocket.fire()
    main_win.blit(galaxy,(0, 0))
    rocket.draw_sprite()
    Bullet_group.draw(main_win)
    Bullet_group.update()
    rocket.move_key()
    UFO_group.draw(main_win)
    UFO_group.update()
    collides = sprite.groupcollide(Bullet_group, UFO_group, True, True)
    if sprite.spritecollide(rocket, UFO_group, False) or lost >= max_lost:
        main_win.blit(lose_text,(200,200))
    if score >= goal:
        main_win.blit(win_text,(200,200))
    for c in collides:
        score += 1
        UFO = UFO_group.draw(main_win)
        UFO_group.add()
    display.update()