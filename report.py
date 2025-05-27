from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
import pandas as pd

def create_etf_pdf(summary_path, csv1_path, csv2_path, output_pdf):
    # Load summary
    with open(summary_path, "r", encoding="utf-8") as f:
        summary_text = f.read()

    # Load CSVs
    df1 = pd.read_csv(csv1_path)
    df2 = pd.read_csv(csv2_path)

    # Create PDF document
    doc = SimpleDocTemplate(output_pdf, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Add title
    story.append(Paragraph("ETF Report", styles['Title']))
    story.append(Spacer(1, 12))

    # Add summary
    story.append(Paragraph("Summary", styles['Heading2']))
    story.append(Paragraph(summary_text, styles['Normal']))
    story.append(Spacer(1, 12))

    # Function to convert DataFrame to Table
    def df_to_table(df, title):
        story.append(Paragraph(title, styles['Heading2']))
        data = [df.columns.tolist()] + df.values.tolist()
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 10),
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ]))
        story.append(table)
        story.append(Spacer(1, 12))

    # Add both CSVs
    df_to_table(df1, "Top Holdings")
    df_to_table(df2, "Fundamentals")

    # Build PDF
    doc.build(story)
    print(f"PDF report saved to {output_pdf}")

'''
# Example usage
create_etf_pdf(
    summary_path="data/output_summary.txt",
    csv1_path="data/top_holdings.csv",
    csv2_path="data/stock_fundamentals.csv",
    output_pdf="report.pdf"
)
'''