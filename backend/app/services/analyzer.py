def analyze_match(team1, team2):

    elo1 = team1["elo"]
    elo2 = team2["elo"]

    diff = elo1 - elo2

    if diff > 80:
        prediction = "1"
        confidence = "Yüksek"
    elif diff > 30:
        prediction = "1"
        confidence = "Orta"
    elif diff < -80:
        prediction = "2"
        confidence = "Yüksek"
    elif diff < -30:
        prediction = "2"
        confidence = "Orta"
    else:
        prediction = "X"
        confidence = "Düşük"

    return {
        "prediction": prediction,
        "confidence": confidence,
        "elo_difference": diff
    }
