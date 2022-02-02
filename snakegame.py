import pygame
import sys
import random
from pygame.math import Vector2


class Button:
    def __init__(self, text, width, height, pos, elevation):
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]

        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#475F77'

        self.bottom_rect = pygame.Rect(pos, (width, elevation))
        self.bottom_color = '#354B5E'

        self.text_surf = game_font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = (self.top_rect.center))

    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=10)
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=10)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed == True:
                    return True
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = '#475F77'
        return False

class Fruit:
    def __init__(self) -> None:
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)
        self.apple = pygame.image.load('graphics/apple.png').convert_alpha()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(
            int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(self.apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class Snake:
    def __init__(self) -> None:
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

        self.head_up = pygame.image.load(
            'Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load(
            'Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load(
            'Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load(
            'Graphics/head_left.png').convert_alpha()
        self.head = self.head_right

        self.tail_up = pygame.image.load(
            'Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load(
            'Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load(
            'Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load(
            'Graphics/tail_left.png').convert_alpha()
        self.tail = self.tail_left

        self.body_vertical = pygame.image.load(
            'Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load(
            'Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load(
            'Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load(
            'Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load(
            'Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load(
            'Graphics/body_bl.png').convert_alpha()

    def draw_snake(self):
        self.update_head_grapchis()
        self.update_tail_graphics()
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            snake_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, snake_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, snake_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block

                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, snake_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, snake_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, snake_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, snake_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, snake_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, snake_rect)

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def update_head_grapchis(self):
        head_relation = self.body[0] - self.body[1]
        if head_relation == Vector2(1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(0, 1):
            self.head = self.head_down
        elif head_relation == Vector2(0, -1):
            self.head = self.head_up

    def update_tail_graphics(self):
        tail_relation = self.body[-1] - self.body[-2]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_down
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_up

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]

class Main:
    def __init__(self) -> None:
        self.snake = Snake()
        self.fruit = Fruit()
        

        pygame.display.set_caption('Aku sebenernya sayang sama kamu')
        icon = pygame.image.load('graphics/icon.png').convert()
        pygame.display.set_icon(icon)
        self.cruch_sound = pygame.mixer.Sound('Sound/crunch.wav')

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.eat_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if self.snake.body[0].x < 0 or self.snake.body[0].x > cell_number-1 or self.snake.body[0].y < 0 or self.snake.body[0].y > cell_number-1:
            self.game_over()
            return True
        for block in self.snake.body[2:]:
            if block == self.snake.body[0]:
                self.game_over()
                return True
        return False

    def game_over(self):
        self.snake.reset()
        
    def draw_grass(self):
        grass_color = (167, 209, 61)

        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(
                            col*cell_size, row*cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(
                            col*cell_size, row*cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        self.score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(self.score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        self.score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = self.fruit.apple.get_rect(
            midright=(self.score_rect.left, self.score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top,
                              apple_rect.width+self.score_rect.width + 10, apple_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, self.score_rect)
        screen.blit(self.fruit.apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)
        

    def eat_sound(self):
        self.cruch_sound.play()



pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
game_font = pygame.font.Font('font/PoetsenOne-Regular.ttf', 25)
clock = pygame.time.Clock()
game_active = True
pause_state = False

SCREEN_UPDATE = pygame.USEREVENT + 1
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = Main()

play_button = Button('Play', 200, 40, (cell_number * cell_size / 2  - 250, cell_number * cell_size / 2), 6)
exit_button = Button('Exit', 200, 40, (cell_number * cell_size / 2 + 50, cell_number * cell_size / 2), 6)
resume_button = Button('Resume', 200, 40, (cell_number * cell_size / 2  - 250, cell_number * cell_size / 2), 6)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE and game_active == True:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_ESCAPE:
                game_active = not(game_active)
                pause_state = not(pause_state)

    if game_active:
        screen.fill((175, 215, 70))
        main_game.draw_elements()
        if main_game.check_fail():
            main_game.snake.direction = Vector2(1,0)
            game_active = False
            pause_state = False
    else:
        # screen.fill((94,129,162))
        paused_text = game_font.render('Paused', True, '#475F77')
        game_over_text = game_font.render('Game Over', True, '#475F77')
        score_text =  game_font.render('Your Score: ' + main_game.score_text, True, '#475F77')
        # play_text =  game_font.render('Press ESC to Continue', True, (56, 74, 12))
        menu_score = score_text.get_rect(center = (cell_number * cell_size / 2, cell_number * cell_size / 2 - 100))
        game_over_rect = game_over_text.get_rect(center = (cell_number * cell_size / 2, cell_number * cell_size / 2 - 50))
        paused_text_rect = game_over_text.get_rect(center = (cell_number * cell_size / 2 + 20, cell_number * cell_size / 2 - 50))
        # play_text_rect = play_text.get_rect(center = (cell_number * cell_size / 2, cell_number * cell_size / 2 - 100 + int(score.get_height())))
        if pause_state == True:
            screen.blit(paused_text, paused_text_rect)
            resume_button.draw()
        else:
            screen.blit(game_over_text, game_over_rect)
            screen.blit(score_text, menu_score)
            play_button.draw()
        
        
        # screen.blit(play_text, play_text_rect)
        exit_button.draw()

        if play_button.check_click() or resume_button.check_click():
            pause_state = False
            game_active = True
            play_button.pressed = False
            resume_button.pressed = False
            
        elif exit_button.check_click():
            pygame.quit()
            sys.exit()
        
    pygame.display.update()
    clock.tick(60)
