
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output
from dash import html
from dash import dcc
from flask import url_for
import os
from dotenv import load_dotenv

load_dotenv()
PWD = os.getenv("PWD")
import sys
sys.path.insert(1, f'{PWD}\\modules')
sys.path.insert(1, PWD)

from api_modules.open_binance_api import OpenBinanceApi
from plot_modules.candle_plot import CandlePlot
from dash.exceptions import PreventUpdate
from data_API.data_API_wrapper import DataApiWrapper

endpoint = 'http://192.168.1.125:8000'
data_API = DataApiWrapper(
    endpoint=endpoint
)

def get_fig():
    df = OpenBinanceApi.get_df(
            pair = 'RVNUSDT', # pair
            interval = '1m', # Interval
            limit = 1000,   # limit
    )   
    plot = CandlePlot(
        df=df,
        open_col='Open',
        close_col='Close',
        low_col='Low',
        high_col='High',
        date_col='Date',    
    )

    settings = {
        'candle_plot': 1,
        'MA_lines': 0,
        'add_trades': 0,
        'add_profit': 0,
        'profit_annotations': 0, 
        'amplitude': 0, 
        'MACD_lines': True, # to do
        'EMA_lines': True, # to do
    }
    # settings.update(kwargs)

    return plot.use_settings(
        settings=settings,
        # GO_WIDTH=1300,
        GO_HEIGHT=800,
        title='MA algoritm',
        pair='RVNUSDT',
        interval='--',
        limit='no limit',
        # MA_list=MA_list,
        # trade_data=trade_data,

    )

def init_dashboard(server, **kwargs):
    """Create a Plotly Dash dashboard."""
    html_layout = kwargs.pop('html_layout',)

    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/trading_dashboard/",
        external_stylesheets=[
            "/static/dist/css/styles.css",
            "https://fonts.googleapis.com/css?family=Lato",
        ],
    )
    # add web page layout to dash layout
    dash_app.index_string = html_layout

    dash_app.layout = html.Div([
        # title
        html.Br(),
        html.H3('Trading candlestick plot',
                style={'float': 'left',
                    }),
        html.Br(),
        html.Br(),

        html.Div([
            dbc.Row([
                dbc.Col(children=dcc.Checklist(
                    id='graph-update-checklist',
                    options=[{
                        'label': "  Auto update graph",
                        'value': 'auto_update'
                    }],
                    value=['auto_update'],
                    # style={"padding": "20px"},
                )
                ),
                dbc.Col(children=dcc.Dropdown(
                    options=[{'label': i, 'value': i} for i in ['RVNUSDT', 'pepe', 'pog']],
                    value="",
                    placeholder="Trade pair",
                    id="input_pair",
                )),
                dbc.Col(children=dcc.Dropdown(
                    options=[{'label': i, 'value': i} for i in [10, 100, 1000]],
                    value="",
                    placeholder="Limit",
                    id="input_limit_drop",
                )),
                dbc.Col(children=dcc.Dropdown(
                    options=[{'label': i, 'value': i} for i in ['1m', '5m', '15m',]],
                    value="",
                    placeholder="Interval",
                    id="input_interval",
                )),
                dbc.Col(children=dcc.DatePickerRange(
                    display_format='DD.MM.Y',
                )),
                # dbc.Col(children=dcc.Input(
                #     id="input_limit", 
                #     type="number", 
                #     placeholder="Limit",
                #     min=1, 
                #     max=1001, 
                #     # step=100,
                #     value=1000
                # )
                # ),
                ]
            ),
        ]),
        dcc.Graph(
            id='graph', 
            figure=get_fig(),
        ),
        dcc.Interval(
            id='graph-update',
            interval=5*1000, #take time from interval 
            n_intervals = 0,
        ),
    ])

    @dash_app.callback(
        Output('graph', 'figure'), 
        Input('graph-update', 'n_intervals'),
        Input('graph-update-checklist', 'value'),
    )
    def update_graph(n_intervals, value):
        if not value:
            raise PreventUpdate            
        # get_dataframe_from_thread()
        # request.???
        # w.get_data()
        return get_fig()


    return dash_app.server


if __name__ == '__main__':


    from jinja2 import Environment, FileSystemLoader

    # dict w/ common data to be rendered in templates
    defaults = {
        # 'members': members,
        # 'folder_content_html': folder_content_html,
        # 'url_for': url_for,
    }

    env = Environment(loader=FileSystemLoader(f'{PWD}/web_dashboard/templates'))
    template = env.get_template('dashboard.html')

    init_dashboard(True, html_layout=template.render(page_title='Debug_dashboard')).run(debug=True, port=8008)