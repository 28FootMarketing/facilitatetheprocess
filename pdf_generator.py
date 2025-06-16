from fpdf import FPDF

def generate_pdf_from_chat(messages, filename="chat_summary.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for msg in messages:
        role = msg.get("role", "unknown").capitalize()
        content = msg.get("content", "")
        pdf.multi_cell(0, 10, f"{role}: {content}")

    pdf.output(filename)
    return filename
