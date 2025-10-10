"""
LLM-as-judge protocols with bias mitigation.

Includes randomization, masking, and cross-family validation.
"""

import random


def create_judge_prompt(
    criterion: str,
    output: str,
    reference: str | None = None,
    randomize_order: bool = True,
    mask_metadata: bool = True,
) -> str:
    """
    Create judge prompt with bias controls.

    Args:
        criterion: Evaluation criterion (e.g., "correctness", "helpfulness")
        output: Output to evaluate
        reference: Optional reference output
        randomize_order: Randomize order if reference provided
        mask_metadata: Remove provider/model metadata

    Returns:
        Judge prompt string
    """
    if mask_metadata:
        # Remove common metadata markers
        output = output.replace("GPT-4", "[MODEL]").replace("Claude", "[MODEL]")
        if reference:
            reference = reference.replace("GPT-4", "[MODEL]").replace("Claude", "[MODEL]")

    if reference and randomize_order:
        if random.random() < 0.5:
            output, reference = reference, output

    prompt = f"""Evaluate the following output based on: {criterion}

Output: {output}"""

    if reference:
        prompt += f"\n\nReference: {reference}"

    prompt += "\n\nProvide rating 1-10 and explanation.\nVERDICT: [rating]\nEXPLANATION: [your explanation]"

    return prompt


def cohens_kappa(rater1_labels: list[int], rater2_labels: list[int]) -> float:
    """
    Cohen's kappa for inter-rater reliability.

    Args:
        rater1_labels: Labels from rater 1
        rater2_labels: Labels from rater 2

    Returns:
        Kappa value
    """
    if len(rater1_labels) != len(rater2_labels):
        raise ValueError("Label lists must have same length")

    n = len(rater1_labels)
    observed_agreement = sum(1 for a, b in zip(rater1_labels, rater2_labels, strict=False) if a == b) / n

    # Expected agreement by chance
    unique_labels = set(rater1_labels + rater2_labels)
    expected = 0.0
    for label in unique_labels:
        p1 = rater1_labels.count(label) / n
        p2 = rater2_labels.count(label) / n
        expected += p1 * p2

    kappa = (observed_agreement - expected) / (1 - expected) if expected < 1 else 1.0

    return kappa


def fleiss_kappa(ratings_matrix: list[list[int]]) -> float:
    """
    Fleiss' kappa for multiple raters.

    Args:
        ratings_matrix: n_items × n_raters matrix of ratings

    Returns:
        Fleiss' kappa value
    """
    n_items = len(ratings_matrix)
    n_raters = len(ratings_matrix[0])

    # Get unique categories
    all_ratings = [r for row in ratings_matrix for r in row]
    categories = sorted(set(all_ratings))

    # Agreement per item
    P_i = []
    for item_ratings in ratings_matrix:
        item_agreement = 0.0
        for cat in categories:
            n_ij = item_ratings.count(cat)
            item_agreement += n_ij * (n_ij - 1)
        P_i.append(item_agreement / (n_raters * (n_raters - 1)))

    P_bar = sum(P_i) / n_items

    # Expected agreement
    p_j = []
    for cat in categories:
        count = sum(row.count(cat) for row in ratings_matrix)
        p_j.append(count / (n_items * n_raters))

    P_e = sum(p * p for p in p_j)

    kappa = (P_bar - P_e) / (1 - P_e) if P_e < 1 else 1.0

    return kappa
