import pygame

scenes = {}
active_scene = None

class SceneBase:
    def __init__(self, screen, inputpi, settings, width, height, sfx):
        self.next = self
        self.settings = settings
        self.inputpi = inputpi
        self.screen = screen
        self.width = width
        self.height = height
        self.sfx = sfx
    
    def Start(self):
        print("uh-oh, you didn't override this in the child class")    
    def Stop(self):
        print("uh-oh, you didn't override this in the child class")    
    def ProcessInput(self, events, pressed_keys):
        print("uh-oh, you didn't override this in the child class")

    def Update(self):
        print("uh-oh, you didn't override this in the child class")

    def Render(self, screen):
        print("uh-oh, you didn't override this in the child class")

    def SwitchToScene(self, next_scene):
        global active_scene
        print "switchtoscene"
        self.Stop()
        active_scene = scenes[next_scene]
        self.next.Start()

    
    def Terminate(self):
        self.SwitchToScene(None)

def run_game(pygame, screen, inputpi, settings, width, height, sfx, fps, starting_scene):
    global active_scene
    
    clock = pygame.time.Clock()

    active_scene = scenes[starting_scene]
    active_scene.Start()

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
        
        #active_scene = active_scene.next
        pygame.display.flip()
