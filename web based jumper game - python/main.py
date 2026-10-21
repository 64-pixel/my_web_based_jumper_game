
import asyncio
import pygame, sys
import os
from os import listdir
from os.path import isfile, join
from button import Button




pygame.init()

pygame.display.set_caption("Jumper")

BG_COLOR = (255, 255, 255)
WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 6

BACKGROUND_DIR = join("textures and art", "background")

BACKGROUND_FILES = sorted(
    f for f in listdir(BACKGROUND_DIR)
    if isfile(join(BACKGROUND_DIR, f))
    and f.lower().endswith(".png")
)

selected_background = (
    "background.png"
    if "background.png" in BACKGROUND_FILES
    else BACKGROUND_FILES[0]
)

CONTROLS =  {
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "jump": pygame.K_SPACE
}

window = pygame.display.set_mode((WIDTH, HEIGHT))

def end_screen():
    pygame.display.set_caption("Jumper - END")
    clock = pygame.time.Clock()



    restart_button = Button(
        image=pygame.image.load(
            "textures and art/Options rect.png"
        ),
        pos=(500, 400),
        text_input="RESTART",
        font=get_font(90),
        base_color="#d7fcd4",
        hovering_color="Red"
    )

    quit_button = Button(
        image=pygame.image.load(
            "textures and art/Quit Rect.png"
        ),
        pos=(500, 600),
        text_input="QUIT",
        font=get_font(75),
        base_color="#d7fcd4",
        hovering_color="Purple"
    )

    while True:
        mouse_pos = pygame.mouse.get_pos()
        window.fill("#968c38")

        end_text = get_font(80).render(
                    "You Died", True, "#BA1B1B"
                )
        end_rect = end_text.get_rect(center=(500, 100))
        window.blit(end_text, end_rect)

        for button in (quit_button, restart_button):
            button.changeColor(mouse_pos)
            button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if restart_button.checkForInput(event.pos):
                        pygame.display.set_caption("Jumper")
                        return "restart"

                    if quit_button.checkForInput(event.pos):
                        pygame.quit()
                        sys.exit()

        pygame.display.update()
        clock.tick(FPS)


def get_font(size):
    return pygame.font.Font("textures and art/font.ttf",size)

