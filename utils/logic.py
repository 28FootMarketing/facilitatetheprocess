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
    try:
        # Convert inputs to float, default to 0 if conversion fails
        s1 = float(stat1) if stat1 else 0
        s2 = float(stat2) if stat2 else 0
        s3 = float(stat3) if stat3 else 0

        raw_score = (s1 + s2 + s3) / 3
        return round(raw_score, 2)
    except Exception as e:
        print(f"⚠️ Error calculating strength score: {e}")
        return 0
