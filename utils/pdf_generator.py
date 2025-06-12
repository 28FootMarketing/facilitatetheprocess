from fpdf import FPDF
import io

def generate_pdf_from_chat(name, sport, video_link, chat_transcript):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, f"{name or 'Athlete'}'s Recruiting Plan", ln=True, align='C')

    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    if sport:
        pdf.cell(200, 10, f"Sport: {sport}", ln=True)
    if video_link:
        pdf.cell(200, 10, f"Video: {video_link}", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Conversation Summary & Recommendations:", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, chat_transcript)

    buffer = io.BytesIO()
    pdf.output(buffer)
    return buffer.getvalue()

