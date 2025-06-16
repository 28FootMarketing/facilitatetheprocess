def build_summary(data):
    name = data.get("name", "Athlete")
    sport = data.get("sport", "Sport")
    grade = data.get("grade", "Grade")
    gpa = data.get("gpa", "N/A")
    motivation = data.get("motivation", "N/A")
    outreach = data.get("outreach", "N/A")
    stat1 = data.get("stat1", "Stat 1")
    stat2 = data.get("stat2", "Stat 2")
    stat3 = data.get("stat3", "Stat 3")
    video_link = data.get("video_link", "No Video Provided")

    summary = f"""
    📝 **Athlete Summary Report**

    - **Name**: {name}
    - **Sport**: {sport}
    - **Grade**: {grade}
    - **GPA**: {gpa}
    - **Motivation Level**: {motivation}
    - **Outreach Status**: {outreach}

    📊 **Performance Stats**
    - {stat1}
    - {stat2}
    - {stat3}

    🎥 **Highlight Video**: {video_link}
    """
    return summary.strip()
