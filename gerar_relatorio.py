from fpdf import FPDF
from datetime import datetime

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, "Relatório Financeiro - Simulação de Reservas vs Despesas", border=False, ln=True, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Gerado em: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}', align='R')

def generate_pdf_report(df, intersection_reserves, intersection_expenses, analista):
    """
    Gera o relatório financeiro em PDF.
    
    Parâmetros:
        df (pd.DataFrame): DataFrame com os dados da simulação.
        intersection_reserves (float): Reservas ajustadas no ponto de interseção.
        intersection_expenses (float): Despesas ajustadas no ponto de interseção.
        analista (str): Nome do analista responsável pelo relatório.
    """
    pdf = PDFReport()
    pdf.add_page()

    # Cabeçalho com data e local
    local = "Ponta Grossa - PR"
    data = datetime.now().strftime("%d de %B de %Y")
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"{local}, {data}", ln=True, align="R")
    pdf.ln(10)

    # Endereçamento
    pdf.set_font("Arial", "B", size=12)
    pdf.cell(0, 10, "À", ln=True)
    pdf.cell(0, 10, "Empresa XYZ", ln=True)
    pdf.cell(0, 10, "Sr. Administrador", ln=True)
    pdf.ln(10)

    # Introdução
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=(
        "Conforme sua solicitação, apresentamos o relatório com base na análise financeira "
        "das reservas e despesas acumuladas, considerando as condições fornecidas. "
        "Abaixo, seguem os resultados da simulação e o parecer técnico."
    ))
    pdf.ln(10)

    # Resultados do Ponto de Interseção
    pdf.set_font("Arial", "B", size=12)
    pdf.cell(0, 10, "Ponto de Interseção Calculado:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Reservas Ajustadas: R$ {intersection_reserves:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), ln=True)
    pdf.cell(0, 10, f"Despesas Ajustadas: R$ {intersection_expenses:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), ln=True)
    pdf.ln(10)

    # Resultados Ano a Ano
    pdf.set_font("Arial", "B", size=12)
    pdf.cell(0, 10, "Resultados Ano a Ano:", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", size=10)
    for index, row in df.iterrows():
        pdf.cell(0, 10, f"Ano {row['Ano']} - Reservas: {row['Reservas Restantes (R$)']} - Despesas: {row['Despesas Acumuladas (R$)']}", ln=True)

    pdf.ln(10)

    # Parecer Técnico
    pdf.set_font("Arial", "B", size=12)
    pdf.cell(0, 10, "Parecer Técnico:", ln=True)
    pdf.set_font("Arial", size=12)

    if intersection_reserves <= intersection_expenses:
        pdf.multi_cell(0, 10, txt=(
            "As reservas disponíveis estão em risco de se tornarem insuficientes em relação às despesas acumuladas. "
            "Recomenda-se revisar os planos financeiros, ajustar o orçamento e evitar novos compromissos financeiros."
        ))
    else:
        pdf.multi_cell(0, 10, txt=(
            "As reservas disponíveis são suficientes para cobrir as despesas acumuladas no período analisado. "
            "Recomenda-se manter o monitoramento contínuo e garantir a estabilidade financeira."
        ))

    # Assinatura do Analista
    pdf.ln(20)
    pdf.set_font("Arial", "B", size=12)
    pdf.cell(0, 10, "Atenciosamente,", ln=True)
    pdf.cell(0, 10, analista, ln=True)

    # Salvar o PDF
    pdf.output("output/relatorio_financeiro.pdf")
    