def levels():
    clock = pygame.time.Clock()
    waiting_for = None

    while True:

        level1_button = Button(
                    None, (500,400), "1",
                    get_font(45), "Black", "Green"
                )
        level2_button = Button(
                            None, (600,400), "2",
                            get_font(45), "Black", "Green"
                        )

        back_button = Button(
            None, (150, 200), "BACK",
            get_font(45), "Black", "Green"
        )

        while True:
            mouse_pos = pygame.mouse.get_pos()
            window.fill("#968c38")

            title = get_font(65).render(
                        "SELECT LEVEL", True, "Black"
                    )
            window.blit(title, title.get_rect(center=(500,100)))

            for button in (level1_button, level2_button, back_button):
                button.changeColor(mouse_pos)
                button.update(window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key ==pygame.K_ESCAPE:
                        return None

                if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1:
                    if level1_button.checkForInput(event.pos):
                        return 1

                    if level2_button.checkForInput(event.pos):
                        return 2

                    if back_button.checkForInput(event.pos):
                        return None

            pygame.display.update()
            clock.tick(FPS)




def options():
    global selected_background

    waiting_for = None
    clock = pygame.time.Clock()

    while True:
        mouse_pos = pygame.mouse.get_pos()
        window.fill("#968c38")

        title = get_font(65).render(
            "Options", True, "Black"
        )
        window.blit(title, title.get_rect(center=(500, 70)))

        background_name = get_font(35).render(
            "Background", True, "Green"
        )
        window.blit(
            background_name,
            background_name.get_rect(center=(500,205))
        )

        preview_image = pygame.image.load(
            join(BACKGROUND_DIR, selected_background)
        ).convert()

        preview_image = pygame.transform.scale(
            preview_image, (240,120)
        )

        preview_rect = preview_image.get_rect(
            center=(130, 200)
        )

        window.blit(preview_image, preview_rect)

        pygame.draw.rect(
            window, "Black", preview_rect, 2
        )

        previous_bg = Button(
            None, (300,205), "<",
            get_font(45), "Black", "Green"
        )

        next_bg = Button(
            None, (700,205), ">",
            get_font(45), "Black", "Green"
        )

        controls_title = get_font(35). render(
            "Controls", True, "Black"
        )
        window.blit(
            controls_title,
            controls_title.get_rect(center=(500,285))
        )

        control_buttons = {}

        labels = [
            ("left", "MOVE LEFT"),
            ("right", "MOVE RIGHT"),
            ("jump", "JUMP")
        ]

        for i, (control, label) in enumerate(labels):
            y = 350 + i * 75

            text = get_font(30).render(
                label, True, "Black"
            )
            window.blit(
                text,
                text.get_rect(midright=(440,y))
            )

            if waiting_for ==control:
                key_text = "PRESS A KEY ..."
            else:
                key_text = pygame.key.name(CONTROLS[control]).upper()

            control_buttons[control] = Button(
                None, (610,y), key_text,
                get_font(30), "Blue", "Green"
            )

        back_button = Button(
            None, (500,610), "BACK",
            get_font(50), "Black", "Green"
        )

        all_buttons = [
            previous_bg, next_bg, back_button,
            *control_buttons.values()
        ]

        for button in all_buttons:
            button.changeColor(mouse_pos)
            button.update(window)

        if waiting_for:
            hint = get_font(22).render(
                "Press a key to assign the control",
                True, "Red"
            )
            window.blit(
                hint, hint.get_rect(center=(500,690))
            )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and waiting_for:
                already_used = any(
                    key == event.key
                    for name, key in CONTROLS.items()
                    if name != waiting_for
                )

                if not already_used and event.key != pygame.K_ESCAPE:
                    CONTROLS[waiting_for] = event.key

                waiting_for = None
                continue

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button.checkForInput(event.pos):
                    return

                if previous_bg.checkForInput(event.pos):
                    index = BACKGROUND_FILES.index(selected_background)
                    selected_background = BACKGROUND_FILES[
                        (index - 1) % len(BACKGROUND_FILES)
                    ]  

                elif next_bg.checkForInput(event.pos):
                    index = BACKGROUND_FILES.index(selected_background)
                    selected_background = BACKGROUND_FILES[
                        (index + 1 ) % len(BACKGROUND_FILES)
                    ] 

                for control, button in control_buttons.items():
                    if button.checkForInput(event.pos):
                        waiting_for = control
                        break

        pygame.display.update()
        clock.tick(FPS)


def main_menu():
    pygame.display.set_caption("Jumper - Main Menu")

    play_button = Button(
        image=pygame.image.load(
            "textures and art/Play Rect.png"
        ),
        pos=(500, 300),
        text_input="PLAY",
        font=get_font(75),
        base_color="#d7fcd4",
        hovering_color="Purple"
    )

    levels_button = Button(
        image= pygame.image.load(
            "textures and art/Play Rect.png"
        ),
        pos = (500, 570),
        text_input="LEVELS",
        font=get_font(50),
        base_color="#d7fcd4",
        hovering_color="Purple"
    )

    options_button = Button(
        image=pygame.image.load(
            "textures and art/Options Rect.png"
        ),
        pos=(500, 450),
        text_input="OPTIONS",
        font=get_font(75),
        base_color="#d7fcd4",
        hovering_color="Purple"
    )

    quit_button = Button(
        image=pygame.image.load(
            "textures and art/Quit Rect.png"
        ),
        pos=(500, 700),
        text_input="QUIT",
        font=get_font(75),
        base_color="#d7fcd4",
        hovering_color="Purple"
    )

    while True:
        mouse_pos = pygame.mouse.get_pos()
        window.fill("#968c38")

        menu_text = get_font(75).render(
            "MAIN MENU", True, "#8e3797"
        )
        menu_rect = menu_text.get_rect(center=(500, 100))
        window.blit(menu_text, menu_rect)

        for button in (play_button, options_button, levels_button, quit_button):
            button.changeColor(mouse_pos)
            button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if play_button.checkForInput(event.pos):
                        return "play"

                    if options_button.checkForInput(event.pos):
                        return "options"

                    if levels_button.checkForInput(event.pos):
                        return "levels"

                    if quit_button.checkForInput(event.pos):
                        pygame.quit()
                        sys.exit()

        pygame.display.update()


def flip(sprites):
    return [
        pygame.transform.flip(sprite, True, False)
        for sprite in sprites
    ]


def load_sprite_sheets(
    dir1, dir2, width, height, direction=False
):
    path = join("textures and art", dir1, dir2)

    images = [
        f for f in listdir(path)
        if isfile(join(path, f)) and f.lower().endswith(".png")
    ]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(
            join(path, image)
        ).convert_alpha()

        sprites = []

        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface(
                (width, height), pygame.SRCALPHA, 32
            )

            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)

            sprites.append(pygame.transform.scale2x(surface))

        name = image[:-4]

        if direction:
            all_sprites[name + "_right"] = sprites
            all_sprites[name + "_left"] = flip(sprites)
        else:
            all_sprites[name] = sprites

    return all_sprites


