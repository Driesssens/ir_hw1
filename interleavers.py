from random import getrandbits

from origin import Origin
from ranking import *
from winner import Winner


class Interleaver:
    def __init__(self):
        self.click_model = None

    def run_simulation(self, pair):
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

    def evaluate(self, pair):
        production_clicks, experiment_clicks = self.run_simulation(pair)
        if experiment_clicks == production_clicks:
            return Winner.T
        else:
            return Winner.P if production_clicks > experiment_clicks else Winner.E


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


class TeamDraftInterleaver(Interleaver):
    def __init__(self):
        Interleaver.__init__(self)

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


class ProbabilisticInterleaver(Interleaver):
    tau = 3

    def __init__(self):
        Interleaver.__init__(self)

    def interleave(self, pair):
        length = min(len(pair.p.ranking), len(pair.e.ranking))

        origins, ranking = [], []

        remaining_p = pair.p.ranking[:]
        remaining_e = pair.e.ranking[:]

        for i in range(length):
            if getrandbits(1):
                ranking.append(self.sample_element_from(remaining_p))
                ranking.append(self.sample_element_from(remaining_e))
                origins.extend([Origin.P, Origin.E])
            else:
                ranking.append(self.sample_element_from(remaining_e))
                ranking.append(self.sample_element_from(remaining_p))
                origins.extend([Origin.E, Origin.P])

        return ranking, origins

    def sample_element_from(self, remaining_list):
        remaining_amount = len(remaining_list)
        probabilities = self.softmax_probabilities(remaining_amount)
        sampled_index = np.random.choice(range(remaining_amount), p=probabilities)
        popped = remaining_list.pop(sampled_index)
        return popped

    def softmax_probabilities(self, length):
        unnormalized = [1 / float(np.power(rank, self.tau)) for rank in range(1, length + 1)]
        normalization_factor = float(sum(unnormalized))
        normalized = [x / normalization_factor for x in unnormalized]
        return normalized
