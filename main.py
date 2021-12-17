import pygame, sys, random
from pygame import mixer

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()

# for icon
icon = pygame.image.load('pong.png')
pygame.display.set_caption('Pong Game')
pygame.display.set_icon(icon)



class Player:
    def __init__(self):
        self.player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
        self.player_speed = 0

    def draw_player(self):
        pygame.draw.rect(screen, (242, 51, 22), self.player)

    def player_movement(self):
        self.player.y += self.player_speed
        if self.player.top <= 0:
            self.player.top = 0
        if self.player.bottom >= screen_height:
            self.player.bottom = screen_height


class Opponent:
    def __init__(self):
        self.opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)
        self.opponent_speed = 10

    def draw_opponent(self):
        pygame.draw.rect(screen, (38, 68, 237), self.opponent)


class Game():
    def __init__(self):
        self.score_time = True
        self.playing = False


class Font:
    def __init__(self):
        self.score_font = pygame.font.Font('Trailer Park Girl.otf', 32)
        self.player_font = pygame.font.Font('Trailer Park Girl.otf', 42)
        self.opponent_font = pygame.font.Font('Trailer Park Girl.otf', 42)



class Sound:
    def __init__(self):
        self.sound = mixer.Sound('collision.mp3')
        self.score = mixer.Sound('score_sound.mp3')


class Ball:
    def __init__(self):
        self.ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
        self.ball_change_X = 7 * random.choice((-1, 1))
        self.ball_change_Y = 7 * random.choice((-1, 1))
        self.player = Player()
        self.opponent = Opponent()
        self.font = Font()
        self.game = Game()
        self.sounds = Sound()
        self.opponent_score = 0
        self.player_score = 0
        self.player_text = self.font.score_font.render(f"{self.player_score}", False, (242, 51, 22))
        self.opponent_text = self.font.score_font.render(f"{self.opponent_score}", False, (38, 68, 237))

    def draw_ball(self):
        pygame.draw.ellipse(screen, (200, 200, 200), self.ball)

    def ball_movement(self):
        self.ball.x += self.ball_change_X
        self.ball.y += self.ball_change_Y
        if self.ball.top <= 0 or self.ball.bottom >= screen_height:
            self.ball_change_Y *= -1
        if self.ball.left <= 0:
            mixer.Sound.play(self.sounds.score)
            self.player_score += 1
            self.game.score_time = pygame.time.get_ticks()
        if self.ball.right >= screen_width:
            mixer.Sound.play(self.sounds.score)
            self.opponent_score += 1
            self.game.score_time = pygame.time.get_ticks()
        if self.ball.colliderect(self.player.player) and self.ball_change_X > 0:
            mixer.Sound.play(self.sounds.sound)
            if abs(self.ball.right - self.player.player.left) < 10:
                self.ball_change_X *= -1
            elif abs(self.ball.bottom - self.player.player.top) < 10 and self.ball_change_Y > 0:
                self.ball_change_Y *= -1
            elif abs(self.ball.top - self.player.player.bottom) < 10 and self.ball_change_Y < 0:
                self.ball_change_Y *= -1
        if self.ball.colliderect(self.opponent.opponent) and self.ball_change_X < 0:
            mixer.Sound.play(self.sounds.sound)
            if abs(self.ball.left - self.opponent.opponent.right) < 10:
                self.ball_change_X *= -1
            elif abs(self.ball.bottom - self.opponent.opponent.top) < 10 and self.ball_change_Y > 0:
                self.ball_change_Y *= -1
            elif abs(self.ball.top - self.opponent.opponent.bottom) < 10 and self.ball_change_Y < 0:
                self.ball_change_Y *= -1

    def ball_restart(self):
        current_time = pygame.time.get_ticks()
        self.ball.center = (screen_width / 2, screen_height / 2)
        if current_time - self.game.score_time < 700:
            three = self.font.score_font.render("3", False, (200, 200, 200))
            screen.blit(three, (screen_width / 2 - 10, screen_height / 2 + 20))

        if 700 < current_time - self.game.score_time < 1400:
            two = self.font.score_font.render("2", False, (200, 200, 200))
            screen.blit(two, (screen_width / 2 - 10, screen_height / 2 + 20))
        if 1400 < current_time - self.game.score_time < 2100:
            one = self.font.score_font.render("1", False, (200, 200, 200))
            screen.blit(one, (screen_width / 2 - 10, screen_height / 2 + 20))

        if current_time - self.game.score_time < 2100:
            self.ball_change_X, self.ball_change_Y = 0, 0
        else:
            self.ball_change_Y = 7 * random.choice((-1, 1))
            self.ball_change_X = 7 * random.choice((-1, 1))
            self.game.score_time = None

    def opponent_movement(self):
        if self.opponent.opponent.top < self.ball.y:
            self.opponent.opponent.top += self.opponent.opponent_speed
        if self.opponent.opponent.bottom > self.ball.y:
            self.opponent.opponent.bottom -= self.opponent.opponent_speed

        if self.opponent.opponent.top <= 0:
            self.opponent.opponent.top = 0
        if self.opponent.opponent.bottom >= screen_height:
            self.opponent.opponent.bottom = screen_height

    def game_over(self):
        if self.opponent_score == 10:
            wins = self.font.opponent_font.render("!!!! Opponent Wins !!!!", True, (51, 122, 214))
            screen.blit(wins, (20, screen_height / 2 - 200))
            self.score_time = None
            self.ball.center = (screen_width / 2, screen_height / 2)
            self.playing = True

        if self.player_score == 10:
            wins = self.font.player_font.render("!!!! Player Wins !!!!", True, (242, 51, 22))
            screen.blit(wins, (screen_width / 2 + 50, screen_height / 2 - 200))
            self.score_time = None
            self.ball.center = (screen_width / 2, screen_height / 2)
            self.playing = True

    def show_player_score(self):
        screen.blit(self.player_text, (screen_width / 2 + 20, screen_height / 2))

    def show_opponent_score(self):
        screen.blit(self.opponent_text, (screen_width / 2 - 40, screen_height / 2))


ball = Ball()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ball.player.player_speed = -10
            if event.key == pygame.K_DOWN:
                ball.player.player_speed += 10

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                ball.player.player_speed += 10
            if event.key == pygame.K_DOWN:
                ball.player.player_speed -= 10

    # Animations
    ball.ball_movement()
    ball.opponent_movement()
    ball.player.player_movement()
    # Visuals
    screen.fill((31, 31, 31))

    ball.player.draw_player()
    ball.opponent.draw_opponent()
    ball.draw_ball()
    pygame.draw.aaline(screen, (200, 200, 200), (screen_width / 2, 0), (screen_width / 2, screen_height))


    if ball.game.score_time:
        ball.ball_restart()
    ball.game_over()
    player_text = ball.font.score_font.render(f"{ball.player_score}", False, (242, 51, 22))
    screen.blit(player_text, (screen_width / 2 + 20, screen_height / 2))
    opponent_text = ball.font.score_font.render(f"{ball.opponent_score}", False, (38, 68, 237))
    screen.blit(opponent_text, (screen_width / 2 - 40, screen_height / 2))

    pygame.display.update()
    clock.tick(100)
