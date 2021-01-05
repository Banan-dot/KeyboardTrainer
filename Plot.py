import os
import matplotlib.pyplot as plt
import numpy as np


class Plot:
    def __init__(self, list_points, nickname):
        self.points = list_points
        self.nick = nickname

    def construction_graphic(self):
        plt.figure()
        x = np.arange(0, len(self.points))
        plt.plot(self.points)
        plt.title('Dynamic training')
        plt.fill_between(x, self.points)
        plt.grid(True)
        plt.xlabel("Training number")
        plt.ylabel("Points")
        Plot.save_png("Plot_" + self.nick, 'png')

    @staticmethod
    def save_png(name='', fmt='Plot'):
        pwd = os.getcwd()
        i_path = './Images/{}'.format(fmt)
        if not os.path.exists(i_path):
            os.makedirs(i_path)
        os.chdir(i_path)
        plt.savefig('{}.{}'.format(name, fmt), fmt='png', dpi=150)
        os.chdir(pwd)


def main():
    plot = Plot([1, 6, 2, 3, 9, -2], "Efrosiy")
    plot.construction_graphic()


if __name__ == "__main__":
    main()
