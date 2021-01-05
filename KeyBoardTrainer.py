#!/usr/
# bin/env python3
# -*- coding: utf-8 -*-
import pygame
import threading
import os
import InputBox as inputUser
import time
from game_loop import Trainer as game
from States import Save
from colors import Color as Color

w_d = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("KeyBoard trainer")
font = pygame.font.SysFont(None, 40, "Monaco")
SIZE = 15

font_article = pygame.font.SysFont(None, 100)

dict_texts_article = {
    0: font_article.render("Choose text, please", True, Color.BLACK.value),
    1: font_article.render("...and music", True, Color.BLACK.value),
    2: font_article.render("Choose mode", True, Color.BLACK.value)
}


def get_list_with_extension(directory, extension):
    dictionary = {}
    files = os.listdir(directory)
    files = [i.encode('utf-8').decode('utf-8') for i in files]
    result = filter(lambda x: x.endswith(extension), files)
    for i, j in enumerate(result):
        dictionary[i] = j
    return dictionary


def get_music(music_list, article):
    y = 250
    width = 200
    height = 100
    font_text = pygame.font.SysFont(None, 35)
    line = "Без музыки (without music)"
    without = font_text.render(line, True, Color.BLACK.value)
    without_rect = pygame.Rect(600, 520, 400, 60)
    without_x_y = (650, 550)
    rectangles = []
    for row in range(250, 380, 125):
        for x in range(150, 700, y):
            if x == 650 and row == 250:
                rectangles.append(pygame.Rect(x, row, width * 2 + 20, height))
                continue
            rectangles.append(pygame.Rect(x, row, width, height))
    rectangles.append(without_rect)
    while True:
        w_d.fill(Color.WHITE.value)
        w_d.blit(article, (200, 100))
        pygame.draw.rect(w_d, Color.GREEN.value, without_rect)
        w_d.blit(without, without_x_y)
        for j, i in enumerate(rectangles):
            if j == 6:
                break
            pygame.draw.rect(w_d, Color.RED.value, i)
            curr_text = music_list[j].split(".")[0]
            font = font_text.render(curr_text, True, Color.BLACK.value)
            if i.x == 650 and i.y == 250:
                w_d.blit(font, (i.centerx - width + 20, i.centery))
            else:
                w_d.blit(font, (i.centerx - width // 2 + 20, i.centery))
        key = click_handling(rectangles)
        if key is not None:
            if key != -1:
                return True, music_list[key]
            else:
                return False, 0
        pygame.display.update()


def get_text_name(text_list, article):
    my_text = "Your text"
    rectangles = []
    y = 250
    width = 200
    height = 100
    coord = (100, 100)
    for x in range(150, 950, y):
        rectangles.append(pygame.Rect(x, y, width, height))
        rectangles.append(pygame.Rect(x, y + y // 2, width, height))
        rectangles.append(pygame.Rect(x, 2 * y, width, height))
    itself_text = pygame.Rect(900, height, width, height)
    rectangles.append(itself_text)
    while True:
        font_text = pygame.font.SysFont(None, 35)
        w_d.fill(Color.WHITE.value)
        w_d.blit(article, coord)
        for j, i in enumerate(rectangles):
            if j == 12:
                pygame.draw.rect(w_d, Color.GREEN.value, itself_text)
                curr_font = font_text.render(my_text, True, Color.BLACK.value)
                w_d.blit(curr_font, (i.centerx - width // 2 + 20, i.centery))
                break
            pygame.draw.rect(w_d, Color.RED.value, i)
            curr_text = text_list[j].split(".")[0]
            curr_font = font_text.render(curr_text, True, Color.BLACK.value)
            w_d.blit(curr_font, (i.centerx - width // 2 + 20, i.centery))
        key = click_handling(rectangles)
        if key is not None:
            if key != -2:
                return text_list[key]
            else:
                return "Yes"
        pygame.display.update()


def get_type_mode(article):
    y = 400
    x = 200
    width = 300
    height = 100
    rectangles = [
        pygame.Rect(x, y, width, height),
        pygame.Rect(width * 2, y, width, height)]
    coord = (100, 100)
    text_list = ["Стандарт", "На время"]
    font_text = pygame.font.SysFont(None, 50)
    while True:
        w_d.fill(Color.WHITE.value)
        w_d.blit(article, coord)
        for j, i in enumerate(rectangles):
            pygame.draw.rect(w_d, Color.AQUA.value, i)
            curr_text = text_list[j].split(".")[0]
            curr_font = font_text.render(curr_text, True, Color.BLACK.value)
            w_d.blit(curr_font, (i.centerx - width // 2 + 40, i.centery))
        key = click_handling(rectangles)
        if key is not None:
            return text_list[key]
        pygame.display.update()


def click_handling(rectangles):
    dict_rect = {}
    for j, i in enumerate(rectangles):
        dict_rect[j] = i
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            for j in dict_rect.keys():
                if dict_rect[j].collidepoint(event.pos):
                    if dict_rect[j] == pygame.Rect(600, 520, 400, 60):
                        return -1
                    if dict_rect[j] == pygame.Rect(900, 100, 200, 100):
                        return -2
                    return j
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            quit()
    return None


def load(username, file):
    result = file.get(username)
    return result[0], result[1], result[2], result[3]


def save_state(curr_user, points, velocity, text_count, file, list_points):
    file.add(curr_user, points, velocity, text_count, list_points)


def main(page_size=SIZE):
    my_text = False
    file = Save()
    inputUser.inputString = "Write your nickname..."
    curr_user = inputUser.main()
    pygame.init()
    text_list = get_list_with_extension("./Texts/", ".txt")
    music_list = get_list_with_extension("./Music/", ".mp3")

    text_name = get_text_name(text_list, dict_texts_article[0])
    if text_name == "Yes":
        inputUser.inputString = "Write your text path:"
        my_text = True
        text_name = inputUser.main(my_text)
    enable_music, music_name = get_music(music_list, dict_texts_article[1])
    type_mode = get_type_mode(dict_texts_article[2])
    trainer = \
        game(0, 0, 0, text_name, music_name, enable_music, w_d, type_mode, my_text)
    if curr_user not in file.get_keys():
        save_state(curr_user.format(text_name), 0, 0, 0, file, [0])
    points, velocity, text_count, list_points = load(curr_user, file)
    curr_velocity, curr_points = \
        trainer.trainer_loop(curr_user, text_name, page_size)
    if curr_points > points:
        points = curr_points
    average_sp = (curr_velocity + velocity) / 2
    list_points.append(curr_points)
    p1 = threading.Thread(target=save_state, args=(curr_user, points, average_sp, text_count + 1, file, list_points))
    p1.start()
    p1.join()
    trainer.get_high_score(file, curr_user, list_points)


if __name__ == '__main__':
    main()