def get_block(size):
    path = join("textures and art", "terrain", "Terrain.png")

    image = pygame.image.load(path).convert_alpha()

    surface = pygame.Surface(
        (size, size), pygame.SRCALPHA, 32
    )

    rect = pygame.Rect(9, 0, size, size)
    surface.blit(image, (0, 0), rect)

    return pygame.transform.scale2x(surface)



class Player(pygame.sprite.Sprite):
    GRAVITY = 1

    SPRITES = load_sprite_sheets(
        "characters", "test_char", 32, 32, True
    )

    ANIMATION_DELAY = 5

    def __init__(self, x, y, width, height):
        super().__init__()

        self.rect = pygame.Rect(x, y, width, height)

        self.health = 3
        self.pickedup = 0

        self.x_vel = 0
        self.y_vel = 0

        self.mask = None
        self.sprite = None

        self.direction = "left"
        self.animation_count = 0

        self.fallcount = 0
        self.jump_count = 0

        self.hit = False
        self.hit_count = 0

        self.update_sprite()


    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1

        if self.jump_count == 1:
            self.fallcount = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy


    def make_hit(self):
        if not self.hit:
            self.hit = True
            self.hit_count = 0
            self.health -=1

    def move_left(self, vel):
        self.x_vel = -vel

        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel

        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):

        self.move(self.x_vel, self.y_vel)

        self.y_vel += min(
            1, (self.fallcount / fps) * self.GRAVITY
        )

        if self.hit:
            self.hit_count += 1
            

        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        self.fallcount += 1
        self.update_sprite()

    def landed(self):
        self.fallcount = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.fallcount = 0
        self.y_vel *= -1

    


    def update_sprite(self):
        sprite_sheet = "robber_idle"

        if self.hit:
            sprite_sheet = "robber_hit"

        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "robber_jump"
            elif self.jump_count == 2:
                sprite_sheet = "robber_double_jump"

        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "robber_fall"

        elif self.x_vel != 0:
            sprite_sheet = "robber_run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]

        sprite_index = (
            self.animation_count // self.ANIMATION_DELAY
        ) % len(sprites)

        self.sprite = sprites[sprite_index]
        self.animation_count += 1

        self.update()

    def update(self):
        if self.sprite is None:
            return

        self.rect = self.sprite.get_rect(
            topleft=(self.rect.x, self.rect.y)
        )

        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        win.blit(
            self.sprite,
            (self.rect.x - offset_x, self.rect.y)
        )




class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()

        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface(
            (width, height), pygame.SRCALPHA
        )

        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(
            self.image,
            (self.rect.x - offset_x, self.rect.y)
        )


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)

        block = get_block(size)
        self.image.blit(block, (0, 0))

        self.mask = pygame.mask.from_surface(self.image)

