import plotly.graph_objs as go
import pandas as pd

from backtest import Backtest

class BacktestComparator:

    def __init__(self, backtests: list[Backtest]) -> None:
        self.backtests = backtests

    def plot(self) -> None:
        traces = [b.get_trace() for b in self.backtests]

        fig = go.Figure()
        for trace in traces:
            fig.add_trace(trace)

        fig.update_layout(title='Stock comparison',
                  xaxis_title='Date',
                  yaxis_title='Share value')
        fig.show()

    def plot_DCA(self, monthly_invested: int) -> None:
        fig = go.Figure()

        traces = [b.get_trace_DCA(monthly_invested) for b in self.backtests]

        # FIXME, better handle dates
        dates = self.backtests[0].df['Date'].copy()
        amounts = (dates.index+1) * monthly_invested
        uninvested_trace = go.Scatter(x=dates, y=amounts, mode='lines', name='Uninvested cash')

        fig.add_trace(uninvested_trace)

        for trace in traces:
            fig.add_trace(trace)

        fig.update_layout(title='DCA comparison',
                  xaxis_title='Date',
                  yaxis_title='Wallet value')
        fig.show()
