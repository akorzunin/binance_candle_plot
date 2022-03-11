
from dis import dis
from tkinter.scrolledtext import ScrolledText
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output
from dash import html
from dash import dcc
from dash import dash_table
from flask import url_for
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
PWD = os.getenv("PWD")
import sys
sys.path.insert(1, f'{PWD}\\modules')

from api_modules.open_binance_api import OpenBinanceApi
from plot_modules.candle_plot import CandlePlot
from dash.exceptions import PreventUpdate
import requests
import json

from data_API.data_API_wrapper import DataApiWrapper
# styles for dashboard
from dash_styles.data_dashboard import *



endpoint = 'http://192.168.1.125:8000'

data_API = DataApiWrapper(
    endpoint=endpoint
)
def get_df():
    return OpenBinanceApi.get_df(
            pair = 'RVNUSDT', # pair
            interval = '1m', # Interval
            limit = 1000,   # limit
    )

def get_API_data(endpoint: str, df_name: str) -> pd.DataFrame:
    r = requests.get(f'{endpoint}/{df_name}', )         
    return pd.read_json(r.json()[f'{df_name}'])

dash_table_settings = dict(
    fixed_rows={ 'headers': 1, 'data': 0},
    # style_table={'height': '500px', 'overflowY': 'auto'},

)

def init_dashboard(server, **kwargs):
    """Create a Plotly Dash dashboard."""
    html_layout = kwargs.pop('html_layout',)

    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/dash_data_dashboard/",
        external_stylesheets=[
            "/static/styles/dash_data_dashboard.css",
            "https://fonts.googleapis.com/css?family=Lato",
        ],
    )
    # add web page layout to dash layout
    dash_app.index_string = html_layout
    df = get_df()
    df_p_trdr = pd.DataFrame(
        {
            'RVN': ['USD', 'Fee'],
            '0000.00': ['0000.00','0000.00'],
        }, index=[0, 1],
    )

    dash_app.layout = html.Section([
        html.Div([
            html.Div(
                [
                html.Div(children=[
                    html.H4('PaperTrader info'),
                    dash_table.DataTable(
                        id='tbl_p_trdr',
                        columns=(
                            {'name': 'Column 1', 'id': 'name'},
                            {'name': 'Column 2', 'id': 'value'},
                        ), 
                        data=[
                            {'name': 'RVN', 'value': '0000.00', },
                            {'name': 'USD', 'value': '0000.00', },
                            {'name': 'Fee', 'value': '0000.00', },
                        ],
                        # hide columns names
                        css=[
                            {
                                'selector': 'tr:first-child',
                                'rule': 'display: none',
                            },
                        ],
                    ),
                    ],
                    className='block_2',
                    style=block_2_style,
                ),
                html.Div(children=[
                    html.H4('Last MA line values'),
                    dash_table.DataTable(
                        id='tbl_MA_lines',
                        columns=(
                            {'name': 'Column 1', 'id': 'name'},
                            {'name': 'Column 2', 'id': 'value'},
                        ), 
                        data=[
                            {'name': 'MA 7', 'value': '0000.00', },
                            {'name': 'MA 25', 'value': '0000.00', },
                            {'name': 'MA 100', 'value': '0000.00', },
                        ],
                        # hide columns names
                        css=[
                            {
                                'selector': 'tr:first-child',
                                'rule': 'display: none',
                            },
                        ], 
                    ),
                    ],
                    className='block_2',
                    style=block_2_style,
                ),      

            ],
            className='block_1',
            style=block_1_style,
            ),
            html.Div([
                html.H2('Trading data'),
                dash_table.DataTable(
                    id='tbl_trade_data',
                    data=df.to_dict('records'),
                    columns=[{"name": i, "id": i} for i in df.columns], 
                    page_size=13,
                    style_table={'height': '460px'},
                    **dash_table_settings,

                ),
            ],
            className='block_4',
            style=block_4_style,
            ),

        ],
        className='block_5',
        style=block_5_style,
        ),
        html.Div([
            html.H2('Current stock data'),
            dash_table.DataTable(
                id='tbl_stock_data',
                data=df.to_dict('records'),
                columns=[{"name": i, "id": i} for i in df.columns],
                page_size=22, 
                style_table={'max-height': '800px','height': '700px'},
                **dash_table_settings,
            ),
        ],
        className='block_6',
        style=block_6_style,
        ),
        dcc.Interval(
            id='graph-update',
            interval=60*1000, # 60 seconds
            n_intervals = 0,
            disabled=1,
        ),
    ],
    style=section_style,
    )

    # ===== CALLBACKS =====

    @dash_app.callback(
        Output('tbl_stock_data', 'data'), 
        Output('tbl_stock_data', 'columns'), 
        Input('graph-update', 'n_intervals'),
    )
    def update_graph(n_intervals, *args):
        # if not value:
        #     raise PreventUpdate            
        df = data_API.get_stock_data()
        for col in ['open_', 'high_', 'low_', 'close_']:
            df[col]=df[col].map('{:.4f}'.format)

        df = df.loc[:, ['open_', 'high_', 'low_', 'close_','open_time', 'close_time', ]]
        return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]

    @dash_app.callback(
        Output('tbl_trade_data', 'data'), 
        Output('tbl_trade_data', 'columns'), 
        Input('graph-update', 'n_intervals'),
    )
    def update_graph(n_intervals, *args):
        # if not value:
        #     raise PreventUpdate   
        df = data_API.get_trade_data()
        # format data columns
        for col in ['sell_price', 'buy_price', ]:
            df[col]=df[col].map('{:.4f}'.format)
        for col in ['RVN', 'USD', '_amount']:
            df[col]=df[col].map('{:.1f}'.format)
        df = df.loc[:, ['type', 'sell_price', 'buy_price', 'fee', 'RVN', 'USD', '_amount', 'reason', 'timestamp', ]]
        return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]

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