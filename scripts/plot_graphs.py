import pandas as pd
import plotly.graph_objs as go

def plot_stock_price(df: pd.DataFrame, title: str):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Datetime'], y=df['Close'], mode='lines', name='Close'))
    fig.update_layout(title=title,
                      xaxis_title='Time',
                      yaxis_title='Price',
                      template='plotly_dark',
                      height=500)
    return fig