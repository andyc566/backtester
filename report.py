def calculate_metrics(data):
    total_return = data['cum_pnl'].iloc[-1]
    sharpe_ratio = data['pnl'].mean() / data['pnl'].std() * np.sqrt(252)  # Annualized Sharpe
    max_drawdown = data['cum_pnl'].cummax() - data['cum_pnl']
    return total_return, sharpe_ratio, max_drawdown.max()

import matplotlib.pyplot as plt
def plot_results(data):
    plt.figure(figsize=(12,6))
    plt.plot(data['cum_pnl'], label='Cumulative PnL')
    plt.title('Strategy Performance')
    plt.xlabel('Time')
    plt.ylabel('Cumulative PnL')
    plt.legend()
    plt.show()
