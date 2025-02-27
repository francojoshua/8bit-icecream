import random
import pygame
from pygame.locals import *

pygame.init()

started = False
screen = pygame.display.set_mode([1024, 800])
pygame.display.set_caption('8bit Ice Cream')

# Flavors
flavors = [
    "Chocolate", "Mint", "Strawberry", "Butter Pecan", "Birthday Cake",
    "Vanilla", "Oreo", "Neopolitan", "Superman", "Cookie Dough"
]

# Instructions
instructions = [
    "Read the order",
    "Click respective flavors in order",
    "Press finish to START GAME",
    "Press delete to clear order",
]

# Font
font = pygame.font.Font('stardew-valley-stonks.ttf', 32)
instr_font = pygame.font.Font('stardew-valley-stonks.ttf', 20)


# Images
background = pygame.image.load('background.png')
cancel_image = pygame.image.load('cancel.png')
instruction_image = pygame.image.load('instructions.png')

level_one, level_two, level_three = [], [], []

for i in range(len(flavors)):
    level_one.append(pygame.image.load(f'0layer/{i}.png'))
    level_two.append(pygame.image.load(f'1layer/{i}.png'))
    level_three.append(pygame.image.load(f"2layer/{i}.png"))

cancel_rectangle = Rect(475, 400, 91, 91)
finish_rectangle = Rect(33, 379, 189, 86)


def generate_order(n_scoops):
    order = []

    for _ in range(n_scoops):
        num = random.randint(0, len(flavors) - 1)
        order.append(num)

    return order


instructions = [instr_font.render(item, True, (119, 113, 120)) for item in instructions]


def is_correct_order(order, correct_order):
    if len(order) != len(correct_order):
        return False

    for idx, scoop in enumerate(order):
        if scoop != correct_order[idx]:
            return False

    return True


created_order = []
correct_order = generate_order(3)
order_texts = []


def update_text():
    order_texts.clear()
    for item in correct_order:
        text = font.render(flavors[item], True, (119, 113, 120))
        order_texts.append(text)


update_text()

flavor_rectangles = [
    Rect(37, 527, 119, 116),  # CHOCOLATE,
    Rect(163, 527, 116, 116),  # MINT
    Rect(421, 528, 115, 114),  # STRAWBERRY
    Rect(544, 528, 121, 114),  # BUTTER PECAN
    Rect(673, 528, 121, 114),  # BIRTHDAY CAKE
    Rect(37, 648, 120, 116),  # VANILLA
    Rect(163, 648, 116, 116),  # OREO
    Rect(421, 649, 115, 114),  # NEOPOLITAN
    Rect(544, 649, 121, 114),  # SUPERMAN
    Rect(673, 649, 121, 113)  # COOKIE DOUGH
]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not started:
                if finish_rectangle.collidepoint(event.pos):
                    started = True
                continue

            for idx, flavor_rect in enumerate(flavor_rectangles):
                if flavor_rect.collidepoint(event.pos) and len(created_order) != 3:
                    created_order.append(idx)

            if cancel_rectangle.collidepoint(event.pos):
                created_order.clear()

            if finish_rectangle.collidepoint(event.pos):
                if is_correct_order(created_order, correct_order):
                    n_scoops = random.randint(1, 3)
                    correct_order = generate_order(n_scoops)
                    created_order.clear()
                    update_text()

    for flavor in flavor_rectangles:
        pygame.draw.rect(screen, (0, 0, 0), flavor)

    for rectangle in [finish_rectangle, cancel_rectangle]:
        pygame.draw.rect(screen, (0, 0, 0), rectangle)

    screen.blit(background, (0, 0))
    screen.blit(cancel_image, (0, 0))

    if not started:
        screen.blit(instruction_image, (0,0))

    for idx, item in enumerate(created_order):
        screen.blit(pygame.image.load(f'{idx}layer/{item}.png'), (0, 0))

    for idx, text in enumerate(order_texts if started else instructions):
        rectangle = text.get_rect()
        rectangle.center = (800, 170 + idx * 75)

        screen.blit(text, rectangle)

    pygame.display.flip()
