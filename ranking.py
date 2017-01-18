import numpy as np
from relevance import *


def discounted_gain_at(k, ranking):
    """Returns discounted gain resulting from the document at rank `k` in `ranking`. """
    index = k - 1  # convert 1-based rank to 0-based index
    gain = np.power(2, quantify(ranking[index])) - 1  # non-linear gain resulting from document
    discount = np.log2(1 + k)  # discount factor
    return gain / float(discount)


def dcg_at(k, ranking):
    """Returns DCG at rank `k` for `ranking`. Computes `discounted_gain_at`
    at each rank from 1 to and including `k`, and sums these values. """
    return sum([discounted_gain_at(i + 1, ranking) for i in range(k)])


class Ranking:
    """Ranking objects embody an ordering of Relevance labels and represent either
    the result of a query to the E or P algorithm, or an interleaving of those."""

    total_relevant = 20  # Total amount of relevant (R / HR) documents in collection
    persistence = 0.8  # The RBP persistence parameter

    def __init__(self, ranking):
        """Creates a new Ranking object according to ordered Relevance labels `ranking`."""
        self.ranking = ranking  # Internal ordering of Relevance labels, representing search results
        self.n = len(ranking)
        self.perfect = [Relevance.HR] * self.n  # Optimum ranking of the same length, for DCG normalization

    def relevant_at(self, k):
        """Return amount of relevant (R / HR) documents from ranks 1 to and including `k`."""
        return sum(relevant(grade) for grade in self.ranking[:k])

    def precision_at(self, k):
        """Return precision at rank `k`: amount of relevant (R / HR) documents from ranks 1 to
        and including `k`, divided by total amount of documents in that range (which is `k`)."""
        return self.relevant_at(k) / float(k)

    def recall_at(self, k):
        """Return recall at rank `k`: amount of relevant (R / HR) documents from ranks 1 to
        and including `k`, divided by total amount of relevant (R / HR) documents in collection
        (given by `total_relevant`). """
        return self.relevant_at(k) / float(self.total_relevant)

    def average_precision(self):
        """Return average precision of this Ranking: average of `precision_at` evaluated at
        each rank where this Ranking has a relevant (H / HR) document."""
        precisions = [self.precision_at(i + 1) for i in range(self.n) if relevant(self.ranking[i])]
        return sum(precisions) / len(precisions) if len(precisions) > 0 else 0

    def dcg_at(self, k):
        """Returns DCG at rank `k` of this Ranking. Wrapper static dcg_at function."""
        return dcg_at(k, self.ranking)

    def ndcg_at(self, k):
        """Returns normalized DCG at rank `k` of this Ranking. Normalizes by computing
        DCG at rank `k` of the best possible ranking (stored in `perfect`) and dividing
        the regular (unnormalized) DCG by this value."""
        return dcg_at(k, self.ranking) / dcg_at(k, self.perfect)

    def observation_probability_at(self, k):
        return (1 - self.persistence) * np.power(self.persistence)

    def rank_biased_precision(self):
        return sum([self.ranking[k] * self.observation_probability_at(k) for k in range(self.n)])

    def __eq__(self, other):
        """Ranking objects are equal when they contain the same relevance label ordering. """
        return self.ranking == other.ranking if isinstance(other, self.__class__) else NotImplemented

    def __ne__(self, other):
        return not self.__eq__(other) if isinstance(other, self.__class__) else NotImplemented

    def __hash__(self):
        return hash(tuple(sorted(self.ranking)))

    def __str__(self):
        return "Ranking" + str(self.ranking)
