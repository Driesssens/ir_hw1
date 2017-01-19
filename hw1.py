from relevance import *
from ranking_pair import *
from ranking import *
from interleavers import *
from analysis import *
from click_models import *


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


def test_deltas():
    ranking1 = Ranking([Relevance.HR, Relevance.N, Relevance.N, Relevance.N, Relevance.N])
    ranking2 = Ranking([Relevance.N, Relevance.N, Relevance.N, Relevance.N, Relevance.HR])
    pair = RankingPair(ranking1, ranking2)
    print "average precision:       " + str(pair.delta_average_precision())
    print "cdg at 1:                " + str(pair.delta_dcg_at(1))
    print "cdg at 3:                " + str(pair.delta_dcg_at(3))
    print "cdg at 5:                " + str(pair.delta_dcg_at(5))
    print "ncdg at 1:               " + str(pair.delta_ndcg_at(1))
    print "ncdg at 3:               " + str(pair.delta_ndcg_at(3))
    print "ncdg at 5:               " + str(pair.delta_ndcg_at(5))
    print "precision at 1:          " + str(pair.delta_precision_at(1))
    print "precision at 3:          " + str(pair.delta_precision_at(3))
    print "precision at 5:          " + str(pair.delta_precision_at(5))
    print "recall at 1:             " + str(pair.delta_recall_at(1))
    print "recall at 3:             " + str(pair.delta_recall_at(3))
    print "recall at 5:             " + str(pair.delta_recall_at(5))


def test_generator():
    all_pairs = generate_all_pairs()
    print all_pairs[0]
    print all_pairs[-1]
    print all_pairs[9235]
    print len(all_pairs)


def test_winner_generator():
    all = generate_all_pairs()
    winners = generate_all_winners(RankingPair.delta_recall_at, 5)
    amount_of_winners = sum(winner.delta_recall_at(1) > 0 for winner in winners)
    amount_of_losers = sum(winner.delta_recall_at(1) < 0 for winner in winners)
    amount_of_ties = len(all) - amount_of_losers - amount_of_winners

    print "#all: " + str(len(all))
    print "#winners: " + str(len(winners))
    print "winners %: " + str(len(winners) / float(len(all)) * 100)
    print "winners check: " + str(amount_of_winners)
    print "losers check: " + str(amount_of_losers)
    print "ties check: " + str(amount_of_ties)


def test_probabilistic_interleaving():
    p = Ranking([Relevance.HR, Relevance.HR, Relevance.R, Relevance.R, Relevance.R])
    e = Ranking([Relevance.N, Relevance.N, Relevance.N, Relevance.N, Relevance.N])

    test_pair = RankingPair(p, e)

    interleaver = ProbabilisticInterleaver()
    ranking, origins = interleaver.interleave(test_pair)
    print ranking
    print origins


def test_analysis(random=True):
    pairs1 = generate_all_winners(RankingPair.delta_average_precision)
    inter1 = BalancedInterleaver()
    model1 = RandomClickModel() if random else SimplifiedDependentClickModel()
    combo1 = compare(pairs1, inter1, model1)
    print "Average Precision + Balanced Interleaver + Random Click Model: " + str(combo1)

    pairs2 = generate_all_winners(RankingPair.delta_average_precision)
    inter2 = ProbabilisticInterleaver()
    model2 = RandomClickModel() if random else SimplifiedDependentClickModel()
    combo2 = compare(pairs2, inter2, model2)
    print "Average Precision + Probabil Interleaver + Random Click Model: " + str(combo2)

    pairs3 = generate_all_winners(RankingPair.delta_ndcg_at, 5)
    inter3 = BalancedInterleaver()
    model3 = RandomClickModel() if random else SimplifiedDependentClickModel()
    combo3 = compare(pairs3, inter3, model3)
    print "Normalized DCG @5 + Balanced Interleaver + Random Click Model: " + str(combo3)

    pairs4 = generate_all_winners(RankingPair.delta_ndcg_at, 5)
    inter4 = BalancedInterleaver()
    model4 = RandomClickModel() if random else SimplifiedDependentClickModel()
    combo4 = compare(pairs4, inter4, model4)
    print "Normalized DCG @5 + Balanced Interleaver + Random Click Model: " + str(combo4)

    pairs5 = generate_all_winners(RankingPair.delta_dcg_at, 5)
    inter5 = BalancedInterleaver()
    model5 = RandomClickModel() if random else SimplifiedDependentClickModel()
    combo5 = compare(pairs5, inter5, model5)
    print "Discounted CG @ 5 + Balanced Interleaver + Random Click Model: " + str(combo5)

    pairs6 = generate_all_winners(RankingPair.delta_dcg_at, 5)
    inter6 = BalancedInterleaver()
    model6 = RandomClickModel() if random else SimplifiedDependentClickModel()
    combo6 = compare(pairs6, inter6, model6)
    print "Discounted CG @ 5 + Balanced Interleaver + Random Click Model: " + str(combo6)


def test_sdcm():
    model = SimplifiedDependentClickModel()
    print model.attractiveness_of
    model.learn()
    print model.satisfaction_at
    model2 = SimplifiedDependentClickModel()
    model2.load()
    print model2.satisfaction_at


def test_rcm():
    model = RandomClickModel()
    model.learn()
    print model.rho
    model2 = RandomClickModel()
    model2.load()
    print model2.rho


def test_yandex_parser():
    queries = parse_yandex_file('YandexRelPredChallenge.txt')
    for query in queries:
        print query


test_analysis(random=False)