''' class Saw(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "saw")
        
        self.saw = load_sprite_sheets(
            "traps", "saw", width, height
        )

        self.image = self.saw["off"][0]
        self.mask = pygame.mask.from_surface(self.image)

        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.saw[self.animation_name]

        sprite_index = (
            self.animation_count // self.ANIMATION_DELAY
        ) % len(sprites)

        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(
            topleft=(self.rect.x, self.rect.y)
        )

        self.mask = pygame.mask.from_surface(self.image)

        if (
            self.animation_count // self.ANIMATION_DELAY
            >= len(sprites)
        ):
            self.animation_count = 0
  '''  

class Fire(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")

        self.fire = load_sprite_sheets(
            "traps", "fire", width, height
        )

        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)

        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]

        sprite_index = (
            self.animation_count // self.ANIMATION_DELAY
        ) % len(sprites)

        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(
            topleft=(self.rect.x, self.rect.y)
        )

        self.mask = pygame.mask.from_surface(self.image)

        if (
            self.animation_count // self.ANIMATION_DELAY
            >= len(sprites)
        ):
            self.animation_count = 0

class Spikes(Object):
    def __init__ (self, x,y,width, height):
        super().__init__(x,y,width,height, "spikes")
        self.spikes = load_sprite_sheets(
            "traps", "spikes", width, height
        )
        self.image = self.spikes["Idle"][0]
        self.mask = pygame.mask.from_surface(self.image)

    def loop(self):
        sprites = self.spikes[self.animation_name]

        self.rect = self.image.get_rect(
            topleft = (self.rect.x, self.rect.y)
        )
        self.mask = pygame.mask.from_surface(self.image)

