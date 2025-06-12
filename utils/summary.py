def build_summary(name, sport, plan, score):
    return (
        f"{name}, based on your inputs and {sport} stats, the **{plan} Plan** is your best fit.\n\n"
        f"Your Match Strength Score is **{score}**, which tells us how ready you are for college-level attention.\n\n"
        f"Let’s start moving your recruiting process forward today."
    )
