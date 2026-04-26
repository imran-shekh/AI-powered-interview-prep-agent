def calculate_score(evaluations):
    scores = {}
    for skill, evals in evaluations.items():
        avg = sum(evals) / len(evals)
        scores[skill] = round(avg, 2)
    return scores