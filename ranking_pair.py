from itertools import product
from ranking import *


def generate_rankings(length, grades):
    rankings = list(product(grades, repeat=length))
    return [Ranking(ranking) for ranking in rankings]


def generate_pairs(rankings):
    pairs = list(product(rankings, repeat=2))
    return [RankingPair(p, e) for p, e in pairs]


def generate_all_pairs():
    return generate_pairs(generate_rankings(5, Relevance.all))


class RankingPair:
    """RankingPair objects embody a pair of Ranking objects, representing
    the results of the P and E algorithms to a query.

    Contains all the delta measure methods, which are not further documented
    since they are self-explanatory."""

    def __init__(self, p, e):
        self.p = p  # The results of the P algorithm
        self.e = e  # The results of the E algorithm

    def delta_precision_at(self, k):
        return self.e.precision_at(k) - self.p.precision_at(k)

    def delta_recall_at(self, k):
        return self.e.recall_at(k) - self.p.recall_at(k)

    def delta_average_precision(self):
        return self.e.average_precision() - self.p.average_precision()

    def delta_dcg_at(self, k):
        return self.e.dcg_at(k) - self.p.dcg_at(k)

    def delta_ndcg_at(self, k):
        return self.e.ndcg_at(k) - self.p.ndcg_at(k)

    def delta_rbp(self):
        return self.e.rank_biased_precision() - self.p.rank_biased_precision()

    def __str__(self):
        return "RankingPair[P=" + str(self.p.ranking) + ", E=" + str(self.e.ranking) + "]"
