import pygame
from loader import Loader as f
from colors import Color as Color
import time
import random as rnd
import os
import Plot as plt
import threading

SIZE = 15
FPS = 60

shift = False
caps = False
backspace = False
backspacePressed = False
enter = False
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40, "Monaco")
wrong_sound = pygame.mixer.Sound("./Music/WrongSound.ogg")


class Trainer:
    window_display = None

    def __init__(self,
                 c_mistakes,
                 t_count,
                 vel,
                 t_name,
                 m_name,
                 e_music,
                 wd,
                 type_mode,
                 is_my_text=False):
        self.count_mistakes = c_mistakes
        self.text_count = t_count
        self.velocity = vel
        self.text_name = t_name
        self.music_name = m_name
        self.page_size = 15
        self.fps = 60
        self.enable_music = e_music
        self.points = 0
        self.window_display = wd
        self.type_mode = type_mode
        self.count_time = 0
        self.my_text = is_my_text

    @staticmethod
    def subtract_letter(correct_letters, wrong_letters, number):
        if wrong_letters >= number:
            wrong_letters -= number
            number = 0
        else:
            number -= wrong_letters
            wrong_letters = 0
        if correct_letters >= number:
            correct_letters -= number
        else:
            correct_letters = 0
        return correct_letters, wrong_letters

    @staticmethod
    def add_letter(correct_letters, wrong_letters, number):
        if wrong_letters > 0:
            wrong_letters += number
        else:
            correct_letters += number
        return correct_letters, wrong_letters

    @staticmethod
    def skip_line(line_lengths, correct_letters, wrong_letters):
        index = 0
        total_letters = correct_letters + wrong_letters
        for length in line_lengths:
            if total_letters >= length:
                index += 1
            else:
                break
        assert index < len(line_lengths)
        correct_letters = line_lengths[index]
        wrong_letters = 0
        return correct_letters, wrong_letters

    @staticmethod
    def back_line(line_lengths, correct_letters, wrong_letters):
        index = 0
        total_letters = correct_letters + wrong_letters
        for length in line_lengths:
            if total_letters > length:
                index += 1
            else:
                break

        if index > 0:
            length = total_letters - line_lengths[index - 1]
            correct_letters, wrong_letters = \
                Trainer.subtract_letter(correct_letters, wrong_letters, length)
        else:
            correct_letters = 0
            wrong_letters = 0
        return correct_letters, wrong_letters

    @staticmethod
    def calc_letters(lines, correct_letters, wrong_letters, pressed, line_len):
        global enter
        for letter in pressed:
            try:
                current_letter = lines[correct_letters + wrong_letters]
            except IndexError:
                wrong_letters -= 1
                return correct_letters, wrong_letters
            if letter in ["plus", "#"]:
                correct_letters, wrong_letters = \
                    Trainer.add_letter(correct_letters, wrong_letters, 1)
            elif letter in ["minus", "\b"]:
                correct_letters, wrong_letters = \
                    Trainer.subtract_letter(correct_letters, wrong_letters, 1)
            elif letter == "line+":
                correct_letters, wrong_letters = \
                    Trainer.skip_line(line_len, correct_letters, wrong_letters)
            elif letter == "line-":
                correct_letters, wrong_letters = \
                    Trainer.back_line(line_len, correct_letters, wrong_letters)
            elif letter in ["\n", " "] and current_letter in ["\n", " "]:
                correct_letters, wrong_letters = \
                    Trainer.add_letter(correct_letters, wrong_letters, 1)
            else:
                if letter != current_letter \
                        and not (enter and current_letter == " "):
                    wrong_sound.play()
                    wrong_sound.set_volume(0.05)
                    wrong_letters += 1
                elif enter and current_letter == " ":
                    enter = False
                    correct_letters, wrong_letters = \
                        Trainer.add_letter(correct_letters, wrong_letters, 2)
                else:
                    correct_letters, wrong_letters = \
                        Trainer.add_letter(correct_letters, wrong_letters, 1)
        return correct_letters, wrong_letters

    def draw_lines(self, lines, correct_letters, wrong_letters):
        for line_num, line in enumerate(lines):
            self.draw_text(line, line_num, correct_letters, wrong_letters)
            if correct_letters >= len(line):
                correct_letters -= len(line)
            elif not (correct_letters == 0 and wrong_letters == 0):
                line_remaining = len(line) - correct_letters
                correct_letters = 0
                if line_remaining > wrong_letters:
                    wrong_letters = 0
                else:
                    wrong_letters -= line_remaining

    def draw_text(self, line, line_num, c_let, wr_letters, f_line=(50, 100)):
        line_space = 30
        w_text = line[c_let: c_let + wr_letters]
        n_text = line[c_let + wr_letters:]
        c_text = line[:c_let]

        w_text = w_text.replace(" ", chr(9209))

        wrong_text = font.render(w_text, True, Color.RED.value)
        normal_text = font.render(n_text, True, Color.BLACK.value)
        correct_text = font.render(c_text, True, Color.GREEN.value)

        wrong_rect = wrong_text.get_rect()
        normal_rect = normal_text.get_rect()
        correct_rect = correct_text.get_rect()
        correct_rect.topleft = \
            (f_line[0], f_line[1] + line_space * line_num)
        if c_let == 0:
            correct_rect.size = (0, 0)
        wrong_rect.left, wrong_rect.top = correct_rect.right, correct_rect.top
        if wr_letters == 0:
            wrong_rect.size = (0, 0)
        normal_rect.left, normal_rect.top = wrong_rect.right, wrong_rect.top
        self.window_display.blit(correct_text, correct_rect)
        self.window_display.blit(wrong_text, wrong_rect)
        self.window_display.blit(normal_text, normal_rect)

    @staticmethod
    def strip_lines(text):
        new_text = []
        for line in text:
            # temp = len(line) * 53
            new_text.append(line.strip() + " ")
        return new_text

    def trainer_loop(self, curr_user, filename, page_size, start=0):
        count_mistakes = 0
        cor_letrs = 0
        wr_letrs = 0
        speed = 0
        temp = 0
        coord = (800, 50)
        coord_1 = (800, 400)
        minute = 60
        count_cor_lettrs = 0
        on_time = False
        stop = False
        if self.type_mode == "На время":
            on_time = True
        start_time = time.time()
        if self.enable_music:
            pygame.mixer.music.load("./Music/{}".format(self.music_name))
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(0.05)
        if not self.my_text:
            text, symbol_count = f.load_text("./Texts/" + filename)
        else:
            text, symbol_count = f.load_text(filename)
        self.count_time = rnd.randint(symbol_count // 6, symbol_count // 6 + 20)
        if len(text) < page_size:
            page_size = len(text)
        page_number = start // page_size
        text = self.strip_lines(text)
        self.window_display.fill(Color.WHITE.value)
        pygame.display.update()
        while page_number * page_size < len(text):
            i_1 = (page_number + 1) * page_size
            lines = text[page_number * page_size: i_1]
            lines[0] = lines[0].lstrip()
            line = "".join(lines)
            lines_length = len(line)
            l_len = []
            for i in range(len(lines)):
                l_len.append(len(lines[i]))
                if i > 0:
                    l_len[i] += l_len[i - 1]
            while lines_length > cor_letrs:
                typed = event_handling()
                self.window_display.fill(Color.WHITE.value)
                s = "Page: {}"
                self.draw_text(s.format(page_number + 1), 0, 0, 0, coord)
                self.draw_lines(lines, cor_letrs, wr_letrs)
                mistakes = "Count mistakes: {}".format(count_mistakes)
                if on_time:
                    curr_time = self.count_time - (time.time() - start_time)
                else:
                    curr_time = time.time() - start_time
                time_str = "Time: %.2f" % curr_time
                self.draw_text(mistakes, 2, 0, 0, coord)
                self.draw_text(time_str, 4, 0, 0, coord)
                s = "User: {}"
                self.draw_text(s.format(curr_user), 6, 0, 0, coord)
                cor_letrs, wr_letrs = \
                    self.calc_letters(line, cor_letrs, wr_letrs, typed, l_len)

                if temp < wr_letrs:
                    count_mistakes += 1
                if count_cor_lettrs < cor_letrs:
                    count_cor_lettrs = cor_letrs
                curr_speed = minute * (count_mistakes + count_cor_lettrs) / (time.time() - start_time)
                speed = (curr_speed + speed) / 2
                curr_speed_str = "Speed: %.2f" % speed
                self.draw_text(curr_speed_str, 3, 0, 0, coord)

                possible_wrong = lines_length - cor_letrs
                if possible_wrong < wr_letrs:
                    wr_letrs = possible_wrong
                pygame.display.update()
                clock.tick(FPS)
                if curr_time <= 1e-5:
                    stop = True
                    break
                temp = wr_letrs
            cor_letrs = 0
            wr_letrs = 0
            page_number += 1
            if stop:
                break
        if on_time:
            finish_time = time.time() - start_time
            if finish_time > self.count_time:
                average_velocity = \
                    minute * (count_mistakes + count_cor_lettrs) / self.count_time
            else:
                average_velocity = \
                    minute * (count_mistakes + count_cor_lettrs) / finish_time
        else:
            average_velocity = \
                minute * symbol_count / (time.time() - start_time)
        if count_mistakes != 0:
            self.points = 5 * average_velocity // count_mistakes
        else:
            self.points = 5 * average_velocity
        self.window_display.fill(Color.WHITE.value)

        average_vel = "Average speed: %.2f s / min" % average_velocity
        self.draw_text(average_vel, 1, 0, 0, coord_1)
        self.draw_text("User: {}".format(curr_user), 3, 0, 0, coord_1)
        s = "Mistakes: {}"
        self.draw_text(s.format(count_mistakes), 4, 0, 0, coord_1)
        self.velocity = average_velocity
        if on_time:
            s = "Your points: %.2f"
            self.draw_text(s % self.points, 2, 0, 0, coord_1)
        else:
            if count_mistakes != 0:
                points = 5 * average_velocity // count_mistakes
            else:
                points = 5 * average_velocity
            s = "Your points: %.2f"
            self.draw_text(s % points, 2, 0, 0, coord_1)
        return self.velocity, self.points

    def draw_images(self):
        if self.points > 400:
            image_balgej = pygame.image.load("./Images/Baldej.jpg")
            self.window_display.blit(image_balgej, (800, 200))
            self.window_display.blit(image_balgej, (1000, 200))
        elif 200 <= self.points <= 400:
            image_good = pygame.image.load("./Images/Good.jpg")
            self.window_display.blit(image_good, (820, 10))
        else:
            image_train = pygame.image.load("./Images/Trenirovka.jpg")
            self.window_display.blit(image_train, (850, 150))

    def get_high_score(self, file, user, list_points):
        w_space = 2
        list_tuple = list(file.get_items())
        list_tuple.sort(key=lambda jojo: jojo[1])
        list_tuple.reverse()
        draw_name = "%d.%s"
        s = "Highscore table (nickname -- points, text count):"
        self.draw_text(s, 0, 0, 0)
        space_tuple = (670, 100)
        points_tuple = (400, 100)
        self.draw_text("Name", 2, 0, 0)
        self.draw_text("Points", 2, 0, 0, points_tuple)
        self.draw_text("Texts", 2, 0, 0, space_tuple)
        for j, i in enumerate(list_tuple):
            if j == 16:
                break
            if user == i[0]:
                if j > 8:
                    w_space = 3
                temp = len(i[0]) + len(str(j)) + w_space - 1
                self.draw_text(
                    draw_name % (j + 1, i[0]), j + 4, temp, 0)
                self.draw_text(
                    "%.2f" % (i[1][0]), j + 4, 0, 0, points_tuple)
                self.draw_text(
                    "%d" % (i[1][2]), j + 4, 0, 0, space_tuple)
            else:
                self.draw_text(
                    draw_name % (j + 1, i[0]), j + 4, 0, 0)
                self.draw_text(
                    "%.2f" % (i[1][0]), j + 4, 0, 0, points_tuple)
                self.draw_text(
                    "%d" % (i[1][2]), j + 4, 0, 0, space_tuple)
        plot_rect = pygame.Rect(800, 600, 500, 100)
        font_text = pygame.font.SysFont(None, 50)
        curr_font = font_text.render("Dynamic of training", True, Color.BLACK.value)
        pygame.draw.rect(self.window_display, Color.AQUA.value, plot_rect)
        self.window_display.blit(curr_font, (plot_rect.centerx - 100, plot_rect.centery))
        while True:
            is_true = event_handling_high_score(plot_rect, list_points, user)
            if is_true == 42:
                pygame.quit()
                quit()
            elif is_true:
                self.window_display.fill(Color.WHITE.value)
                image_plot = pygame.image.load("./Images/png/Plot_{}.png".format(user))
                self.window_display.blit(image_plot, (10, 10))
            pygame.display.update()


def get_plot(points, nickname):
    plot = plt.Plot(points, nickname)
    t = threading.Thread(target=plot.construction_graphic)
    t.start()
    t.join()
    return True


def event_handling_high_score(rectangle, points, nickname):
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rectangle.collidepoint(event.pos):
                return get_plot(points, nickname)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return 42
    return None


def event_handling():
    global shift
    global caps
    global backspace
    global backspacePressed
    global enter
    pressed = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            elif event.key == pygame.K_LSHIFT:
                shift = True
            elif event.key == pygame.K_RSHIFT:
                shift = True
            elif event.key == pygame.K_CAPSLOCK:
                caps = not caps
            elif event.key == pygame.K_RETURN:
                enter = True
            elif event.key == pygame.K_RIGHT:
                pressed.append("plus")
            elif event.key == pygame.K_LEFT:
                pressed.append("minus")
            elif event.key == pygame.K_UP:
                pressed.append("line-")
            elif event.key == pygame.K_DOWN:
                pressed.append("line+")
            elif event.unicode != '':
                pressed.append(event.unicode)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                shift = False
            elif event.key == pygame.K_CAPSLOCK:
                caps = not caps
            # Не всегда происходит событие KEYUP после закрытия ключа KEYDOWN
    if backspace:
        backspacePressed = True
        pressed.append("\b")
        pygame.time.wait(100)
    return pressed
