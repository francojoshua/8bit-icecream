import random
import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode([1024, 800])

# Flavors
flavors = [
    "Chocolate", "Mint", "Strawberry", "Butter Pecan", "Birthday Cake",
    "Vanilla", "Oreo", "Neopolitan", "Superman", "Cookie Dough"
]

# Font
font = pygame.font.Font('stardew-valley-stonks.ttf', 32)

# Images
background = pygame.image.load('background.png')
cancel_image = pygame.image.load('cancel.png')

level_one, level_two = [], []
for i in range(len(flavors)):
    level_one.append(pygame.image.load(f'0layer/{i}.png'))
    level_two.append(pygame.image.load(f'1layer/{i}.png'))

cancel_rectangle = Rect(475, 400, 91, 91)
finish_rectangle = Rect(33, 379, 189, 86)

finish_sound = pygame.mixer.Sound('finish.mp3')  # From https://www.youtube.com/watch?v=uiBkqnBh-B0
click_sound = pygame.mixer.Sound('click.mp3')  # From https://www.youtube.com/watch?v=h8y0JMVwdmM


def generate_order(n_scoops):
    order = []

    for _ in range(n_scoops):
        num = random.randint(0, len(flavors) - 1)
        order.append(num)

    extra_topping_choice = random.randint(1, 4)

    return order, extra_topping_choice == 1, extra_topping_choice == 2


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


created_order, created_fudge, created_sprinkles = [], False, False
correct_order, correct_sprinkles, correct_fudge = generate_order(2)


order_texts = []
def update_text():
    order_texts.clear()
    for item in correct_order:
        text = font.render(flavors[item], True, (119, 113, 120))
        order_texts.append(text)

    if correct_sprinkles or correct_fudge:
        text = font.render("Fudge" if correct_fudge else "Sprinkles", True, (119, 113, 120))
        order_texts.append(text)


def play_sound(sound):
    pygame.mixer.Sound.play(sound)
    pygame.mixer.music.stop()


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

fudge_points = [
    (869, 659), (861, 659), (860, 658), (832, 658), (814, 611), (813, 590),
    (833, 530), (835, 518), (833, 507), (828, 487), (823, 468), (849, 452),
    (857, 452), (857, 432), (837, 429), (891, 431), (893, 451), (892, 455),
    (927, 469), (929, 476), (920, 509), (921, 531), (930, 556), (922, 557),
    (913, 560), (902, 566), (891, 576), (879, 588), (871, 604), (868, 671),
    (859, 620), (859, 642), (862, 644), (869, 645), (869, 659)
]

sprinkles_points = [
    (1001, 781), (874, 777), (873, 767), (872, 762), (871, 738),
    (872, 723), (871, 710), (870, 690), (870, 643), (863, 643),
    (863, 621), (872, 621), (872, 608), (885, 587), (907, 568),
    (924, 560), (955, 561), (993, 589), (1008, 613), (1008, 619),
    (1015, 619), (1018, 631), (1019, 639), (1007, 644), (1001, 777)
]


fudge_rect = None
sprinkles_rect = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for idx, flavor_rect in enumerate(flavor_rectangles):
                if flavor_rect.collidepoint(event.pos) and len(created_order) != 2:
                    created_order.append(idx)
                    play_sound(click_sound)

            if cancel_rectangle.collidepoint(event.pos):
                created_order.clear()
                created_sprinkles = False
                created_fudge = False

                play_sound(click_sound)

            if fudge_rect and fudge_rect.collidepoint(event.pos):
                created_fudge = not created_fudge
                play_sound(click_sound)

            if sprinkles_rect and sprinkles_rect.collidepoint(event.pos):
                created_sprinkles = not created_sprinkles
                play_sound(click_sound)

            if finish_rectangle.collidepoint(event.pos):
                created_components = (created_order, created_sprinkles, created_fudge)
                correct_components = (correct_order, correct_sprinkles, correct_fudge)

                if is_correct_order(created_components, correct_components):
                    pygame.mixer.Sound.play(finish_sound)
                    pygame.mixer.music.stop()

                    n_scoops = random.randint(1, 2)
                    correct_order, correct_sprinkles, correct_fudge = generate_order(n_scoops)
                    created_sprinkles = False
                    created_fudge = False
                    created_order.clear()
                    update_text()

    for flavor in flavor_rectangles:
        pygame.draw.rect(screen, (0, 0, 0), flavor)

    for rectangle in [finish_rectangle, cancel_rectangle]:
        pygame.draw.rect(screen, (0, 0, 0), rectangle)

    sprinkles_rect = pygame.draw.polygon(screen, (0, 0, 0), sprinkles_points)
    fudge_rect = pygame.draw.polygon(screen, (255, 255, 255), fudge_points)

    screen.blit(background, (0, 0))

    screen.blit(cancel_image, (0, 0))

    for idx, item in enumerate(created_order):
        screen.blit(pygame.image.load(f'{idx}layer/{item}.png'), (0, 0))

    if len(created_order) != 0:
        layer = len(created_order) - 1
        if created_fudge:
            screen.blit(pygame.image.load(f'{layer}layer/fudge.png'), (0, 0))
        if created_sprinkles:
            screen.blit(pygame.image.load(f'{layer}layer/sprinkles.png'), (0, 0))

    for idx, flavor_rect in enumerate(flavor_rectangles):
        if flavor_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (255, 255, 255), flavor_rect, 3)

    for idx, text in enumerate(order_texts):
        rectangle = text.get_rect()
        rectangle.center = (800, 170 + idx * 75)

        screen.blit(text, rectangle)

    pygame.display.flip()
