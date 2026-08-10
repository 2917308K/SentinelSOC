def calculate_risk_score(
    *,
    base_score: int,
    event_count: int,
) -> int:
    score = base_score

    if event_count >= 5:
        score += 15
    elif event_count >= 3:
        score += 10

    return min(score, 100)