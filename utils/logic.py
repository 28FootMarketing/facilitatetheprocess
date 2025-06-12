def recommend_package(grade, motivation, outreach, gpa):
    if motivation <= 4:
        return "Role Player"
    elif grade in ["11th", "12th", "Post-grad"] and motivation >= 8 and outreach == "Yes":
        return "Captain"
    elif gpa < 2.5:
        return "Role Player"
    else:
        return "Starter"

def build_summary(name, sport, plan):
    return f"{name}, based on your inputs, the **{plan} Plan** is your best starting point. It aligns with your journey as a {sport} athlete."
