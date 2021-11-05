from collections import namedtuple
from open_binance_api import OpenBinanceApi as OBA
import plotly.graph_objects as go
import pandas as pd
from alg_ma import AlgMa

class CandlePlot():
    @staticmethod
    def make_graph(pair, interval, limit, GO_HEIGHT, GO_WIDTH, MA_1=7, MA_2=25, MA_3=100, FLAG_OPACITY=0.6,  WIDTH=2, )->str:

        LINE_COLOR = [
            '#4EC5F1',
            '#8c3d9e',
            '#0df2c9',]

        # get data from binance API
        df = OBA.get_df(pair, interval, limit, )
            

        fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'], name=f'{pair}')])

        # MA alorithm в теории это должно быть посчитанно в отдельном месте
        mov_avg = AlgMa.alg_main(df['Open'], MA_1=MA_1, MA_2=MA_2, MA_3=MA_3, )
        MA_ints = AlgMa.find_intersections(df['Date'], mov_avg=mov_avg)

        fig.add_trace(go.Scatter(x=df['Date'], y=mov_avg[0], name=f'MA {MA_1}', line=dict(color=LINE_COLOR[0], width=WIDTH)))
        fig.add_trace(go.Scatter(x=df['Date'], y=mov_avg[1], name=f'MA {MA_2}', line=dict(color=LINE_COLOR[1], width=WIDTH)))
        fig.add_trace(go.Scatter(x=df['Date'], y=mov_avg[2], name=f'MA {MA_3}', line=dict(color=LINE_COLOR[2], width=WIDTH)))


        min_val = float(min(df['Open'].min(), df['High'].min(), df['Low'].min(), df['Close'].min()))
        max_val = float(max(df['Open'].max(), df['High'].max(), df['Low'].max(), df['Close'].max()))

        def remap(x: float, max_val: float, min_val: float, out_min: float, out_max: float ):
            return (x - min_val) * (out_max - out_min) / (max_val - min_val) + out_min

        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="minute", stepmode="backward"),
                    dict(count=15, label="15m", step="minute", stepmode="backward"),
                    dict(count=1, label="1h", step="hour", stepmode="backward"),
                    dict(count=4, label="4h", step="hour", stepmode="backward"),
                    dict(count=1, label="1d", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )
        fig.update_layout(
            title=f'MA plot     Interval: {interval}, Limit: {limit}',
            yaxis_title=f'{pair} Stock',
            xaxis_title='Time',
            height=GO_HEIGHT,
            width=GO_WIDTH,
            legend=dict(
                yanchor="top",
                y=0.22,
                xanchor="left",
                x=0.01
            ),
            showlegend=True,
            xaxis_rangeslider_visible=True,        
            # draw ticks
            shapes = [dict(
                x0=i.timestamp, 
                x1=i.timestamp, 
                y0=0 if i.type == 'fall' else remap(i.val, max_val, min_val, 0, 1), 
                y1=remap(i.val, max_val, min_val, 0, 1) if i.type == 'fall' else 1, 
                xref='x', 
                yref='paper', 
                line_width=1, 
                opacity=FLAG_OPACITY,) for i in MA_ints ],
            annotations=[dict(
                x=i.timestamp, 
                y=0.01 if i.type == 'fall' else 0.99 , 
                xref='x', 
                yref='paper', 
                showarrow=False, 
                xanchor='left', 
                text=i.type, 
                bgcolor='red' if i.type == 'fall' else 'green') for i in MA_ints],
            hovermode='x',
        )

        # fig.show()
        fig.write_html(
            "./templates/graph_file.html",
            full_html=False,
            )
        print(MA_ints[-1], MA_ints[-2])
        return "./templates/graph_file.html"


if __name__ == '__main__':
    # write file at "./templates/graph_file.html"
    CandlePlot.make_graph(
        pair = 'RVNUSDT',
        interval = '5m',
        limit = 1000,
        GO_HEIGHT=1000,
        GO_WIDTH=1000,
    )