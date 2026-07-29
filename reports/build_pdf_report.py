import os
from fpdf import FPDF

class PDFReport(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(100, 116, 139)
        self.cell(0, 8, "Student Management Portal - Internship Capstone Project Report", align="R")
        self.ln(10)
        self.set_draw_color(226, 232, 240)
        self.line(10, 18, 200, 18)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(148, 163, 184)
        self.cell(0, 10, f"Page {self.page_no()} of {{nb}}", align="C")

def sanitize_text(text: str) -> str:
    """Replaces non-latin1 unicode characters with ASCII equivalents."""
    replacements = {
        '\u2013': '-',   # en-dash
        '\u2014': '--',  # em-dash
        '\u2018': "'",   # left single quote
        '\u2019': "'",   # right single quote
        '\u201c': '"',   # left double quote
        '\u201d': '"',   # right double quote
        '\u2022': '*',   # bullet
        '\u2026': '...', # ellipsis
        '\u200b': '',    # zero-width space
        '🎓': '',
        '🌟': '',
        '🔐': '',
        '📊': '',
        '👨‍🎓': '',
        '🛡️': '',
        '🏗️': '',
        '⚡': '',
        '🔑': '',
        '🧪': '',
        '📜': '',
        '🛠️': '',
        '🎬': '',
        '🎙️': ''
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.encode('latin-1', 'ignore').decode('latin-1')

def generate_pdf():
    md_file_path = os.path.join(os.path.dirname(__file__), 'project_report.md')
    pdf_file_path = os.path.join(os.path.dirname(__file__), 'project_report.pdf')

    if not os.path.exists(md_file_path):
        print(f"Error: {md_file_path} not found.")
        return

    with open(md_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    pdf = PDFReport()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_left_margin(12)
    pdf.set_right_margin(12)

    for line in lines:
        raw_line = sanitize_text(line.strip())
        
        if not raw_line:
            pdf.ln(3)
            continue

        if raw_line.startswith("# "):
            pdf.set_font("Helvetica", "B", 18)
            pdf.set_text_color(15, 23, 42)
            pdf.cell(0, 12, raw_line[2:].strip(), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
        elif raw_line.startswith("## "):
            pdf.set_font("Helvetica", "B", 14)
            pdf.set_text_color(37, 99, 235)
            pdf.cell(0, 10, raw_line[3:].strip(), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
        elif raw_line.startswith("### "):
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_text_color(30, 41, 59)
            pdf.cell(0, 8, raw_line[4:].strip(), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)
        elif raw_line.startswith("|") and "|" in raw_line[1:]:
            pdf.set_font("Courier", "", 9)
            pdf.set_text_color(51, 65, 85)
            clean_table_row = raw_line.replace("|", " ").strip()
            pdf.multi_cell(pdf.epw, 5, clean_table_row)
        elif raw_line.startswith("- ") or raw_line.startswith("* "):
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(30, 41, 59)
            bullet_text = "  - " + raw_line[2:].strip()
            pdf.multi_cell(pdf.epw, 6, bullet_text)
        elif raw_line.startswith("> "):
            pdf.set_font("Helvetica", "I", 10)
            pdf.set_text_color(71, 85, 105)
            pdf.multi_cell(pdf.epw, 6, "  " + raw_line[2:].strip())
        else:
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(30, 41, 59)
            clean_text = raw_line.replace("**", "").replace("*", "").replace("`", "")
            pdf.multi_cell(pdf.epw, 6, clean_text)

    pdf.output(pdf_file_path)
    print(f"PDF successfully generated at: {pdf_file_path}")

if __name__ == '__main__':
    generate_pdf()
