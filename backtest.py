def run_backtest(data):
    data['pnl'] = data['position'].shift(1) * (data['futures_price'].pct_change())
    data['cum_pnl'] = data['pnl'].cumsum()
    return data
