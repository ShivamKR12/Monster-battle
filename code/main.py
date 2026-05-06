from settings import *
from support import *
from timer import Timer # type: ignore
from monster import *
from random import choice
from ui import *
from attack import AttackAnimationSprite
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption('Monster Battle')
        self.clock = pygame.time.Clock()
        self.running = True
        self.import_assets()
        self.bg_surfs['bg'] = pygame.transform.scale(self.bg_surfs['bg'], (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.audio['music'].play(-1)
        self.player_active = True
        self.state = 'battle'
        self.opponent_kills = 0
        self.win_condition = 3

        # groups 
        self.all_sprites = pygame.sprite.Group()

        # data 
        player_monster_list = ['Sparchu', 'Jacana', 'Plumette', 'Atrox']
        self.player_monsters = [Monster(name, self.back_surfs[name]) for name in player_monster_list]
        self.monster = self.player_monsters[0]
        self.all_sprites.add(self.monster)
        opponent_name = choice(list(MONSTER_DATA.keys()))
        self.opponent = Opponent(opponent_name, self.front_surfs[opponent_name], self.all_sprites)

        # ui 
        self.ui = UI(self.monster, self.player_monsters, self.simple_surfs, self.get_input)
        self.opponent_ui = OpponentUI(self.opponent)

        # timers
        self.timers = {'player end': Timer(1000, func = self.opponent_turn), 'opponent end': Timer(1000, func = self.player_turn)}

    def reset_game(self):
        self.player_active = True
        self.state = 'battle'
        self.opponent_kills = 0

        # groups 
        self.all_sprites.empty()

        # data 
        player_monster_list = ['Sparchu', 'Jacana', 'Plumette', 'Atrox']
        self.player_monsters = [Monster(name, self.back_surfs[name]) for name in player_monster_list]
        self.monster = self.player_monsters[0]
        self.all_sprites.add(self.monster)
        opponent_name = choice(list(MONSTER_DATA.keys()))
        self.opponent = Opponent(opponent_name, self.front_surfs[opponent_name], self.all_sprites)

        # ui 
        self.ui = UI(self.monster, self.player_monsters, self.simple_surfs, self.get_input)
        self.opponent_ui = OpponentUI(self.opponent)

        # timers
        self.timers = {'player end': Timer(1000, func = self.opponent_turn), 'opponent end': Timer(1000, func = self.player_turn)}

    def get_input(self, state, data = None):
        if state == 'attack':
            self.apply_attack(self.opponent, data)
        elif state == 'heal':
            self.monster.health += 50
            AttackAnimationSprite(self.monster, self.attack_frames['green'], self.all_sprites)
            self.audio['green'].play()
        elif state == 'switch':
            self.monster.kill()
            self.monster = data
            self.all_sprites.add(self.monster)
            self.ui.monster = self.monster

        elif state == 'escape':
            self.running = False
        self.player_active = False
        self.timers['player end'].activate()

    def apply_attack(self, target, attack):
        attack_data = ABILITIES_DATA[attack]
        attack_multiplier = ELEMENT_DATA[attack_data['element']][target.element]
        target.health -= attack_data['damage'] * attack_multiplier
        AttackAnimationSprite(target, self.attack_frames[attack_data['animation']], self.all_sprites)
        self.audio[attack_data['animation']].play()

    def opponent_turn(self):
        if self.opponent.health <= 0:
            self.opponent_kills += 1
            if self.opponent_kills >= self.win_condition:
                self.state = 'victory'
            else:
                self.player_active = True
                self.opponent.kill()
                monster_name = choice(list(MONSTER_DATA.keys()))
                self.opponent = Opponent(monster_name, self.front_surfs[monster_name], self.all_sprites)
                self.opponent_ui.monster = self.opponent
        else:
            attack = choice(self.opponent.abilities)
            self.apply_attack(self.monster, attack)
            self.timers['opponent end'].activate()

    def player_turn(self):
        self.player_active = True
        if self.monster.health <= 0:
            available_monsters = [monster for monster in self.player_monsters if monster.health > 0]
            if available_monsters:
                self.monster.kill()
                self.monster = available_monsters[0]
                self.all_sprites.add(self.monster)
                self.ui.monster = self.monster
            else:
                self.state = 'game_over'

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def import_assets(self):
        self.back_surfs = folder_importer('images', 'back')
        self.front_surfs = folder_importer('images', 'front')
        self.bg_surfs = folder_importer('images', 'other')
        self.simple_surfs = folder_importer('images', 'simple')
        self.attack_frames = tile_importer(4,'images', 'attacks')
        self.audio = audio_importer('audio')

    def draw_monster_floor(self):
        for sprite in self.all_sprites:
            if isinstance(sprite, Creature):
                floor_rect = self.bg_surfs['floor'].get_frect(center = sprite.rect.midbottom + pygame.Vector2(0, -10))
                self.display_surface.blit(self.bg_surfs['floor'], floor_rect)

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
           
            if self.state == 'battle':
                # update
                self.update_timers()
                self.all_sprites.update(dt)
                if self.player_active:
                    self.ui.update()

            self.display_surface.blit(self.bg_surfs['bg'], (0,0))
            self.draw_monster_floor()
            self.all_sprites.draw(self.display_surface)
            self.ui.draw()
            self.opponent_ui.draw()

            if self.state != 'battle':
                screen_copy = self.display_surface.copy()
                tiny_surf = pygame.transform.smoothscale(screen_copy, (WINDOW_WIDTH // 4, WINDOW_HEIGHT // 4))
                blur_surf = pygame.transform.smoothscale(tiny_surf, (WINDOW_WIDTH, WINDOW_HEIGHT))
                
                tint_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                tint_surf.fill(COLORS['black'])
                tint_surf.set_alpha(150)
                blur_surf.blit(tint_surf, (0, 0))
                self.display_surface.blit(blur_surf, (0, 0))

                font = pygame.font.Font(None, 100)
                text = 'VICTORY' if self.state == 'victory' else 'GAME OVER'
                color = COLORS['green'] if self.state == 'victory' else COLORS['red']
                text_surf = font.render(text, True, color)
                text_rect = text_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50))
                self.display_surface.blit(text_surf, text_rect)

                sub_font = pygame.font.Font(None, 40)
                sub_surf = sub_font.render("Press SPACE to Restart or ESC to Quit", True, COLORS['gray'])
                sub_rect = sub_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50))
                self.display_surface.blit(sub_surf, sub_rect)

                keys = pygame.key.get_just_pressed()
                if keys[pygame.K_ESCAPE]:
                    self.running = False
                if keys[pygame.K_SPACE]:
                    self.reset_game()

            pygame.display.update()
        
        pygame.quit()
        sys.exit()
    
if __name__ == '__main__':
    game = Game()
    game.run()
