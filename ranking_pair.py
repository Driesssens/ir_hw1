from itertools import product
from ranking import *
from types import MethodType


def generate_rankings(length, grades):
    """"Generates all combinatorial possibilities of ranking lists existing of
    the relevance grade labels in `grades`, being of length `length."""
    rankings = list(product(grades, repeat=length))  # all combinatorial possibilities
    return [Ranking(list(ranking)) for ranking in rankings]  # turn into Ranking objects


def generate_pairs(rankings):
    """Given a set of `rankings`, generates all possible pairs. """
    pairs = list(product(rankings, repeat=2))
    return [RankingPair(p, e) for p, e in pairs]


def generate_all_pairs():
    """"Generates all possible pairs of rankings of length 5 containing
    relevance labels N, R and HR. """
    return generate_pairs(generate_rankings(5, Relevance.all))


def generate_all_winners(delta_method, parameter=None):
    """"Generates all pairs, but throws away those pairs for which the experimental algorithm
    is not the winner according to offline evaluation metric `delta_method` (possibly parameterized
    with `parameter`, for instance in the case of 'recall at 5'. """
    all_pairs = generate_all_pairs()
    if parameter is None:
        winners = [pair for pair in all_pairs if MethodType(delta_method, pair)() > 0]
    else:
        winners = [pair for pair in all_pairs if MethodType(delta_method, pair)(parameter) > 0]
    return winners


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
