# coding: utf-8
from consts import ROUNDS, MAX_ROUNDS
import seaborn as sns
import matplotlib.pyplot as plt

from slf_performance import measure_performance

results_fpath = 'results/slf.txt'
histogram_fpath = 'results/slf_histogram.png'
histogram_tail_fpath = 'results/slf_histogram_tail.png'

def summarise_performance(results):
    print('Db size: %d words' % len(results))
    print('Mean number of moves required to solve the problem: %.3f' % (sum(results) / float(len(results))))
    solution_not_found = len(filter(lambda x: x > ROUNDS, results))
    print('Number of cases when no solution was found in %d moves: %d (%.4f%%)' % (ROUNDS, solution_not_found, float(solution_not_found) / len(results) * 100))
    sns.set()
    ax = sns.distplot(results, kde = False)
    ax.set(xlabel = 'no of rounds', ylabel = 'no of words')
    plt.savefig(histogram_fpath)
    plt.clf()
    tail_results = filter(lambda x: x > ROUNDS, results)
    ax = sns.distplot(tail_results, bins = 3, kde = False)
    ax.set(xlabel = 'no of rounds', ylabel = 'no of words')
    plt.xticks([7.35, 8, 8.7], range(7, 10))
    plt.savefig(histogram_tail_fpath)

measure_performance('db/pl_pl.txt', results_fpath, progress_steps=100)
results = map(int, open(results_fpath).readlines())
summarise_performance(results)
