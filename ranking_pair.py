class RankingPair:
    def __init__(self, p, e):
        self.p = p
        self.e = e

    def delta_precision_at(self, k):
        return self.e.precision_at(k) - self.p.precision_at(k)

    def delta_recall_at(self, k):
        return self.e.recall_at(k) - self.p.recall_at(k)

    def delta_average_precision(self):
        return self.e.average_precision() - self.p.average_precision()

    def delta_cdg_at(self, k):
        return self.e.cdg_at(k) - self.p.cdg_at(k)

    def delta_ncdg_at(self, k):
        return self.e.ncdg_at(k) - self.p.ncdg_at(k)

    def delta_rbp(self):
        return self.e.rank_biased_precision() - self.p.rank_biased_precision()
