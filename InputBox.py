#!/usr/bin/env python3
import pygame as pg
import clipboard

pg.init()
screen = pg.display.set_mode((1340, 735))
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 100)
FONT_BOX = pg.font.Font(None, 40)

inputString = ""

ctrl = False


class InputBox:
    def __init__(self, x, y, w, h, my_text, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.my_text = my_text

    def handle_event(self, event):
        global ctrl
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                quit()
            if self.active:
                if event.key == pg.K_RETURN:
                    if self.text != "":
                        return self.text
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pg.K_LCTRL:
                    ctrl = True
                elif event.key == pg.K_v and ctrl:
                    ctrl = False
                    self.text = clipboard.paste()
                else:
                    if event.unicode != "{" and event.unicode != "}" and (self.my_text or len(self.text) < 13):
                        self.text += event.unicode
                self.txt_surface = FONT_BOX.render(self.text, True, self.color)

    def update(self):
        width = max(150, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        text = FONT.render(inputString, True, COLOR_ACTIVE)
        screen.blit(text, (100, 100))
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pg.draw.rect(screen, self.color, self.rect, 2)


def main(my_text=False):
    global text
    clock = pg.time.Clock()
    input_box1 = InputBox(200, 300, 50, 50, my_text)
    done = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            text = input_box1.handle_event(event)
        input_box1.update()
        screen.fill((30, 30, 30))
        input_box1.draw(screen)
        if text is not None:
            a = text
            text = None
            return a

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
    pg.quit()
