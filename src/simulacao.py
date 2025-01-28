import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Função para formatar valores como moeda brasileira
def format_currency(value):
    """
    Formata um valor numérico como moeda brasileira (R$).
    """
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Função para simular as despesas acumuladas e reservas ao longo dos anos
def simulate_expenses_vs_reserves(initial_reserves, total_expense, years_to_predict):
    """
    Simula as despesas acumuladas e reservas restantes ao longo dos anos.

    Parâmetros:
        initial_reserves (float): Reservas iniciais.
        total_expense (float): Despesa total anual.
        years_to_predict (int): Número de anos para previsão.

    Retorna:
        pd.DataFrame: DataFrame contendo anos, reservas restantes e despesas acumuladas.
    """
    reserves = [initial_reserves]
    expenses = []

    for year in range(years_to_predict + 1):
        # Calcula despesas acumuladas
        expenses.append(total_expense * year if year > 0 else 0)
        # Atualiza as reservas remanescentes
        remaining_reserves = max(reserves[-1] - total_expense, 0)
        reserves.append(remaining_reserves)

    return pd.DataFrame({
        "Ano": list(range(years_to_predict + 1)),
        "Reservas Restantes (R$)": reserves[:years_to_predict + 1],
        "Despesas Acumuladas (R$)": expenses
    })

# Função para calcular o ponto de interseção
def calculate_intersection_point(df, initial_reserves, years_to_predict):
    """
    Calcula o ponto de interseção entre reservas e despesas acumuladas.

    Parâmetros:
        df (pd.DataFrame): DataFrame contendo os dados da simulação.
        initial_reserves (float): Reservas iniciais.
        years_to_predict (int): Número de anos para previsão.

    Retorna:
        tuple: Reservas e despesas ajustadas no ponto de interseção.
    """
    # Remover formato de moeda brasileira e converter para float
    cumulative_expenses_total = df.loc[years_to_predict, "Despesas Acumuladas (R$)"]
    if isinstance(cumulative_expenses_total, str):
        cumulative_expenses_total = float(
            cumulative_expenses_total.replace("R$", "").replace(".", "").replace(",", ".").strip()
        )
    
    intersection_expenses = cumulative_expenses_total / 2
    intersection_reserves = initial_reserves - intersection_expenses
    return intersection_reserves, intersection_expenses

# Função para gerar o gráfico de Reservas vs Despesas
def generate_expenses_vs_reserves_graph(df, initial_reserves, years_to_predict):
    """
    Gera o gráfico de Reservas Restantes vs Despesas Acumuladas.

    Parâmetros:
        df (pd.DataFrame): DataFrame contendo os dados da simulação.
        initial_reserves (float): Reservas iniciais.
        years_to_predict (int): Número de anos para previsão.
    """
    fig, ax1 = plt.subplots()

    years = df["Ano"]
    reserves = df["Reservas Restantes (R$)"]
    expenses = df["Despesas Acumuladas (R$)"]

    # Configuração do eixo de Reservas (azul)
    ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, _: format_currency(x)))
    ax1.plot(years, reserves, 'b-o', label="Reservas Restantes (R$)")
    ax1.set_xlabel("Ano")
    ax1.set_ylabel("Reservas Restantes (R$)", color="blue")
    ax1.tick_params(axis='y', labelcolor="blue")
    ax1.set_xticks(years)

    # Configuração do eixo de Despesas (vermelho)
    ax2 = ax1.twinx()
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, _: format_currency(x)))
    ax2.plot(years, expenses, 'r--x', label="Despesas Acumuladas (R$)")
    ax2.set_ylabel("Despesas Acumuladas (R$)", color="red")
    ax2.tick_params(axis='y', labelcolor="red")

    # Calcular o ponto de interseção
    intersection_reserves, intersection_expenses = calculate_intersection_point(df, initial_reserves, years_to_predict)

    # Exibir os valores calculados no terminal
    print(f"\nValores calculados para o ponto de interseção:")
    print(f"Reservas Ajustadas: {format_currency(intersection_reserves)}")
    print(f"Despesas Ajustadas: {format_currency(intersection_expenses)}\n")

    # Adicionar anotação no gráfico próximo à interseção
    if intersection_reserves <= 0:
        ax1.annotate(
            "Reservas Insuficientes!",
            xy=(years_to_predict / 2, 0),
            xytext=(years_to_predict / 2 + 1, initial_reserves * 0.1),
            arrowprops=dict(facecolor='red', arrowstyle="->", lw=0.5),
            fontsize=10,
            color="red",
            alpha=0.8
        )
    else:
        ax1.annotate(
            f"Reservas: {format_currency(intersection_reserves)}\nDespesas: {format_currency(intersection_expenses)}",
            xy=(years_to_predict / 2, intersection_reserves),
            xytext=(years_to_predict / 2 + 0.5, intersection_reserves - (intersection_reserves * 0.05)),
            arrowprops=dict(facecolor='black', arrowstyle="->", lw=0.5),
            fontsize=8,
            color="black",
            alpha=0.8
        )

    plt.title("Simulação de Reservas Lucros vs Despesas Financeiras")
    plt.tight_layout()
    plt.show()
