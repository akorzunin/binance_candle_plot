
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

def get_df():
    return OpenBinanceApi.get_df(
            pair = 'RVNUSDT', # pair
            interval = '1m', # Interval
            limit = 1000,   # limit
    )
section_style = {
    'display': 'flex',
    'flex-direction': 'row',
    'justify-content': 'space-between',
    'width': '80%',
    'margin': '52px auto',
    'min-height': '300px',
    'max-height': '800px',
    
}
block_1_style = {
    'display': 'flex',
    'height': '30%',
    'width': '100%',
    'flex-direction': 'row',
    'justify-content': 'center',
}
block_2_style = {
    'height': '100%',
    'width': '50%',
    'padding': '15px',
    'background': '#ccc',
}
block_4_style = {
    'width': '100%',
    'height': '70%',
    'background': '#ccc',
    'overflow-y': 'scroll',
}
block_5_style = {
    'width': '35%',
}
block_6_style = {
    'width': '60%',
    'background': '#ccc',
    'overflow-y': 'scroll',
}

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
                        data=df_p_trdr.to_dict('records'),
                        columns=[{"name": i, "id": i} for i in df_p_trdr.columns], 
                    ),
                    ],
                    className='block_2',
                    style=block_2_style,
                ),
                html.Div(children=[
                    html.H4('Last MA line values'),
                    dash_table.DataTable(
                        id='tbl_MA_lines',
                        data=df_p_trdr.to_dict('records'),
                        columns=[{"name": i, "id": i} for i in df_p_trdr.columns], 
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
                id='tbl_df',
                data=df.to_dict('records'),
                columns=[{"name": i, "id": i} for i in df.columns], 
            ),
        ],
        className='block_6',
        style=block_6_style,
        )
    ],
    style=section_style,
    )

    # dash_app.layout = html.Div([
    #     # title
    #     # html.Br(),
    #     # html.H3('dash_data_dashboard',
    #     #         style={'float': 'left',
    #     #             }),
    #     dash_table.DataTable(
    #         id='tbl',
    #         data=df.to_dict('records'),
    #         columns=[{"name": i, "id": i} for i in df.columns], 
    #     ),
    #     # html.Br(),
    #     # html.Br(),
    #     dcc.Interval(
    #         id='graph-update',
    #         interval=60*1000, #take time from interval 
    #         n_intervals = 0,
    #     ),
    # ])

    @dash_app.callback(
        Output('tbl', 'data'), 
        Output('tbl', 'columns'), 
        Input('graph-update', 'n_intervals'),
    )
    def update_graph(n_intervals, *args):
        # if not value:
        #     raise PreventUpdate            
        df =  get_df()
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