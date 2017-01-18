from relevance import *
from ranking_pair import *
from ranking import *
from interleavers import *


def freestyle():
    perfect = Ranking([Relevance.HR] * 5)
    medium = Ranking([Relevance.R] * 5)
    worst = Ranking([Relevance.N] * 5)

    production = Ranking([Relevance.HR, Relevance.HR, Relevance.R, Relevance.R, Relevance.N])
    experiment = Ranking([Relevance.N, Relevance.N, Relevance.R, Relevance.R, Relevance.HR])

    test_pair = RankingPair(production, experiment)
    interleaving = interleave_team_draft(test_pair)
    print interleaving.ranking
    print interleaving.origins


def full_test():
    interleaver = BalancedInterleaver()
    interleaver.click_model = RandomClickModel()
    interleaver.click_model.load()
    production, experiment = [Ranking([Relevance.HR] * 5)] * 2
    test_pair = RankingPair(production, experiment)

    production_clicks, experiment_clicks = 0, 0
    production_wins, experiment_wins = 0, 0

    for i in range(1000):
        p, e = interleaver.compare(test_pair)
        production_clicks += p
        experiment_clicks += e

        if p > e:
            production_wins += 1
        elif p < e:
            experiment_wins += 1
        else:
            pass

    print "prod wins: " + str(production_wins)
    print "expi wins: " + str(experiment_wins)
    print "prod clicks: " + str(production_clicks)
    print "expi clicks: " + str(experiment_clicks)


def small_test():
    ranking1 = Ranking([Relevance.R, Relevance.R, Relevance.R, Relevance.R, Relevance.HR])
    ranking2 = Ranking([Relevance.R, Relevance.R, Relevance.R, Relevance.R, Relevance.HR])
    set1 = {ranking1, ranking2}
    set2 = {ranking2, ranking2}

    print set1 == set2

small_test()
