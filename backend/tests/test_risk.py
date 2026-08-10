from app.detection.risk import calculate_risk_score


def test_base_risk_score():
    score = calculate_risk_score(
        base_score=70,
        event_count=1,
    )

    assert score == 70


def test_multiple_events_increase_risk():
    score = calculate_risk_score(
        base_score=70,
        event_count=5,
    )

    assert score == 85


def test_risk_score_cannot_exceed_100():
    score = calculate_risk_score(
        base_score=100,
        event_count=10,
    )

    assert score == 100