from random import random
from yandex_parser import *
from relevance import *


class ClickModel(object):
    def __init__(self):
        self.params_initialized = False

    def simulate_clicks_on(self, ranking):
        probabilities = self.probabilities(ranking)
        clicks = [random() < p for p in probabilities]
        return clicks


class RandomClickModel(ClickModel):
    yandex_file_name = 'YandexRelPredChallenge.txt'
    params_file_name = 'RandomClickModelParams.txt'

    def __init__(self):
        ClickModel.__init__(self)
        self.rho = None

    def learn(self):
        queries = parse_yandex_file(self.yandex_file_name)

        results_count = 0
        click_count = 0

        for query in queries:
            results_count += len(query.ranking)
            click_count += len(query.clicks)

        self.rho = click_count / float(results_count)

        with open(self.params_file_name, 'w+') as f:
            f.write(str(self.rho))

        self.params_initialized = True

    def load(self):
        with open(self.params_file_name) as f:
            self.rho = float(f.readline())
        self.params_initialized = True

    def probabilities(self, ranking):
        if not self.params_initialized:
            raise AssertionError('Parameters have not been initialized.')
        return [self.rho] * len(ranking)


model = RandomClickModel()
