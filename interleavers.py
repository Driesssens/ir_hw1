from random import getrandbits

from origin import Origin
from ranking import *
from winner import Winner


class Interleaver:
    """Base class for interleavers. Stores the click model that it uses for simulations in `click_model`."""

    def __init__(self):
        self.click_model = None  # The click model to use in simulations.

    def run_simulation(self, pair):
        """"Runs one simulation of an online evaluation. Returns the number of clicks that the E and P algorithms have received."""
        ranking, origins = self.interleave(pair)
        clicks = self.click_model.simulate_clicks_on(ranking)
        production_clicks = 0
        experiment_clicks = 0

        for i in range(len(ranking)):
            if clicks[i]:
                if origins[i] is Origin.P:  # Did the production algorithm provide this document to the interleaved list?
                    production_clicks += 1
                else:  # Or was it the experimental algorithm?
                    experiment_clicks += 1

        return production_clicks, experiment_clicks

    def evaluate(self, pair):
        """"Runs one simulation of an online evaluation. Returns which algorithm won, or that there was a tie."""
        production_clicks, experiment_clicks = self.run_simulation(pair)  # Simulate clicks
        if experiment_clicks == production_clicks:
            return Winner.T  # This means there was a tie.
        else:
            return Winner.P if production_clicks > experiment_clicks else Winner.E


class BalancedInterleaver(Interleaver):
    """Implements the balanced interleaving method."""

    def __init__(self):
        Interleaver.__init__(self)

    def interleave(self, pair):
        """Performs the balanced interleaving method."""
        length = min(len(pair.p.ranking), len(pair.e.ranking))
        production_first = getrandbits(1)  # Flip a coin. '1' means the production algorithm may provide a document first.

        #  Stores which algorithm provided the document at each position of the resulting interleaved list
        origins = ([Origin.P, Origin.E] if production_first else [Origin.E, Origin.P]) * length

        #  The next three lines do a Python slicing trick to interleave the lists alternating between P and E.
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
    """Implements the probabilistic interleaving method."""

    tau = 3  # The tau model parameter. Chosen to be 3 as recommended in the paper.

    def __init__(self):
        Interleaver.__init__(self)

    def interleave(self, pair):
        """Performs the probabilistic interleaving method."""
        length = min(len(pair.p.ranking), len(pair.e.ranking))

        # `origins` stores which algorithm provided the document at each position of the resulting interleaved list
        origins, ranking = [], []

        # Copy the rankings to keep track of the documents we still have to interleave
        remaining_p = pair.p.ranking[:]
        remaining_e = pair.e.ranking[:]

        for i in range(length):
            if getrandbits(1):  # flip a coin to see which algorithm goes first
                ranking.append(self.sample_element_from(remaining_p))  # P goes first; stochastically pick a remaining document
                ranking.append(self.sample_element_from(remaining_e))  # Then do the same for E
                origins.extend([Origin.P, Origin.E])  # Keep track of the fact that P went first in this round
            else:
                ranking.append(self.sample_element_from(remaining_e))
                ranking.append(self.sample_element_from(remaining_p))
                origins.extend([Origin.E, Origin.P])

        return ranking, origins

    def sample_element_from(self, remaining_list):
        """Stochastically picks (and removes) a document from the `remaining_list`, according to softmax probabilities."""
        remaining_amount = len(remaining_list)
        probabilities = self.softmax_probabilities(remaining_amount)
        sampled_index = np.random.choice(range(remaining_amount), p=probabilities)
        popped = remaining_list.pop(sampled_index)
        return popped

    def softmax_probabilities(self, length):
        """Computes the softmax probability distribution for a document list of `length`."""
        unnormalized = [1 / float(np.power(rank, self.tau)) for rank in range(1, length + 1)]
        normalization_factor = float(sum(unnormalized))
        normalized = [x / normalization_factor for x in unnormalized]  # normalize all probabilities to make it a distribution
        return normalized
