class Origin:
    """Statically used class containing the origin enumeration. Used by interleavers
    to keep track of which algorithm provided each document in the interleaved list."""
    P, E = [
        'P ',  # indicates a document originated from the production algorithm
        'E '  # indicates a document originated from the experimental algorithm
    ]
