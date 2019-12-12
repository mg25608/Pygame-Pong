# Start the game via "start.bat" and not this file directly. I mean you CAN, but I created the file for a reason.

import pygame # Main Pygame module
import sys # System module
import xml_parser # My XML parser
import random
import math
import os

os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init() # Initialize pygame

# Get stuff from settings
SettingsXML = xml_parser.XML('settings.xml')

# Gather all settings from the XML
ResolutionSettings = {'Width': SettingsXML.FindByName('setting', 'resolution', 'width'),'Height': SettingsXML.FindByName('setting', 'resolution', 'height')}
ApplicationSettings = {'ShowMouse': SettingsXML.FindByName('setting', 'application', 'show_mouse'), 'Title': SettingsXML.FindByName('setting', 'application', 'title'), 'FPS': int(SettingsXML.FindByName('setting', 'application', 'fps')), 'IsFullscreen': str(SettingsXML.FindByName('setting', 'application', 'fullscreen'))}
SurfaceSettings = {'BackgroundColor': SettingsXML.FindByName('setting', 'surface', 'background_color')}
GameSettings = {'PaddleHeight': SettingsXML.FindByName('setting', 'game', 'paddle_height'), 'PaddleWidth': SettingsXML.FindByName('setting', 'game', 'paddle_width'), 'PaddleSpeed': SettingsXML.FindByName('setting', 'game', 'paddle_movement_speed'), 'BallSpeed': SettingsXML.FindByName('setting', 'game', 'ball_movement_speed'), 'PaddleColor': SettingsXML.FindByName('setting', 'game', 'paddle_color'), 'BallColor': SettingsXML.FindByName('setting', 'game', 'ball_color'), 'BallHeight': SettingsXML.FindByName('setting', 'game', 'ball_height'), 'BallWidth': SettingsXML.FindByName('setting', 'game', 'ball_width'), 'BallRadius': SettingsXML.FindByName('setting', 'game', 'ball_radius')}

# Set display
IsFullscreen = ApplicationSettings['IsFullscreen'].lower()
if IsFullscreen == 'yes':
    Surface = pygame.display.set_mode((int(ResolutionSettings['Width']), int(ResolutionSettings['Height'])), pygame.FULLSCREEN)
else:
    Surface = pygame.display.set_mode((int(ResolutionSettings['Width']), int(ResolutionSettings['Height'])))

# Set title for the game
pygame.display.set_caption(str(ApplicationSettings['Title']))

pygame.mouse.set_visible(1)

# Set mouse visibility
if ApplicationSettings['ShowMouse'].lower() == 'y' or ApplicationSettings['ShowMouse'].lower() == 'true':
    pygame.mouse.set_visible(0)

# Get some colors
Colors = {'black': (0,0,0),'red': (255,0,0),'green': (0,255,0),'blue': (0,0,255),'white': (255,255,255)}

# Set background color (from settings.xml)
try:
    Surface.fill(Colors[SurfaceSettings['BackgroundColor'].lower()])
except Exception as e:
    print("Caught exception:",e)

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([int(GameSettings['BallWidth']), int(GameSettings['BallHeight'])])
        self.image.fill(Colors['white'])
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
        self.speed = 0
        self.x = 0
        self.y = 0
        self.direction = 0
        self.width = 10
        self.height = 10
        self.reset()

    def reset(self):
        self.x = self.screenwidth / 2
        self.y = self.screenheight / 2
        self.speed = int(GameSettings['BallSpeed'])
        self.direction = random.randrange(-45,45)
        if random.randrange(2) == 0 :
            self.direction += 180

    def bounce(self,diff):
        self.direction = (180-self.direction)%360
        self.direction -= diff

    def update(self):
        direction_radians = math.radians(self.direction)
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)
        if self.y < 0:
            self.reset()
        if self.y > self.screenheight:
            self.reset()
        self.rect.x = self.x
        self.rect.y = self.y
        if self.x <= 0:
            self.direction = (360-self.direction)%360
        if self.x > self.screenwidth-self.width:
            self.direction = (360-self.direction)%360

class Player(pygame.sprite.Sprite):
    def __init__(self, player, y_pos):
        super().__init__()
        self.width = int(GameSettings['PaddleWidth'])
        self.height = int(GameSettings['PaddleHeight'])
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(Colors[GameSettings['PaddleColor'].lower()])
        self.player = player
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
        self.rect.x = 0
        self.rect.y = y_pos

    def update(self, side):
        CanGoLeft = True
        CanGoRight = True

        if self.rect.x > self.screenwidth - self.width:
            CanGoRight = False
        if self.rect.x <= 0:
            CanGoLeft = False

        if side == 'right':
            if CanGoRight == True:
                self.rect.x = self.rect.x + int(GameSettings['PaddleSpeed'])
        elif side == 'left':
            if CanGoLeft == True:
                self.rect.x = self.rect.x - int(GameSettings['PaddleSpeed'])

score1 = 0
score2 = 0

font = pygame.font.Font(None, 36)

background = pygame.Surface(Surface.get_size())

ball = Ball()
balls = pygame.sprite.Group()
balls.add(ball)

player1 = Player('player1', (int(ResolutionSettings['Height']) - int(GameSettings['PaddleHeight']))-5)
player2 = Player('player2', 25)

movingsprites = pygame.sprite.Group()
movingsprites.add(player1)
movingsprites.add(player2)
movingsprites.add(ball)

clock = pygame.time.Clock()
done = False
exit_program = False

player1_side = "still"
player2_side = "still"

while not exit_program:

    Surface.fill(Colors[SurfaceSettings['BackgroundColor'].lower()])

    for event in pygame.event.get():
        # Update the players if they exist
        keys = pygame.key.get_pressed()
        player1_side = "still"
        player2_side = "still"
        try:
            if keys[pygame.K_LEFT]:
                player2_side = 'left'
            if keys[pygame.K_RIGHT]:
                player2_side = 'right'
            if keys[pygame.K_d]:
                player1_side = 'right'
            if keys[pygame.K_a]:
                player1_side = 'left'
        except Exception as e:
            print("Caught exception:",e)

        # Exit
        if event.type == pygame.QUIT:
            exit_program = True

    if abs(score1 - score2) > 3:
        done = True

    if not done:
        player1.update(player1_side)
        player2.update(player2_side)
        ball.update()

    if done:
        text = font.render("Game Over", 1, (200, 200, 200))
        textpos = text.get_rect(centerx=background.get_width()/2)
        textpos.top = 50
        Surface.blit(text, textpos)

    if pygame.sprite.spritecollide(player1, balls, False):
        diff = (player1.rect.x + player1.width/2) - (ball.rect.x+ball.width/2)
        #ball.y = 570
        ball.bounce(diff)

    if pygame.sprite.spritecollide(player2, balls, False):
        #diff = (player2.rect.x + player2.width/2) - (ball.rect.x+ball.width/2)
        #ball.y = 40
        diff = -ball.direction
        ball.bounce(diff)

    if ball.y <= 5:
        # Give player 2 a point
        score2 += 1
    if ball.y >= int(ResolutionSettings['Height']):
        # Give player 1 a point
        score1 += 1

    scoreprint = "Player 1: "+str(score1)
    text = font.render(scoreprint, 1, Colors['white'])
    textpos = (0, 0)
    Surface.blit(text, textpos)

    scoreprint = "Player 2: "+str(score2)
    text = font.render(scoreprint, 1, Colors['white'])
    textpos = (300, 0)
    Surface.blit(text, textpos)

    movingsprites.draw(Surface)
    clock.tick(ApplicationSettings['FPS'])
    pygame.display.update()

pygame.quit()
