def recommend_package(score):
    if score >= 80:
        return "🏆 Captain Package – You're leading the game!"
    elif score >= 60:
        return "🔋 Starter Package – Solid potential with room to grow."
    elif score >= 40:
        return "⚙️ Role Player Package – Get support and rise up."
    else:
        return "📈 Let's Build – Start with development basics and work up."

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
