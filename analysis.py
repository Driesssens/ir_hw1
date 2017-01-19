from winner import Winner
from relevance import *
from ranking_pair import *
from ranking import *
from interleavers import *
from analysis import *
from click_models import *


def compare(pairs, interleaver, click_model):
    """"The final evaluation method. Given a set of query ranking pairs for the E and P algorithms,
     and given an interleaving method, and given a click model, simulations an online evaluation.
     For each query ranking pair, one interleaving is presented to 'the user', whom the click
     model is modelling. Based on the clicks, the algorithms receive credit. Then, the
     'delta_AB' metric from 'Large-Scale Validation and Analysis of Interleaved Search Evaluation'
     is used to finally measure the preference an online evaluation expresses for one of the algorithms.

     We adjusted the metric in two ways:
     - we don't disregard evaluations with zero clicks
     - we make it range from -100% to 100%, instead of -50% to 50%
     """

    # Loads the click model parameters (given they have been learned
    # before). Change to `learn` to deduce from the Yandex log file.
    click_model.load()

    interleaver.click_model = click_model
    production_wins, experiment_wins, ties = 0, 0, 0

    for pair in pairs:
        winner = interleaver.evaluate(pair)
        if winner is Winner.P:
            production_wins += 1
        elif winner is Winner.E:
            experiment_wins += 1
        else:
            ties += 1

    # Compute and return the adjusted delta_AB metric
    return ((experiment_wins + 0.5 * ties) / float(len(pairs)) - 0.5) * 200


def analyse():
    """"Performs the analysis for each of the 12 model combinations."""
    print "The following models express a preference in % for the experimental algorithm on the following data sets:"
    print

    print "     On the data set where the experimental algorithm wins on all pairs according to the average precision:"
    data_set_1 = generate_all_winners(RankingPair.delta_average_precision)

    print "         Balanced Interleaving with RCM =       {0}%".format(compare(data_set_1, BalancedInterleaver(), RandomClickModel()))
    print "         Probabilistic Interleaving with RCM =  {0}%".format(compare(data_set_1, ProbabilisticInterleaver(), RandomClickModel()))
    print "         Balanced Interleaving with SDCM =      {0}%".format(compare(data_set_1, BalancedInterleaver(), SimplifiedDependentClickModel()))
    print "         Probabilistic Interleaving with SDCM = {0}%".format(compare(data_set_1, ProbabilisticInterleaver(), SimplifiedDependentClickModel()))
    print "     This data set contained {0} pairs.".format(len(data_set_1))
    print

    print "     On the data set where the experimental algorithm wins on all pairs according to DCG at rank 5:"
    data_set_2 = generate_all_winners(RankingPair.delta_dcg_at, 5)

    print "         Balanced Interleaving with RCM =       {0}%".format(compare(data_set_2, BalancedInterleaver(), RandomClickModel()))
    print "         Probabilistic Interleaving with RCM =  {0}%".format(compare(data_set_2, ProbabilisticInterleaver(), RandomClickModel()))
    print "         Balanced Interleaving with SDCM =      {0}%".format(compare(data_set_2, BalancedInterleaver(), SimplifiedDependentClickModel()))
    print "         Probabilistic Interleaving with SDCM = {0}%".format(compare(data_set_2, ProbabilisticInterleaver(), SimplifiedDependentClickModel()))
    print "     This data set contained {0} pairs.".format(len(data_set_2))
    print

    print "     On the data set where the experimental algorithm wins on all pairs according to normalized DCG at rank 5:"
    data_set_3 = generate_all_winners(RankingPair.delta_ndcg_at, 5)

    print "         Balanced Interleaving with RCM =       {0}%".format(compare(data_set_3, BalancedInterleaver(), RandomClickModel()))
    print "         Probabilistic Interleaving with RCM =  {0}%".format(compare(data_set_3, ProbabilisticInterleaver(), RandomClickModel()))
    print "         Balanced Interleaving with SDCM =      {0}%".format(compare(data_set_3, BalancedInterleaver(), SimplifiedDependentClickModel()))
    print "         Probabilistic Interleaving with SDCM = {0}%".format(compare(data_set_3, ProbabilisticInterleaver(), SimplifiedDependentClickModel()))
    print "     This data set contained {0} pairs.".format(len(data_set_3))
