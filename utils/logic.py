def recommend_package(grade, motivation, outreach, gpa):
    if motivation <= 4:
        return "Role Player"
    elif grade in ["11th", "12th", "Post-grad"] and motivation >= 8 and outreach == "Yes":
        return "Captain"
    elif gpa < 2.5:
        return "Role Player"
    else:
        return "Starter"

def calculate_strength_score(stat1, stat2, stat3):
    raw_score = (stat1 + stat2 + stat3) / 3
    if raw_score >= 20:
        return "Elite"
    elif raw_score >= 10:
        return "Competitive"
    else:
        return "Developing"
