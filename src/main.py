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
    Surface.fill(Colors[SurfaceSettings['BackgroundColor']])
except Exception as e:
    print("Caught exception:",e)

# Functional loop
Clock = pygame.time.Clock()
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update
    pygame.display.update()

    # Refresh rate
    Tick = Clock.tick(ApplicationSettings['FPS'])
