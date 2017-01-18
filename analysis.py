from winner import Winner


def compare(pairs, interleaver, click_model):
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

    return (experiment_wins + 0.5 * ties) / float(len(pairs))
