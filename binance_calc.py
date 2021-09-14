# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import json
import requests
import numpy as np
from datetime import datetime
from collections import namedtuple
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime


# %%
# configs
pair = 'RVNUSDT'
interval = '5m'
limit = 1000


WIDTH = 2
LINE_COLOR = [
    '#4EC5F1',
    '#8c3d9e',
    '#0df2c9',]

MA_1 = 7
MA_2 = 25
MA_3 = 100

FLAG_OPACITY = 0.6
resource = requests.get(f"https://api.binance.com/api/v1/klines?symbol=%s&interval={interval}&limit={limit}" % (pair))
data = json.loads(resource.text)


# %%

def real_time(time_: int):
    return datetime.fromtimestamp(time_/1000.0)

Date_list = []
Open_list = []
High_list = []
Low_list = []
Close_list = []

for i in data:
    Date_list.append(i[0])
    Open_list.append(i[1])
    High_list.append(i[2])
    Low_list.append(i[3])
    Close_list.append(i[4])

df = pd.DataFrame()
df['Date'] = Date_list 
# datetime objects
df['Date'] = df['Date'].to_frame().applymap(real_time)
# candlestick data
df['Open'] = Open_list
df['High'] = High_list
df['Low'] = Low_list
df['Close'] = Close_list 
# unix time
df['Real_Date'] = Date_list 

fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'], name=f'{pair}')])

prices = np.array( np.float64(Open_list))



mov_avg = [[], [], []]
mov_avg[0] = df['Open'].rolling(window = MA_1).mean()
mov_avg[1] = df['Open'].rolling(window = MA_2).mean()
mov_avg[2] = df['Open'].rolling(window = MA_3).mean()
fig.add_trace(go.Scatter(x=df['Date'], y=mov_avg[0], name=f'MA {MA_1}', line=dict(color=LINE_COLOR[0], width=WIDTH)))
fig.add_trace(go.Scatter(x=df['Date'], y=mov_avg[1], name=f'MA {MA_2}', line=dict(color=LINE_COLOR[1], width=WIDTH)))
fig.add_trace(go.Scatter(x=df['Date'], y=mov_avg[2], name=f'MA {MA_3}', line=dict(color=LINE_COLOR[2], width=WIDTH)))


# %%
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
    # height=750,
    # width=1230,

)
fig.update_layout(legend=dict(
    yanchor="top",
    y=0.22,
    xanchor="left",
    x=0.01
))
fig.update_layout(showlegend=True)
# fig.update_xaxes(

# )


fig.update_layout(xaxis_rangeslider_visible=True)
max_val = float(max(Open_list+High_list+Low_list+Close_list))
min_val = float(min(Open_list+High_list+Low_list+Close_list))

type(max_val), min_val, min(Open_list+High_list+Low_list+Close_list)


# %%
# найти координаты пересечения линий
def find_intersections(arr1, arr2):
    intersections = []
    MA_point = namedtuple('MA_point', 'timestamp val type')
    for num, i in enumerate(df['Date']):
        # if num == 999: print(num)
        if num == 0: next(enumerate(df['Date']))
        else:    
            A1 = arr1[num-1]
            A2 = arr1[num] 
            B1 = arr2[num-1]
            B2 = arr2[num] 
            if (A1 > B1) and (B2 > A2):
                intersections.append(MA_point(i, arr1[num], 'fall'))
            if (A1 < B1) and (B2 < A2):
                intersections.append(MA_point(i, arr1[num], 'raise'))

    return intersections

def remap(x: float, max_val: float, min_val: float, out_min: float, out_max: float ):
    return (x - min_val) * (out_max - out_min) / (max_val - min_val) + out_min
# find intersections MA_2 and MA_3
MA_ints = find_intersections(mov_avg[0], mov_avg[1],)


# %%
# draw ticks
fig.update_layout(
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
# rename traces


# %%
# TODO понятькак считать временные метки типа там есть начало и конец а в график можно засунуть только одну цыфру получается надо среднее считать
# TODO скльзящее среднее считается по открытию свечи (но верно ли жто???)


# %%
fig.show()
print(MA_ints[-1], MA_ints[-2])


