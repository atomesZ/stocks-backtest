import pandas as pd
import numpy as np
import plotly.graph_objs as go


class Backtest:
    """
    Load and plot historical stocks data for a given stock
    """

    def __init__(self, csv_path: str, is_copy_pasted_csv: bool = False) -> None:
        """
        Args:
            csv_path (str): path to the CSV containing data from yahoo finance, example: https://finance.yahoo.com/quote/%5EGSPC/history/?frequency=1mo&period1=1705528411&period2=1713386985
            is_copy_pasted_csv (bool, optional): Did you copy pasted the data or was it downloaded. Defaults to False (downloaded).
        """
        self.csv_path = csv_path
        if is_copy_pasted_csv:
            self.df = self._read_copy_pasted_csv()
        else:
            self.df = self.read_downloaded_csv()

    def get_trace(self):
        return go.Scatter(
            x=self.df["Date"], y=self.df["Open"], mode="lines", name=self.csv_path
        )

    def plot(self) -> None:
        trace = self.get_trace()
        fig = go.Figure()
        fig.add_trace(trace)
        fig.show()

    def get_trace_DCA(self, monthly_invested: int) -> go.Scatter:
        df = self.df  # alias
        df["Shares bought"] = monthly_invested / df["Open"]
        df["Cumulative shares"] = df["Shares bought"].cumsum()
        df["Wallet value"] = df["Cumulative shares"] * df["Open"]

        trace = go.Scatter(
            x=df["Date"], y=df["Wallet value"], mode="lines", name=self.csv_path
        )

        return trace

    def plot_DCA(self, monthly_invested: int) -> None:
        trace = self.get_trace_DCA(monthly_invested)
        fig = go.Figure()
        fig.add_trace(trace)
        fig.show()

    def read_downloaded_csv(self) -> pd.DataFrame:
        return pd.read_csv(self.csv_path)

    def _read_copy_pasted_csv(self) -> pd.DataFrame:
        """
        Read data copy pasted from
        https://finance.yahoo.com/quote/%5EGSPC/history/?frequency=1mo&period1=1705528411&period2=1713386985
        """
        schema = {
            "Date": str,
            "Open": np.float64,
            "High": np.float64,
            "Low": np.float64,
            "Close": np.float64,
            "Adj Close": np.float64,
            "Volume": int,
        }

        df = pd.read_csv(
            self.csv_path,
            header=None,
            dtype=schema,
            names=list(schema.keys()),
            thousands=",",
            sep="\t",
        )

        df["Date"] = pd.to_datetime(df["Date"], format="%b %d, %Y")

        df = df.sort_values("Date").reset_index(drop=True)

        return df
