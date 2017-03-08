import sys
import sdl2.ext
import random
import time
# Custom Modules:
import game
import globals
import sprite_classes
import music

# Create a resource container:
RESOURCES = sdl2.ext.Resources(__file__, "resources")

# Z-LAYERING DEPTHS:
#    0 - HIDE (HOME/GAMEOVER OFF)
#    1 - BACKGROUND
#    2 - SALMON
#    3 - ENEMIES
#    4 - HUD
#    5 - SHOW (HOME/GAMEOVER ON)

class SalmonRun(game.Game):
    def __init__(self, name, winx, winy):
        super(SalmonRun, self).__init__(name, winx, winy)
        # Init sprites:
        self.sp_homescreen = self.factory.from_image(RESOURCES.get_path('homescreen.bmp'))
        self.sp_gameover = self.factory.from_image(RESOURCES.get_path('gameover.bmp'))
        self.sp_background = self.factory.from_image(RESOURCES.get_path('background.bmp'))
        self.sp_dashboard = self.factory.from_image(RESOURCES.get_path('dashboard.bmp'))
        self.sp_salmon = self.factory.from_image(RESOURCES.get_path('salmon.bmp'))
        self.sp_energy = self.factory.from_color((0,255,0,0),(615,15,10,30))

        # Init sprite class instances: (except for the special salmon...)
        self.homescreen = sprite_classes.Inert(self.world, self.sp_homescreen, 0, 0)
        self.gameover = sprite_classes.Inert(self.world, self.sp_gameover, 0, 0)
        self.background = sprite_classes.Inert(self.world, self.sp_background, 0, 50)
        self.dashboard = sprite_classes.Inert(self.world, self.sp_dashboard,0, 0)

        self.energy = sprite_classes.Inert(self.world, self.sp_energy,615,15)
        self.energy.setDepth(6)

    def init_numbers(self):
        self.zero = game.factory.from_image(RESOURCES.get_path('s_numbers.bmp'))

    def init_salmon(self):
        self.salmon = sprite_classes.Player(self.world, self.sp_salmon, 400, 550)
        self.salmon.setDepth(2)
        self.collision.salmon = self.salmon
        self.aicontroller.target = self.salmon

    def render_home(self):
        self.homescreen.setDepth(5)
        self.world.process()
        while globals.home_lock == True:                # Wait for user-input
            events = sdl2.ext.get_events()
            for event in events:
                self.handleEvent(event)
            self.world.process()
        self.homescreen.setDepth(0)

    def render_game_over(self):
        self.gameover.setDepth(5)
        self.world.process()
        sdl2.SDL_Delay(2000)
        self.gameover.setDepth(0)

    def render_play(self):
        self.init_salmon()
        self.background.setDepth(1)
        self.dashboard.setDepth(4)

    def spawn(self, path, size, depth, tracking):
        v = random.randint(1,10)
        x = random.randint(90,610)
        sp_enemy = self.factory.from_image(RESOURCES.get_path(path))
        if tracking:
            self.enemy = sprite_classes.Enemy(self.world, sp_enemy, x, 0, True)
        else:
            self.enemy = sprite_classes.Enemy(self.world, sp_enemy, x, 0, False)
        self.enemy.velocity.vy = v
        self.enemy.size.size = size
        self.enemy.setDepth(depth)

    def manage_spawn(self, delta_t, ai_flag):
        if delta_t % 1 == 0:
            self.spawn('enemy0.bmp', 0, 3, ai_flag)
        if delta_t % 2 == 0:
            self.spawn('enemy1.bmp', 1, 3, ai_flag)
        if delta_t % 3 == 0:
            self.spawn('enemy2.bmp', 2, 3, ai_flag)
        if delta_t % 4 == 0:
            self.spawn('enemy3.bmp', 3, 3, ai_flag)
        if delta_t % 5 == 0:
            self.spawn('enemy4.bmp', 4, 3, ai_flag)
        if delta_t % 8 == 0:
            self.spawn('enemy5.bmp', 5, 3, ai_flag)
        if delta_t % 10 == 0:
            self.spawn('enemy6.bmp', 6, 3, ai_flag)
        if delta_t % 12 == 0:
            self.spawn('enemy7.bmp', 7, 3, ai_flag)
        if delta_t % 14 == 0:
            self.spawn('enemy8.bmp', 8, 3, ai_flag)
        if delta_t % 16 == 0:
            self.spawn('enemy9.bmp', 9, 3, ai_flag)
        if delta_t % 18 == 0:
            self.spawn('enemy10.bmp', 10, 3, ai_flag)
        if delta_t % 20 == 0:
            self.spawn('enemy11.bmp', 11, 3, ai_flag)
        if delta_t % 22 == 0:
            self.spawn('enemy12.bmp', 12, 3, ai_flag)
        if delta_t % 24 == 0:
            self.spawn('enemy13.bmp', 13, 3, ai_flag)
        if delta_t % 26 == 0:
            self.spawn('enemy14.bmp', 14, 3, ai_flag)

    def handleEvent(self, event):
        # Handle home screen events:
        if globals.home_lock == True:
            if event.type == sdl2.SDL_QUIT:
                globals.home_lock = False
                globals.running = False
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_p:
                    globals.home_lock = False
                    self.render_play()          # Render game play screen
        # Handle game play events:
        else:
            if event.type == sdl2.SDL_QUIT:
                globals.running = False
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_LEFT:
                    self.salmon.velocity.vx = -6
                elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
                    self.salmon.velocity.vx = 6
                elif event.key.keysym.sym == sdl2.SDLK_UP:
                    self.salmon.velocity.vy = -3
                elif event.key.keysym.sym == sdl2.SDLK_DOWN:
                    self.salmon.velocity.vy = 3
                elif event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    globals.running = False
            elif event.type == sdl2.SDL_KEYUP:
                if event.key.keysym.sym in (sdl2.SDLK_LEFT, sdl2.SDLK_RIGHT, sdl2.SDLK_UP, sdl2.SDLK_DOWN):
                    self.salmon.velocity.vx -= 1
                    self.salmon.velocity.vy -= 1

    def run(self):
        music.play_music()                      # Play background music
        self.render_home()                      # Render home screen
        globals.running = True
        while globals.running:                  # Begin event loop
            delta_t = int(time.time()-self.start_t)
            # Spawn Enemies:
            if delta_t != self.old_t:
                num = random.randint(1,6)       # Give 1/6 of enemies ai
                ai_flag = True if num == 1 else False
                self.manage_spawn(delta_t, ai_flag)  # Spawn enemies
            # Process SDL events:
            events = sdl2.ext.get_events()
            for event in events:
                self.handleEvent(event)
            # Death process:
            if globals.death == True:
                self.render_game_over()         # Render Game Over screen & delete sprites
                globals.death = False
                globals.home_lock = True
                self.render_home()              # Render home screen
            sdl2.SDL_Delay(10)
            self.old_t = delta_t
            self.world.process()
        sdl2.ext.quit()
        return 0

def main():
    sr = SalmonRun("Salmon Run",800,650)
    sr.run()

if __name__ == "__main__":
    main()
