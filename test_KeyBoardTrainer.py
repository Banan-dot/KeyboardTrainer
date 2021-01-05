#!/usr/bin/env python3
import unittest
import pygame
import os
import sys
import InputBox as inputUser
import KeyBoardTrainer as f
from game_loop import Trainer as game
from States import Save
from colors import Color as Color
from loader import Loader as load


class TestTyping(unittest.TestCase):
    def test_numbers_3_4(self):
        self.assertEqual(12, 3 * 4)

    def test_get_lists_with_extension(self):
        if "win" in sys.platform:
            dictionary_music = {
                0: "La-Campanella.mp3",
                1: "Las Ketchup.mp3",
                2: "Never-Gonna-Give-You-Up.mp3",
                3: "Queen.mp3",
                4: "Rap God.mp3",
                5: "Shrek.mp3",
            }
            result = f.get_list_with_extension("./Music/", "mp3")
            self.assertEqual(result, dictionary_music)

    def test_init(self):
        trainer = game(1, 2, 3, "ъ.txt", "HardBass.mp3", True, '', '')
        self.assertEqual(trainer.velocity, 3)
        self.assertEqual(trainer.count_mistakes, 1)
        self.assertEqual(trainer.text_count, 2)
        self.assertEqual(trainer.text_name, "ъ.txt")
        self.assertEqual(trainer.music_name, "HardBass.mp3")
        self.assertTrue(trainer.enable_music)

    def test_subtract_letters(self):
        self.assertEqual((0, 0), game.subtract_letter(1, 2, 3))
        self.assertEqual((3, 1), game.subtract_letter(3, 2, 1))
        self.assertEqual((0, 0), game.subtract_letter(0, 2, 6))

    def test_add_letter(self):
        self.assertEqual((3, 3), game.add_letter(3, 2, 1))
        self.assertEqual((6, -2), game.add_letter(0, -2, 6))

    def test_skip_line(self):
        self.assertEqual((20, 0), game.skip_line([10, 20, 30], 5, 6))

    def test_back_line(self):
        self.assertEqual((5, 5), game.back_line([10, 20, 30], 5, 6))
        self.assertEqual((0, 0), game.back_line([12, 20, 30], 5, 6))

    def test_calculate_letters(self):
        correct_list = ['Jasdaa', 'Jadsasdo', 'Jdasdasdo']
        wrong_list = ['C', 'a', 'a']
        lines = '  \n\n\nasqkedpokqepod. FqepodaaJfwefewadsa. FdoJdasdewasdo'
        short_line = "Jasda"
        temp = game.calc_letters
        t_1 = temp(correct_list, 0, 0, correct_list, [12, 20, 30])
        t_2 = temp(correct_list, 0, 0, wrong_list, [12, 20, 30])
        t_3 = temp(lines, 6, 2, ['a', 'b', "plus"], [12, 20, 30])
        t_4 = temp(lines, 2, 3, ['a', "minus", 'b'], [12, 20, 30])
        t_5 = temp(lines, 2, 2, ['a', "line+", 'b'], [12, 20, 30])
        t_6 = temp(lines, 10, 2, ['a', 'b', "line-"], [12, 20, 30])
        t_7 = temp(lines, 1, 1, ['a', 'b', '#'], [12, 20, 30])
        t_8 = temp(lines, 1, 1, [' ', '\n', '\n', '\n', '#'], [12, 20, 30])
        t_9 = temp(short_line, 5, 3, ['a', 'b', 'a', 'b'], [12, 20, 30])
        self.assertEqual((3, 0), t_1)
        self.assertEqual((0, 3), t_2)
        self.assertEqual((6, 5), t_3)
        self.assertEqual((2, 4), t_4)
        self.assertEqual((12, 1), t_5)
        self.assertEqual((10, 2), t_6)
        self.assertEqual((1, 4), t_7)
        self.assertEqual((1, 6), t_8)
        self.assertEqual((5, 2), t_9)

    def test_draw_lines(self):
        w_d = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        trainer = game(1, 2, 3, "ъ.txt", "HardBass.mp3", True, w_d, '')
        lines = ["Aasqkedpokqepod", "FqepodaaJfwefewadsa", "FdoJdasdefasdo"]
        try:
            game.draw_lines(trainer, lines, 5, 2)
        except Exception as e:
            raise e

    def test_draw_lines_2(self):
        w_d = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        trainer = game(1, 2, 3, "ъ.txt", "HardBass.mp3", True, w_d, '')
        lines = 'Aasiooijoiqke'
        try:
            game.draw_lines(trainer, lines, 10, 6)
        except Exception as e:
            raise e

    def test_strip_lines(self):
        text = ['To be,\n', "to suffer\n"]
        t_1 = game.strip_lines(text)
        self.assertEqual(['To be, ', "to suffer "], t_1)

    def test_load_music(self):
        try:
            load.load_music("Shrek", 0.25)
        except Exception as e:
            raise e

    def test_load_text(self):
        try:
            load.load_text("Texts/Pushkin.txt")
        except Exception as e:
            raise e

    def test_load(self):
        file = Save()
        answer = file.get("daniil")
        tuple_answer = (answer[0], answer[1], answer[2], answer[3])
        self.assertEqual(tuple_answer, f.load("daniil", file))

    def test_save_state(self):
        file = Save()
        try:
            f.save_state("my_file", 1010, 10100, 2, file, [])
        except Exception as e:
            raise e


if __name__ == '__main__':
    unittest.main()
