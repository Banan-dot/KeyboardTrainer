#!/usr/bin/env python3
import shelve


class Save:
    def __init__(self):
        self.file = shelve.open('./States/data')

    def add(self, name, points, velocity, text_count, list_points):
        self.file[name] = [points, velocity, text_count, list_points]

    def get(self, name):
        try:
            return self.file[name]
        except KeyError:
            return [0, 0, 0, [0]]

    def get_tuple(self):
        for i in self.file.items():
            try:
                users.append(i)
            except KeyError:
                user.append([0, 0, 0, [0]])
        return users

    def get_items(self):
        return self.file.items()

    def get_keys(self):
        keys = []
        for user in self.file.keys():
            keys.append(user)
        return keys

    def get_values(self):
        values = []
        for elements in self.file.values():
            values.append(elements)
        return values
