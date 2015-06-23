import pygame

class SceneBase:
    def __init__(self, screen, inputpi, settings, width, height, sfx):
        self.next = self
        self.settings = settings
        self.inputpi = inputpi
        self.screen = screen
        self.width = width
        self.height = height
        self.sfx = sfx
    
    def ProcessInput(self, events, pressed_keys):
        print("uh-oh, you didn't override this in the child class")

    def Update(self):
        print("uh-oh, you didn't override this in the child class")

    def Render(self, screen):
        print("uh-oh, you didn't override this in the child class")

    def SwitchToScene(self, next_scene):
        print "switchtoscene"
        self.next = next_scene


    
    def Terminate(self):
        self.SwitchToScene(None)

def run_game(pygame, screen, inputpi, settings, width, height, sfx, fps, starting_scene):
    clock = pygame.time.Clock()

    active_scene = starting_scene

    while active_scene != None:
        deltat = clock.tick(fps)
        if not inputpi is False:
            inputpi.sendEvents()
        pressed_keys = pygame.key.get_pressed()
        
        # Event filtering
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
            
            if quit_attempt:
                active_scene.Terminate()
            else:
                filtered_events.append(event)
        
        active_scene.ProcessInput(filtered_events, pressed_keys)
        active_scene.Update()
        active_scene.Render(screen, clock, deltat)
        
        active_scene = active_scene.next
        pygame.display.flip()
