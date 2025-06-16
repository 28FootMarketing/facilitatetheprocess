from fpdf import FPDF

def generate_pdf_from_chat(name, messages, output_path="/mnt/data/chat_summary.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Chat Summary for {name}", ln=True, align='C')
    pdf.ln(10)
    for msg in messages:
        role = msg.get("role", "unknown").capitalize()
        content = msg.get("content", "")
        pdf.multi_cell(0, 10, f"{role}: {content}")
        pdf.ln(5)
    pdf.output(output_path)
    return output_path