class Apple(Object):
    ANIMATION_DELAY = 5

    def __init__(self, x,y, width, height):
        super().__init__(x,y,width, height, "apple")

        self.fruits = load_sprite_sheets(
            "items", "fruits", width, height
        )

        apple_key = next(
            (
            name for name in self.fruits
            if "apple" in name.lower()
            ),
            None
        )

        if apple_key is None:
            raise ValueError(
                "cant find image Apple.png"
            )

        self.animation_name = apple_key
        self.animation_count = 0

        self.image = self.fruits[self.animation_name][0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def loop(self):
        sprites = self.fruits[self.animation_name]

        sprite_index = (
            self.animation_count // self.ANIMATION_DELAY
        ) % len(sprites)

        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(
            topleft = (self.rect.x, self.rect.y)
        )

        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count >= len(sprites) * self.ANIMATION_DELAY:
            self.animation_count


        



def g_background(name):
    image = pygame.image.load(
        join("textures and art", "background", name)
    ).convert()

    _, _, width, height = image.get_rect()

    tiles = []

    for i in range(WIDTH // width + 1):
        for n in range(HEIGHT // height + 1):
            position = (i * width, n * height)
            tiles.append(position)

    return tiles, image


def draw(window, background, bg_image, player, objects, offset_x):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)

    hud_background = pygame.Surface((420,90), pygame.SRCALPHA)
    hud_background.fill((0,0,0,170))
    window.blit(hud_background, (15,15))

    health_text = get_font(30).render(
        f"Health: {player.health}/3",
        True,
        "Red"
    )

    points_text = get_font(20).render(
        f"Apples: {player.pickedup}/ Points: {player.pickedup}",
        True,
        "Yellow"
    )

    window.blit(health_text, (25,20))
    window.blit(points_text, (25,55))

    pygame.display.flip()



def handle_vertical_collision(player, objects, dy):
    collided_objects = []

    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):

            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()

            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()

    collided_object = None

    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()

    return collided_object


def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0

    collide_left = collide(
        player, objects, -PLAYER_VEL * 2
    )

    collide_right = collide(
        player, objects, PLAYER_VEL * 2
    )

    if keys[CONTROLS["left"]] and not collide_left:
        player.move_left(PLAYER_VEL)

    if keys[CONTROLS["right"]] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(
        player, objects, player.y_vel
    )

    to_check = [
        collide_left,
        collide_right,
        *vertical_collide
    ]

    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()

    for obj in to_check:
        if obj and obj.name =="spikes":
            player.make_hit()

    for obj in to_check:
        if obj and obj.name == "saw":
            player.make_hit()

def collect_apples(player,apples,objects):
    for apple in apples[:]:
        if pygame.sprite.collide_mask(player, apple):
            player.pickedup +=1

            apples.remove(apple)
            objects.remove(apple)




async def main(window, level=1):
    clock = pygame.time.Clock()

    level_background = selected_background

    if level == 2 and len(BACKGROUND_FILES) >1:
        other_backgrounds = [
            name for name in BACKGROUND_FILES
            if name != selected_background
        ]
        level_background = other_backgrounds[0]

    background, bg_image = g_background(level_background)
    print(f"Loading level{level}, background: {level_background}")

    player = Player(100, 600, 50, 50)

    block_size = 96

    # Společná podlaha pro oba levely
    floor = [
        Block(i * block_size, HEIGHT - block_size, block_size)
        for i in range(
            -WIDTH // block_size,
            (WIDTH * 2) // block_size
        )
    ]

    if level == 1:
        # MAPA LEVELU 1
        fire1 = Fire(
            450,
            HEIGHT - block_size * 2 - 64,
            16, 32
        )
        fire2 = Fire(
            600,
            HEIGHT - block_size * 2 - 64,
            16, 32
        )

        spikes = [
            Spikes(x, HEIGHT - block_size - 32, 16, 16)
            for x in (300, 500, 800)
        ]

        platforms = [
            Block(0, HEIGHT - block_size * 2, block_size),
            Block(block_size * 3, HEIGHT - block_size * 4, block_size)
        ]

        apples = [
            Apple(100, 200, 32,32),
            Apple(400, 450, 32,32),
            Apple(700, 300, 32,32)
        ]

    else:
        # MAPA LEVELU 2 - jiné plošiny a překážky
        fire1 = Fire(
            350,
            HEIGHT - block_size * 2 - 64,
            16, 32
        )
        fire2 = Fire(
            700,
            HEIGHT - block_size * 3 - 64,
            16, 32
        )

        spikes = [
            Spikes(x, HEIGHT - block_size - 32, 16, 16)
            for x in (220, 420, 620, 820)
        ]

        platforms = [
            Block(200, HEIGHT - block_size * 2, block_size),
            Block(400, HEIGHT - block_size * 3, block_size),
            Block(1100, HEIGHT - block_size * 2, block_size),
            Block(1300, HEIGHT - block_size * 4, block_size)
        ]

        apples = [
            Apple(250, 400, 16, 32),
            Apple(550, 250, 16, 32),
            Apple(850, 150, 16, 32)
        ]

    fire1.on()
    fire2.on()

    objects = [
        *floor,
        *platforms,
        fire1,
        fire2,
        *spikes,
        *apples
    ]

    offset_x = 0
    scroll_area_width = 200

    running = True

    while running:
        clock.tick(FPS)

        
        await asyncio.sleep(0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if (event.key == CONTROLS["jump"] and player.jump_count < 2):
                    player.jump()

        if not running:
            break

        player.loop(FPS)
        fire1.loop()
        fire2.loop()
        for apple in apples:
            apple.loop()
        #saw1.loop()

        collect_apples(player, apples, objects)
        handle_move(player, objects)

        if player.health <=0:
            result = end_screen()
            return result

        draw(
            window,
            background,
            bg_image,
            player,
            objects,
            offset_x
        )

        if (
            (player.rect.right - offset_x >= WIDTH - scroll_area_width)
            and player.x_vel > 0) or ((player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

    pygame.quit()


if __name__ == "__main__":
    while True:
        choice = main_menu()

        if choice == "options":
            options()

        elif choice == "levels":
            chosen_level = levels()

            # Pokud hráč klikne na BACK, vrátí se do menu
            if chosen_level is None:
                continue

            while True:
                result = asyncio.run(main(window, chosen_level))

                if result != "restart":
                    break

        elif choice == "play":
            while True:
                result = asyncio.run(main(window, 1))

                if result != "restart":
                    break

    pygame.quit()
