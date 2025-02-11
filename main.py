import random
import pygame
from pygame.locals import *


def generate_order(n_scoops):
    order = []
    sprinkles = False
    fudge = False

    for _ in range(n_scoops):
        num = random.randint(0, len(flavors) - 1)
        order.append(num)

    side_num = random.randint(1, 4)
    sprinkles = side_num == 1
    fudge = side_num == 2

    return order, sprinkles, fudge


def is_correct_order(order_components, correct_order_components):
    order, sprinkles, fudge = order_components
    correct_order, correct_sprinkles, correct_fudge = correct_order_components

    if len(order) != len(correct_order):
        return False

    if fudge != correct_fudge or sprinkles != correct_sprinkles:
        return False

    for idx, scoop in enumerate(order):
        if scoop != correct_order[idx]:
            return False

    return True


flavors = ["Chocolate", "Mint", "Strawberry", "Butter Pecan", "Birthday Cake", "Vanilla", "Oreo", "Neopolitan",
           "Superman", "Cookie Dough"]

created_order = []
previous_size = 0

correct_order, sprinkles, fudge = generate_order(2)

pygame.init()
screen = pygame.display.set_mode([1024, 800])

background = pygame.image.load('background.png')

font = pygame.font.Font('stardew-valley-stonks.ttf', 32)
order_texts = []

def update_text():
    order_texts.clear()
    for item in correct_order:
        text = font.render(flavors[item], True, (119, 113, 120))
        order_texts.append(text)

    if fudge or sprinkles:
        text = font.render("Fudge" if fudge else "Sprinkles", True, (119, 113, 120))
        order_texts.append(text)

update_text()

cancel_image = pygame.image.load('cancel.png')

flavor_rectangles = [
    Rect(37, 527, 119, 116),   # CHOCOLATE,
    Rect(163, 527, 116, 116),  # MINT
    Rect(421, 528, 115, 114),  # STRAWBERRY
    Rect(544, 528, 121, 114),  # BUTTER PECAN
    Rect(673, 528, 121, 114),  # BIRTHDAY CAKE
    Rect(37, 648, 120, 116),   # VANILLA
    Rect(163, 648, 116, 116),  # OREO
    Rect(421, 649, 115, 114),  # NEOPOLITAN
    Rect(544, 649, 121, 114),  # SUPERMAN
    Rect(673, 649, 121, 113)   # COOKIE DOUGH
]

level_one = []
level_two = []
for i in range(9):
    level_one.append(pygame.image.load(f'0layer/{i}.png'))
    level_two.append(pygame.image.load(f'1layer/{i}.png'))

finish_rectangle = Rect(33, 379, 189, 86)
finish_sound = pygame.mixer.Sound('finish.mp3') # From https://www.youtube.com/watch?v=uiBkqnBh-B0
click_sound = pygame.mixer.Sound('click.mp3') # https://www.youtube.com/watch?v=h8y0JMVwdmM

fudge_rect = Rect(809, 430, 120, 128)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.MOUSEBUTTONDOWN:
            for idx, flavor_rect in enumerate(flavor_rectangles):
                if flavor_rect.collidepoint(event.pos):
                    created_order.append(idx)

                    pygame.mixer.Sound.play(click_sound)
                    pygame.mixer.music.stop()

            if finish_rectangle.collidepoint(event.pos):
                created_components = (created_order, True, True)
                correct_components = (correct_order, True, True)

                if is_correct_order(created_components, correct_components):
                    pygame.mixer.Sound.play(finish_sound)
                    pygame.mixer.music.stop()

                    n_scoops = random.randint(1, 2)
                    correct_order, sprinkles, fudge = generate_order(n_scoops)
                    created_order.clear()
                    previous_size = 0
                    update_text()


    for flavor in flavor_rectangles:
        pygame.draw.rect(screen, (0, 0, 0), flavor)

    pygame.draw.rect(screen, (0, 0, 0), finish_rectangle)
    screen.blit(background, (0, 0))

    pygame.draw.rect(screen, (0, 0, 0), fudge_rect)

    # screen.blit(cancel_image, (0, 0))
    # pygame.draw.circle(screen, (0,0, 0), (521, 445), 48)

    if len(created_order) >= 1:
        screen.blit(pygame.image.load(f'0layer/{created_order[0]}.png'), (0, 0))
    if len(created_order) >= 2:
        screen.blit(pygame.image.load(f'1layer/{created_order[1]}.png'), (0, 0))

    if len(created_order) != 0:
        if fudge:
            screen.blit(pygame.image.load(f'{len(created_order) - 1}layer/fudge.png'), (0, 0))
        if sprinkles:
            screen.blit(pygame.image.load(f'{len(created_order) - 1}layer/sprinkles.png'), (0, 0))

    for idx, flavor_rect in enumerate(flavor_rectangles):
        if flavor_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (255, 255, 255), flavor_rect, 3)

    for idx, text in enumerate(order_texts):
        rect = text.get_rect()
        rect.center = (800, 170 + idx * 75)

        screen.blit(text, rect)

    pygame.display.flip()

    if previous_size != len(created_order):
        print([flavors[flavor_id] for flavor_id in created_order])
        previous_size += 1
