# logic.py

def calculate_strength_score(stat1, stat2, stat3):
    """
    Safely calculates an average score from three athletic statistics.
    Converts inputs to float and handles invalid input gracefully.
    """
    try:
        s1 = float(stat1)
        s2 = float(stat2)
        s3 = float(stat3)
        raw_score = (s1 + s2 + s3) / 3
        return round(raw_score, 2)
    except (ValueError, TypeError):
        return 0.0

def recommend_package(score):
    """
    Recommends a recruiting package based on the calculated score.
    """
    if score >= 8.5:
        return "Captain (Elite)"
    elif score >= 6.5:
        return "Starter (Competitive)"
    elif score > 0:
        return "Role Player (Developmental)"
    else:
        return "Incomplete Data"
