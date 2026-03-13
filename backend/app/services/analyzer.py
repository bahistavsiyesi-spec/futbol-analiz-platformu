def analyze_match(team1, team2):
    elo1 = team1.get("elo", 0)
    elo2 = team2.get("elo", 0)

    team1_name = team1.get("team", "Team1")
    team2_name = team2.get("team", "Team2")

    diff = elo1 - elo2

    if diff >= 80:
        prediction = "1"
        confidence = "Yüksek"
    elif diff >= 30:
        prediction = "1"
        confidence = "Orta"
    elif diff <= -80:
        prediction = "2"
        confidence = "Yüksek"
    elif diff <= -30:
        prediction = "2"
        confidence = "Orta"
    else:
        prediction = "X"
        confidence = "Düşük"

    return {
        "match": f"{team1_name} vs {team2_name}",
        "team1_elo": elo1,
        "team2_elo": elo2,
        "elo_difference": diff,
        "prediction": prediction,
        "confidence": confidence
    }
