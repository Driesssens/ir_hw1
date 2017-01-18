from random import getrandbits

from click_models import *
from origin import Origin
from ranking_pair import *
from ranking import *


class Interleaver:
    def __init__(self):
        self.click_model = None

    def compare(self, pair):
        ranking, origins = self.interleave(pair)
        clicks = self.click_model.simulate_clicks_on(ranking)
        production_clicks = 0
        experiment_clicks = 0

        for i in range(len(ranking)):
            if clicks[i]:
                if origins[i] is Origin.P:
                    production_clicks += 1
                else:
                    experiment_clicks += 1

        return production_clicks, experiment_clicks


class BalancedInterleaver(Interleaver):
    def __init__(self):
        Interleaver.__init__(self)

    def interleave(self, pair):
        length = min(len(pair.p.ranking), len(pair.e.ranking))
        production_first = getrandbits(1)

        origins = ([Origin.P, Origin.E] if production_first else [Origin.E, Origin.P]) * length
        ranking = [None] * length * 2

        ranking[int(not production_first)::2] = pair.p.ranking
        ranking[int(production_first)::2] = pair.e.ranking

        return ranking, origins


class TeamDraftInterleaver:
    def __init__(self):
        self.click_model = None

    def interleave(self, pair):
        length = min(len(pair.p.ranking), len(pair.e.ranking))

        origins, ranking = [], []

        for i in range(length):
            if getrandbits(1):
                origins.extend([Origin.P, Origin.E])
                ranking.extend([pair.p.ranking[i], pair.e.ranking[i]])
            else:
                origins.extend([Origin.E, Origin.P])
                ranking.extend([pair.e.ranking[i], pair.p.ranking[i]])

        return ranking, origins
