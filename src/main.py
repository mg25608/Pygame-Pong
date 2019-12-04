# Start the game via "start.bat" and not this file directly. I mean you CAN, but I created the file for a reason.

import pygame # Main Pygame module
import sys # System module
import xml_parser # My XML parser

pygame.init() # Initialize pygame

# Get stuff from settings
SettingsXML = xml_parser.XML('settings.xml')

# Gather all settings from the XML
ResolutionSettings = {'Width': SettingsXML.FindByName('setting', 'resolution', 'width'),'Height': SettingsXML.FindByName('setting', 'resolution', 'height')}
ApplicationSettings = {'Title': SettingsXML.FindByName('setting', 'application', 'title'), 'FPS': int(SettingsXML.FindByName('setting', 'application', 'fps')), 'IsFullscreen': str(SettingsXML.FindByName('setting', 'application', 'fullscreen'))}
SurfaceSettings = {'BackgroundColor': SettingsXML.FindByName('setting', 'surface', 'background_color')}
GameSettings = {'PaddleHeight': SettingsXML.FindByName('setting', 'game', 'paddle_height'), 'PaddleWidth': SettingsXML.FindByName('setting', 'game', 'paddle_width'), 'PaddleSpeed': SettingsXML.FindByName('setting', 'game', 'paddle_movement_speed'), 'BallShape': SettingsXML.FindByName('setting', 'game', 'ball_shape'), 'BallSpeed': SettingsXML.FindByName('setting', 'game', 'ball_movement_speed'), 'PaddleColor': SettingsXML.FindByName('setting', 'game', 'paddle_color'), 'BallColor': SettingsXML.FindByName('setting', 'game', 'ball_color'), 'BallHeight': SettingsXML.FindByName('setting', 'game', 'ball_height'), 'BallWidth': SettingsXML.FindByName('setting', 'game', 'ball_width'), 'BallRadius': SettingsXML.FindByName('setting', 'game', 'ball_radius')}

# Set display
IsFullscreen = ApplicationSettings['IsFullscreen'].lower()
if IsFullscreen == 'yes':
    Surface = pygame.display.set_mode((int(ResolutionSettings['Width']), int(ResolutionSettings['Height'])), pygame.FULLSCREEN)
else:
    Surface = pygame.display.set_mode((int(ResolutionSettings['Width']), int(ResolutionSettings['Height'])))

# Set title for the game
pygame.display.set_caption(str(ApplicationSettings['Title']))

# Get some colors
Colors = {'black': (0,0,0),'red': (255,0,0),'green': (0,255,0),'blue': (0,0,255),'white': (255,255,255)}

# Set background color (from settings.xml)
try:
    Surface.fill(Colors[SurfaceSettings['BackgroundColor'].lower()])
except Exception as e:
    print("Caught exception:",e)

# Classes
class Draw:
    def __init__(self, surface):
        print("Initializing draw for object")
        self.surface = surface
    def rect(self, color, x,y,w,h, thickness, fill):
        try:
            if self.surface != None:
                print("Drawing a rectangle with sizes (X:{}, Y:{}, W:{}, H:{})".format(x,y,w,h))
                this = pygame.draw.rect(self.surface, color, (x,y,w,h), thickness)
                if fill == True:
                    # Fill using a new surface
                    base = pygame.display.get_surface()
                    base.fill(color, this)
            else:
                raise Exception('Invalid surface, possible bad initialization')
        except Exception as e:
            print("Caught exception:",e)
        finally:
            print("Drawing step complete")
    def circle(self, color, x,y, radius, thickness):
        try:
            if self.surface != None:
                print("Drawing a circle with sizes (X:{}, Y:{} R:{})".format(x,y,radius))
                pygame.draw.circle(self.surface, color, (x,y), radius, radius)
            else:
                raise Exception("Invalid surface, possible bad initialization")
        except Exception as e:
            print("Caught exception:",e)
        finally:
            print("Drawing step complete")

class Ball:
    def __init__(self, sprite):
        self.sprite = sprite

# Draw game ball and paddles with variables
HalfResolutionWidth = int(ResolutionSettings['Width']) / 2
HalfResolutionHeight = int(ResolutionSettings['Height']) / 2

print(HalfResolutionHeight, int(HalfResolutionHeight))

GameBall = Draw(Surface)
# What is the shape?
if GameSettings['BallShape'].lower() == 'default':
    # Draw the default, which is a square
    GameBall.rect(Colors[GameSettings['BallColor'].lower()], int(HalfResolutionWidth), int(HalfResolutionHeight), int(GameSettings['BallWidth']), int(GameSettings['BallHeight']), 1, True)
else:
    # Draw a circle
    GameBall.circle(Colors[GameSettings['BallColor'].lower()], int(HalfResolutionWidth), int(HalfResolutionHeight), int(GameSettings['BallRadius']), 1)

# Functional loop
Clock = pygame.time.Clock()
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update ball


    # Update
    pygame.display.update()

    # Refresh rate
    Tick = Clock.tick(ApplicationSettings['FPS'])
