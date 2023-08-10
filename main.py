import pygame as pg
import sys
import random

ARRAY_LENGTH = 10  # Not to be changed


class Block:

    def __init__(self, n: int) -> None:
        self.num = n
        self.x = 100 + (len(blocks) * 60)
        self.y = 725 - (n * 6)
        self.w = 40
        self.h = n * 6
        self.rect = pg.rect.Rect(self.x, self.y, self.w, self.h)
        self.colour = (255, 255, 255)
        self.text_font = pg.font.SysFont("Consolas", 40)

    def display_amount(self, display_surface: pg.Surface):
        text = self.text_font.render(str(self.num), True, (255, 255, 255))
        x = self.rect.centerx - text.get_width() // 2
        y = self.rect.y - text.get_height()
        display_surface.blit(text, (x, y))

    def display(self, display_surface: pg.Surface) -> None:
        pg.draw.rect(display_surface, self.colour, self.rect)


blocks: list[Block] = []
states: list[list[int]] = []
indices: list[list[int]] = []


def display(display_surface: pg.Surface, n, x: int, y: int,
            font: pg.font.Font) -> None:
    text = font.render(str(n), True, (0, 255, 255))
    display_surface.blit(text, (x, y))


def sort(arr: list[int]) -> None:
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            swapped = False
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
            states.append(arr.copy())
            indices.append([i, j, swapped])


def main() -> None:

    global blocks
    pg.init()
    screen = pg.display.set_mode((800, 800))
    pg.display.set_caption("Bubble Sort Visualisation")

    clock = pg.time.Clock()

    array = [random.randint(1, 100) for _ in range(ARRAY_LENGTH)]
    sort(array)

    timer_font = pg.font.SysFont("Consolas", 100)
    final_font = timer_font
    pass_font = pg.font.SysFont("Consolas", 50)
    comp_font = pg.font.SysFont("Consolas", 25)

    comp_rect = pg.rect.Rect(0, 750, 100, 20)

    running = True
    finished = False
    display_info = True
    display_comp = True
    timer = 0
    update = 10

    while running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False

        if (timer // update) < 45:
            if not (timer % update):
                blocks.clear()
                for i in states[max(0, timer // update - 1)]:
                    blocks.append(Block(i))
            if (timer // update) == 44:
                display_comp = False
        elif (timer // update) == 45:
            finished = True
            display_info = False

        screen.fill((0, 0, 0))

        for i in blocks:
            i.display(screen)
            i.display_amount(screen)

        text = timer_font.render(str(timer // update), True, (0, 255, 255))
        screen.blit(text, (20, 20))

        if display_info:

            pass_no = str(indices[timer // update][0] + 1)
            text2 = "Pass " + pass_no
            pass_text = pass_font.render(text2, True, (255, 255, 0))
            xcoord = screen.get_rect().centerx - pass_text.get_width() // 2
            screen.blit(pass_text, (xcoord, 20))

            comp_no = indices[timer // update][1]
            text3 = "Comparing " + str(comp_no + 1) + "th and " \
                    + str(comp_no + 2) + "th element"
            comp_text = comp_font.render(text3, True, (255, 255, 0))
            xcoord = screen.get_rect().centerx - comp_text.get_width() // 2
            screen.blit(comp_text, (xcoord, 70))

        if display_comp:

            if indices[(timer // update)][2]:
                comp_rect_colour = (255, 0, 0)
            else:
                comp_rect_colour = (0, 255, 0)
            comp_rect.x = 100 + indices[(timer // update)][1] * 60
            pg.draw.rect(screen, comp_rect_colour, comp_rect)

        if finished:
            finished_text = final_font.render("Sorted", True, (0, 255, 0))
            screen.blit(finished_text,
                        (400 - finished_text.get_width() / 2, 20))
        else:
            timer += 1

        pg.display.update()

        clock.tick(60)

    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
