from random import random
from yandex_parser import *
from relevance import *
from collections import Counter
from ast import literal_eval


class ClickModel(object):
    """"Base class for click models."""

    yandex_file_name = 'YandexRelPredChallenge.txt'

    def __init__(self):
        self.params_initialized = False  # Safety check: simulation methods are blocked as long as parameters are not initialized.


class RandomClickModel(ClickModel):
    params_file_name = 'RandomClickModelParams.txt'  # File to store learned parameters

    def __init__(self):
        ClickModel.__init__(self)
        self.rho = None  # Model parameter representing the single click probability for every document

    def learn(self):
        """"Learns rho parameter from a Yandex log file. Stores it in `params_file_name` afterwards."""
        queries = parse_yandex_file(self.yandex_file_name)

        results_count = 0  # Total amount of results returned by all queries in log file
        click_count = 0  # Total amount of clicks in the whole log file

        for query in queries:
            results_count += len(query.ranking)
            click_count += len(query.clicks)

        self.rho = click_count / float(results_count)

        with open(self.params_file_name, 'w+') as f:
            f.write(str(self.rho))  # Storing learned parameter in file

        self.params_initialized = True  # We can now run simulations

    def load(self):
        """"Loads rho parameter from `params_file_name` if it was previously learned and stored there."""
        with open(self.params_file_name) as f:
            self.rho = float(f.readline())
        self.params_initialized = True  # We can now run simulations

    def probabilities(self, ranking):
        """"Given `ranking`, returns click probabilities for each document in the list."""
        if not self.params_initialized:
            raise AssertionError('Parameters have not been initialized.')
        return [self.rho] * len(ranking)  # It is simply the same for each document

    def simulate_clicks_on(self, ranking):
        """"Given `ranking`, stochastically decides for each document whether it was clicked."""
        probabilities = self.probabilities(ranking)  # First, get probabilities
        clicks = [random() < p for p in probabilities]  # Then, sample yes / no from those probabilities
        return clicks


class SimplifiedDependentClickModel(ClickModel):
    params_file_name = 'SimplifiedDependentClickModelParams.txt'  # File to store learned parameters

    def __init__(self):
        """"Initializes two parameter dictionaries. First, `satisfaction_at`, which contains the satisfaction parameter (inverse
        continuation parameter) for each rank. Second, `attractiveness_of`, which contains the attractiveness parameter per
        relevance grade. We have chosen to assign 0 to N, 0.5 to R and 1 to HR. """
        ClickModel.__init__(self)
        self.satisfaction_at = {}
        max_relevance_quantity = float(max([quantify(grade) for grade in Relevance.all]))
        self.attractiveness_of = {grade: quantify(grade) / max_relevance_quantity for grade in Relevance.all}

    def learn(self):
        """Leans the satisfaction parameters (inverse continuation parameters) at each rank from the Yandex log file.
         Stores it in `params_file_name` afterwards. In the terminology below, with 'a satisfaction', we mean a click
         that was the final click of the query."""
        queries = parse_yandex_file(self.yandex_file_name)

        all_click_lists = [query.clicks for query in queries if query.clicks]
        all_clicks = [click for click_list in all_click_lists for click in click_list]
        all_satisfactions = [max(click_list) for click_list in all_click_lists]

        click_count_at_rank = Counter(all_clicks)  # Counts, per rank, over the whole log file, the number of clicks on that rank
        satisfaction_count_at_rank = Counter(all_satisfactions)  # Counts, per rank, over the whole log file, the number of satisfactions on that rank

        # This line computes the satisfaction (inverse continuation) parameters for each rank that has ever been the last clicked rank of a query
        self.satisfaction_at = {rank: satisfaction_count / float(click_count_at_rank[rank]) for rank, satisfaction_count in satisfaction_count_at_rank.items()}

        with open(self.params_file_name, 'w+') as f:
            f.write(str(self.satisfaction_at))  # Storing learned parameter in file

        self.params_initialized = True  # We can now run simulations

    def load(self):
        """"Loads satisfaction parameters (inverse continuation parameters) from `params_file_name` if they were previously learned and stored there."""
        with open(self.params_file_name) as f:
            self.satisfaction_at = literal_eval(f.readline())
        self.params_initialized = True  # We can now run simulations

    def probabilities(self, ranking):
        """"Given `ranking`, returns click and satisfaction probabilities for each document in the list."""
        if not self.params_initialized:
            raise AssertionError('Parameters have not been initialized.')

        click_probabilities = [self.attractiveness_of[grade] for grade in ranking]
        satisfaction_probabilities = [self.satisfaction_at[index + 1] for index in range(len(ranking))]

        return click_probabilities, satisfaction_probabilities

    def simulate_clicks_on(self, ranking):
        """"Given `ranking`, stochastically decides for each document whether it was clicked. Iterates through the
        ranking list according to the model: at each document, stochastically decided whether it was clicked, and if
        it was, stochastically decides whether the user was satisfied. If the user was satisfied, stop. """
        click_probabilities, satisfaction_probabilities = self.probabilities(ranking)
        clicks = [False] * len(ranking)

        for i in range(len(ranking)):
            if random() < click_probabilities[i]:  # Was the document clicked?
                clicks[i] = True
                if random() < satisfaction_probabilities[i]:  # Was the user satisfied?
                    return clicks  # Immediately stop if satisfied

        return clicks
