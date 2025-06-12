from fpdf import FPDF
import io

def generate_pdf_from_chat(name, sport, video_link, chat_transcript):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    title = f"{name or 'Athlete'}'s Recruiting Action Plan"
    pdf.cell(200, 10, title, ln=True, align='C')

    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    if sport:
        pdf.cell(200, 10, f"Sport: {sport}", ln=True)
    if video_link:
        pdf.cell(200, 10, f"Highlight Video: {video_link}", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Chat Summary & Advice:", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, chat_transcript)

    buffer = io.BytesIO()
    pdf.output(buffer)
    return buffer.getvalue()
