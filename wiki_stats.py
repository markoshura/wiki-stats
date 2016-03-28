
import os
import sys
import math

import array

import statistics

from matplotlib import rc
rc('font', family='DejaVu Sans', weight='normal', size=14)

import matplotlib.pyplot as plt


class WikiGraph:

    def load_from_file(self, file):
        print('Загружаю граф из файла: ' + file)

        with open(file) as f:
            (n, _nlinks) = (map(int, f.readline().split()))
            self._titles = []

            self._sizes = array.array('L', [0]*n)
            self._links = array.array('L', [0]*_nlinks)
            self._redirect = array.array('B', [0]*n)
            self._offset = array.array('L', [0]*(n+1))
            n_lks = 0
            for i in range(n):
                self._titles.append(f.readline().rstrip())
                (size, redirect, lks) = (map(int, f.readline().split()))
                self._sizes[i] = size
                self._redirect[i] = redirect
                for j in range(n_lks, n_lks + lks):
                    self._links[j] = int(str(f.readline()))
                n_lks += lks
                self._offset[i+1] = self._offset[i] + lks


        print('Граф загружен')

    def get_number_of_links_from(self, _id):
        return len(self._links[self._offset[_id]:self._offset[_id+1]])

    def get_links_from(self, _id):
        return self._links[self._offset[_id]:self._offset[_id+1]]

    def get_id(self, title):
        for i in range(len(self._titles)):
            if self._titles[i] == title:
                return(i)

    def get_number_of_pages(self):
        return len(self._titles)

    def is_redirect(self, _id):
        return self._redirect[_id]

    def get_title(self, _id):
        return self._titles[_id]

    def get_page_size(self, _id):
        return self._sizes(_id)


def analyse_links_from_page(G):
    numlinks_from = list(map(G.get_number_of_links_from, range(G.get_number_of_pages())))
    _max = max(numlinks_from)
    _min = min(numlinks_from)
    mxn = sum(x == _max for x in numlinks_from)
    mnn = sum(x == _min for x in numlinks_from)
    print("Минимальное количество:", _min)
    print("Количество статей с минимальным количеством ссылок:", mnn)
    print("Максимальное количество ссылок из статьи:", _max)
    print("Количество статей с максимальным количеством ссылок:", mxn)
    found_id = None
    for i in range(G.get_number_of_pages()):
        if G.get_number_of_links_from(i) == _max:
            found_id = i
            break
    print("Статья с наибольшим количеством внешних ссылок:",  G.get_title(found_id))
    print("Среднее количество внешних ссылок на статью: %0.2f  (ср. откл. : %0.2f)" %(statistics.mean(numlinks_from), statistics.stdev(numlinks_from)))

def analyse_links_to_page(G):
    numlinks_to = [0 for i in range(G.get_number_of_pages())]
    for i in range(G.get_number_of_pages()):
        for x in G.get_links_from(i):
            numlinks_to[x] += 1
            if G.is_redirect(i) == 1:
                numlinks_to[x] -= 1
    _max = max(numlinks_to)
    _min = min(numlinks_to)
    mxn = sum(x == _max for x in numlinks_to)
    mnn = sum(x == _min for x in numlinks_to)
    print("Минимальное количество ссылок на статью:", _min)
    print("Количество статей с минимальным количеством внешних ссылок:", mnn)
    print("Максимальное количество ссылок на статью:", _max)
    print("Количество статей с максимальным количеством внешних ссылок:", mxn)
    found_id = None
    for i in range(G.get_number_of_pages()):
        if numlinks_to[i] == _max:
            found_id = i
            break
    print("Статья с наибольшим количеством внешних ссылок:",  G.get_title(found_id))
    print("Среднее количество внешних ссылок на статью: %0.2f  (ср. откл. : %0.2f)" %(statistics.mean(numlinks_to), statistics.stdev(numlinks_to)))


def analyse_redirects(G):
    redirects_to = [0 for i in range(G.get_number_of_pages())]
    for i in range(G.get_number_of_pages()):
        for x in G.get_links_from(i):
            if G.is_redirect(i) == 1:
                redirects_to[x] += 1
    _max = max(redirects_to)
    _min = min(redirects_to)
    mxn = sum(x == _max for x in redirects_to)
    mnn = sum(x == _min for x in redirects_to)
    print("Минимальное количество перенаправление на статью:", _min)
    print("Количество статей с минимальным количеством внешних перенаправлений:", mnn)
    print("Максимальное количество перенаправлений на статью:", _max)
    print("Количество статей с максимальным количеством внешних перенаправлений:", mxn)
    found_id = None
    for i in range(G.get_number_of_pages()):
        if redirects_to[i] == _max:
            found_id = i
            break
    print("Статья с наибольшим количеством внешних перенаправлений:",  G.get_title(found_id))
    print("Среднее количество внешних перенаправлений на статью: %0.2f  (ср. откл. : %0.2f)" %(statistics.mean(redirects_to), statistics.stdev(redirects_to)))

def dejkstra(G, start):
    shortest_path={vertex:int('50000') for vertex in G}
    shortest_path[start] = 0
    queue = [start]
    while queue:
        current=queue.pop(0)
        for neighbour in G[current]:
            offering_shortest_path = shortest_path[current]+(G[current][neighbour])
            if offering_shortest_path < shortest_path[neighbour]:
                shortest_path[neighbour]=offering_shortest_path
                queue.append(neighbour)
    return shortest_path

def hist(fname, data, bins, xlabel, ylabel, title, facecolor='green', alpha=0.5, transparent=True, **kwargs):
    plt.clf()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.hist(x=data, bins=bins, facecolor=facecolor, alpha=alpha, **kwargs)
    plt.savefig(fname, transparent=transparent)

if __name__ == '__main__':
    wg = WikiGraph()
    wg.load_from_file('wiki_small.txt')
    print("Количество статей с перенаправлением:", sum(wg._redirect))
    analyse_links_from_page(wg,)
    analyse_links_to_page(wg)
    analyse_redirects(wg)
    hist(fname='1.png', data=[wg.get_number_of_links_from(i) for i in range(1211)],bins=200,xlabel='Количество статей', ylabel="Количество ссылок", title="Распределение количества ссылок из статьи")
    #hist(fname='2.png', data=[wg. for i in range(1211)], bins=200, xlabel='Количество статей', ylabel="Количество ссылок", title="Распределение количества ссылок на статью")
   # hist(fname='3.png', data=[wg. for i in range(1211)], bins=50, xlabel='Количество статей', ylabel="Количество ссылок", title="Распределение количества редиректов на статью")
    hist(fname='4.png', data=[wg._sizes[i] for i in range(1211)], bins=50, xlabel='Количество статей', ylabel="Количество ссылок", title="Распределение размеров статей")
    hist(fname='5.png', data=[wg._sizes[i] for i in range(1211)], bins=50, xlabel='Количество статей', ylabel="Количество ссылок", title="Распределение размеров статей (log)", log=True)














