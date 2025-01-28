from src.simulacao import (
    simulate_expenses_vs_reserves,
    calculate_intersection_point,
    generate_expenses_vs_reserves_graph,
    format_currency
)
from gerar_relatorio import generate_pdf_report
from tabulate import tabulate

def parse_float(value):
    try:
        return float(value)
    except ValueError:
        print("Entrada inválida! Por favor, insira um valor numérico.")
        exit()

def main():
    print("Simulação Financeira - Reservas vs Despesas\n")

    # Entrada de dados
    initial_reserves = parse_float(input("Digite o valor das Reservas Iniciais (em R$): "))
    existing_loans = parse_float(input("Digite o saldo devedor de empréstimos existentes (em R$): "))
    existing_rate = parse_float(input("Digite a taxa de juros existente (% ao ano): "))
    new_loan = parse_float(input("Digite o valor do novo empréstimo (em R$): "))
    new_rate = parse_float(input("Digite a taxa de juros do novo empréstimo (% ao ano): "))
    years_to_predict = int(input("Digite o número de anos para previsão: "))
    analista = input("Digite o nome do analista responsável pelo relatório: ")

    # Calcular despesas totais
    total_expense = (existing_loans * existing_rate / 100) + (new_loan * new_rate / 100)

    # Simular valores
    df = simulate_expenses_vs_reserves(initial_reserves, total_expense, years_to_predict)

    # Calcular ponto de interseção
    intersection_reserves, intersection_expenses = calculate_intersection_point(df, initial_reserves, years_to_predict)

    # Copiar DataFrame para exibição com formatação
    df_formatted = df.copy()
    df_formatted["Reservas Restantes (R$)"] = df["Reservas Restantes (R$)"].apply(format_currency)
    df_formatted["Despesas Acumuladas (R$)"] = df["Despesas Acumuladas (R$)"].apply(format_currency)

    # Mostrar resultados no terminal
    print("\nResultados da Simulação:")
    print(tabulate(df_formatted, headers="keys", tablefmt="grid", showindex=False, numalign="right"))

    # Gerar gráfico (usando o DataFrame original)
    generate_expenses_vs_reserves_graph(df, initial_reserves, years_to_predict)

    # Gerar relatório PDF (usando o DataFrame formatado)
    generate_pdf_report(df_formatted, intersection_reserves, intersection_expenses, analista)
    print("\nRelatório PDF gerado em 'output/relatorio_financeiro.pdf'.")

if __name__ == "__main__":
    main()
