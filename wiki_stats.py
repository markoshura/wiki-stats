#!/usr/bin/python3


import os
import sys
import math

import array

import statistics

from matplotlib import rc
rc('font', family='Droid Sans', weight='normal', size=14)

import matplotlib.pyplot as plt


class WikiGraph:

    def load_from_file(self, file):
        print('Загружаю граф из файла: ' + file)

        with open(file) as f:
            s=list(map(int, f.readline().split()))
            (n, _nlinks) = (s[0],s[1])

            self._titles = []
            self._sizes = array.array('L', [0]*n)
            self._links = array.array('L', [0]*_nlinks)
            self._redirect = array.array('B', [0]*n)
            self._offset = array.array('L', [0]*(n+1))

            for i in range(n):
                s=f.readline()
                s = s.rstrip()
                self._titles.append(s)
                s=list(map(int, f.readline().split()))
                self._sizes[i] = s[0]
                self._redirect[i] = s[1]
                for k in range(s[2]):
                    self._links[k] = int(f.readline())
                if i==0:
                    self._offset[i]=0
                else:
                    self._offset[i] = s[2]+self._offset[i-1]






        print('Граф загружен')

    def get_number_of_links_from(self, _id):
        pass

    def get_links_from(self, _id):
        pass

    def get_id(self, title):
        pass

    def get_number_of_pages(self):
        pass

    def is_redirect(self, _id):
        pass

    def get_title(self, _id):
        pass

    def get_page_size(self, _id):
        pass


def hist(fname, data, bins, xlabel, ylabel, title, facecolor='green', alpha=0.5, transparent=True, **kwargs):
    plt.clf()
    # TODO: нарисовать гистограмму и сохранить в файл


if __name__ == '__main__':
    wg = WikiGraph()
    wg.load_from_file('wiki_small.txt')

    # TODO: статистика и гистограммы
