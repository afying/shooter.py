from pygame import *
from pygame.locals import *
import random

all_sprites = sprite.Group()
missed_objects = 0
shooted = 0

window = display.set_mode((700, 500))  
display.set_caption("Shooter")

background = transform.scale(image.load("galaxy.jpg"), (700, 500))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (60, 90))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 625:
            self.rect.x += self.speed
    def fire(self):
        pass

class SmartEnemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.image = transform.scale(image.load(player_image), (65, 50))
        self.direction = 1  # 1 = вправо/вниз, -1 = влево/вверх
        self.steps = 0
    
    def update(self, player=None):
        self.steps += 1

        self.rect.y += self.speed * self.direction
        
        global missed_objects 
        if self.rect.y >= 500:
            missed_objects += 1
            self.rect.y = 0
            self.rect.x = random.randint(5, 625)
        '''if (sprite.collide_rect(newbullet, enemy)):
            self.kill'''
            

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.image = transform.scale(image.load(player_image), (20, 30))
        self.direction = -1
        self.steps = 0
    
    def update(self, player=None):
        self.steps -= 1

        self.rect.y += self.speed * self.direction

        if self.rect.y <= -25:
            self.kill()
def restart_game():
    global missed_objects, shooted, all_sprites, bullets, player
    missed_objects = 0
    shooted = 0
    finish = False
    all_sprites.empty()
    bullets.empty()

#player

p_x = 325
p_y = 400

player = Player('rocket.png', p_x, p_y, 10)

#enemy
for i in range (5):
    enemy = SmartEnemy('ufo.png', random.randint(5, 625), 0, random.randint(1, 3))
    all_sprites.add(enemy)

#bullet
#bullet = Bullet('bullet.png', p_x, p_y, 6)
newbullet = Bullet('bullet.png', player.rect.x + 9999, player.rect.y, 6)
bullets = sprite.Group()
#bullets.add(bullet)


game = True
finish = False
clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
shoot_sound = mixer.Sound('fire.ogg') 

font.init()
my_font = font.Font(None, 30)
score = my_font.render(f"Сбито: {shooted}", True, (255, 255, 255))
lose = my_font.render(f"Пропущено: {missed_objects}", True, (255, 255, 255))

myy_font = font.Font(None, 70)
win = myy_font.render('YOU WIN!', True, (255, 230, 0))
fail = myy_font.render('YOU LOSE!', True, (180, 0, 0))

# Параметры кнопки
but_font = font.Font(None, 20)
button_rect = Rect(240, 300, 200, 50)
button_color = (0, 0, 0)
text_color = (255, 255, 255)
text = but_font.render("Нажми для игры снова", True, text_color)

clock = time.Clock()
start_ticks = time.get_ticks()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
            
        # Проверка клика по кнопке (только если игра окончена)
        if e.type == MOUSEBUTTONDOWN and finish:
            if button_rect.collidepoint(e.pos):
                print("Кнопка нажата!")
                # Сброс игры
                missed_objects = 0
                shooted = 0
                start_ticks = time.get_ticks()
                seconds = 0
                finish = False
                all_sprites.empty()
                bullets.empty()
                # Создаем заново
                for i in range(5):
                    enemy = SmartEnemy('ufo.png', random.randint(5, 625), 0, random.randint(1, 3))
                    all_sprites.add(enemy)
                player.rect.x = p_x
                player.rect.y = p_y

        if e.type == KEYDOWN and not finish:
            if e.key == K_SPACE:
                shoot_sound.play()
                newbullet = Bullet('bullet.png', player.rect.x + 20, player.rect.y, 6)
                bullets.add(newbullet)

    seconds = (time.get_ticks() - start_ticks) / 1000

    if finish != True:
        window.blit(background, (0, 0))

        timer = my_font.render(f"Времени прошло:{seconds:.1f}", True, (255, 255, 255))
        window.blit(timer, (0, 25))
        score = my_font.render(f"Сбито: {shooted}", True, (255, 255, 255))
        window.blit(score, (0, 50))
        lose = my_font.render(f"Пропущено: {missed_objects}", True, (255, 255, 255))
        window.blit(lose, (0, 75))

        player.update()
        all_sprites.update()

        all_sprites.draw(window)
        player.reset()

        bullets.update()
        bullets.draw(window)

        hits = sprite.spritecollide(newbullet, all_sprites, True) # True удаляет врага
        for hit in hits:
            shooted += 1
            print("Враг уничтожен!")
            enemy = SmartEnemy('ufo.png', random.randint(5, 625), 0, random.randint(1, 3))
            all_sprites.add(enemy)
        # Условия проигрыша/победы
        if sprite.spritecollide(player, all_sprites, False) or missed_objects >= 3:
            finish = True
        if shooted >= 10:
            finish = True
            
    else:
        # Экран завершения
        window.blit(background, (0, 0)) # Чтобы кнопка не рисовалась поверх мусора
        if shooted >= 10:
            window.blit(win, (225, 225))
        else:
            window.blit(fail, (225, 225))
            
        draw.rect(window, button_color, button_rect)
        window.blit(text, (button_rect.x + 20, button_rect.y + 15))

    display.update()
    clock.tick(FPS)