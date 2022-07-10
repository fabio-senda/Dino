import pygame
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGH = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGH))

pygame.display.set_caption('Dino, cactos e passaros')
icon = pygame.image.load('images/dinossaur.png')
pygame.display.set_icon(icon)

dino_move0 = pygame.image.load('images/dinossaur.png')
dino_move0 = pygame.transform.scale(dino_move0, (100, 100))
dino_move1 = pygame.image.load('images/dinossaur_move.png')
dino_move1 = pygame.transform.scale(dino_move1, (100, 100))

passaro_voando0 = pygame.image.load('images/passaro.png')
passaro_voando0 = pygame.transform.scale(passaro_voando0, (100, 69))
passaro_voando1 = pygame.image.load('images/passaro_voando.png')
passaro_voando1 = pygame.transform.scale(passaro_voando1, (100, 69))
passaro_morto = pygame.image.load('images/passaro_morto.png')
passaro_morto = pygame.transform.scale(passaro_morto, (100, 69))

cacto = pygame.image.load('images/cacto.png')
cacto = pygame.transform.scale(cacto, (100, 100))
cacto_quebrado = pygame.image.load('images/cacto_quebrado.png')
cacto_quebrado = pygame.transform.scale(cacto_quebrado, (100, 100))

fundo = pygame.image.load('images/fundo.png')

obstacles = ([cacto, cacto_quebrado], [passaro_voando0, passaro_voando1, passaro_morto])


def score():
    global pontos, game_speed
    font = pygame.font.SysFont('arial', 20)
    pontos += 1
    if pontos % 100 == 0:
        game_speed += 1
    text = font.render("Pontos: " + str(pontos), True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (700, 10)
    screen.blit(text, textRect)


def background():
    global fundo_x
    image_width = fundo.get_width()
    screen.blit(fundo, (fundo_x, 0))
    screen.blit(fundo, (fundo_x - image_width, 0))
    if fundo_x >= image_width:
        screen.blit(fundo, (fundo_x - image_width, 0))
        fundo_x = 0
    fundo_x += game_speed


class Dino:
    X_POS = 610
    Y_POS = 440
    VEL_PULO = 8.5

    def __init__(self):
        self.img_correr = [dino_move0, dino_move1]
        self.img_pular = dino_move0

        self.dino_correndo = True
        self.dino_pulando = False

        self.vel_pulo = self.VEL_PULO
        self.step_index = 0
        self.imagem = self.img_correr[0]
        self.dino_hitbox = self.imagem.get_rect()
        self.dino_hitbox.x = self.X_POS
        self.dino_hitbox.y = self.Y_POS
        self.dino_hitbox.width = 80

    def update(self, userInput):
        if (userInput[pygame.K_UP] or userInput[pygame.K_SPACE]) and not self.dino_pulando:
            self.dino_correndo = False
            self.dino_pulando = True

        if self.dino_correndo:
            self.correndo()
        elif self.dino_pulando:
            self.pulando()

        if self.step_index >= 10:
            self.step_index = 0

    def correndo(self):
        self.imagem = self.img_correr[self.step_index // 5]
        self.dino_hitbox.x = self.X_POS
        self.dino_hitbox.y = self.Y_POS
        self.step_index += 1

    def pulando(self):
        self.imagem = self.img_pular
        self.dino_hitbox.y -= self.vel_pulo * 4
        self.vel_pulo -= 0.8
        if self.vel_pulo < -self.VEL_PULO:
            self.dino_pulando = False
            self.dino_correndo = True
            self.vel_pulo = self.VEL_PULO
            self.dino_hitbox.y = self.Y_POS

    def draw(self, screen):
        screen.blit(self.imagem, (self.dino_hitbox.x - 10, self.dino_hitbox.y))


class PassaroNuvem:
    def __init__(self):
        self.x = -random.randint(100, 1000)
        self.y = random.randint(15, 150)
        self.img_voando = [passaro_voando0, passaro_voando1]
        self.image = passaro_voando0
        self.width = self.image.get_width()
        self.step_index = 0

    def update(self):
        self.x += game_speed
        if self.step_index >= 10:
            self.step_index = 0
        self.image = self.img_voando[self.step_index // 5]
        if self.x > SCREEN_WIDTH:
            self.x = -random.randint(100, 1000)
            self.y = random.randint(15, 150)
        self.step_index += 1

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class Obstaculo:
    def __init__(self, tipo):
        self.image = obstacles[tipo]
        self.tipo = tipo
        self.rect = self.image[self.tipo].get_rect()
        self.rect.x = -100
        self.rect.y = (random.randint(1, 2) + 2) * 110
        self.rect.height = 100
        self.rect.width = 50
        self.step_index = 0

    def update(self):
        self.rect.x += game_speed
        if self.rect.x >= SCREEN_WIDTH:
            obstaculos.pop()

    def draw(self, screen):
        if self.step_index == 10:
            self.step_index = 0
        if self.tipo == 0:
            self.rect.y = 450
            screen.blit(self.image[0], (self.rect.x-20, self.rect.y))
        else:
            screen.blit(self.image[self.step_index // 5], (self.rect.x-5, self.rect.y))
        self.step_index += 1

    def batida(self):
        if self.tipo == 0:
            screen.blit(self.image[1], (self.rect.x, self.rect.y))
        else:
            screen.blit(self.image[2], (self.rect.x, self.rect.y))


def main():
    global game_speed, fundo_x, pontos, obstaculos, run
    game_speed = 10
    running = True
    clock = pygame.time.Clock()
    player = Dino()
    fundo_x = 0
    passaros = list()
    qtd_passaros = 5
    pontos = 0
    obstaculos = list()
    death_count = 0

    for i in range(qtd_passaros):
        passaros.append(PassaroNuvem())

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        screen.fill((100, 100, 100))
        userInput = pygame.key.get_pressed()

        background()
        score()

        if len(obstaculos) == 0:
            if random.randint(0, 1) == 0:
                obstaculos.append(Obstaculo(0))
            elif random.randint(0, 1) == 0:
                if pontos > 1000:
                    obstaculos.append(Obstaculo(1))
        #pygame.draw.rect(screen, (255, 0, 0), player.dino_hitbox, 2)
        for obstacle in obstaculos:
            obstacle.update()
            obstacle.draw(screen)
            #pygame.draw.rect(screen, (255, 0, 0), obstacle.rect, 2)
            if player.dino_hitbox.colliderect(obstacle.rect):
                background()
                for passaro in passaros:
                    passaro.draw(screen)
                player.draw(screen)
                obstacle.batida()
                pygame.display.update()
                #pygame.draw.rect(screen, (255, 0, 0), player.dino_hitbox, 2)
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        player.update(userInput)
        player.draw(screen)

        for passaro in passaros:
            passaro.update()
            passaro.draw(screen)

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points, run
    run = True
    while run:
        screen.fill((100, 100, 100))
        font = pygame.font.SysFont('arial', 30)

        if death_count == 0:
            text = font.render("Pressione alguma tecla para começar", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Pressione alguma tecla para começar", True, (0, 0, 0))
            score = font.render("Sua pontação: " + str(pontos), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGH //2 + 50)
            screen.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGH // 2)
        screen.blit(text, textRect)
        screen.blit(dino_move1, (SCREEN_WIDTH//2 - 50, SCREEN_HEIGH//2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
            elif event.type == pygame.KEYDOWN:
                main()

menu(death_count = 0)
