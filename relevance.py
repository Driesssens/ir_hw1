class Relevance:
    """Statically used class containing the relevance grade enumeration."""
    N, R, HR = [
        "N ",  # not relevant
        "R ",  # relevant
        "HR"  # highly relevant
    ]

    all = [N, R, HR]


def quantify(grade):
    """Assigns a numerical value to a relevance grade."""
    if grade is Relevance.N:
        return 0
    if grade is Relevance.R:
        return 1
    if grade is Relevance.HR:
        return 2


def relevant(grade):
    """Tells if a relevance grade counts as relevant (R / HR) or not (N)."""
    return grade is Relevance.R or grade is Relevance.HR
