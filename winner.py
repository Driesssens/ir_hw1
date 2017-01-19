class Winner:
    """Statically used class containing the winner enumeration. Used by interleaving methods
    to indicate which algorithm won an online evaluation."""
    P, E, T = [
        'P',  # The production algorithm won this evaluation.
        'E',  # The experimental algorithm won this evaluation.
        'T'  # This evaluation resulted in a tie.
    ]
