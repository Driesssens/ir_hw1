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
