
import sys
sys.path.insert(1, './modules')

from flask import Flask, app, redirect, url_for, render_template
import datetime
# import binance_calc
import bs4
import candle_plot
def read_file_db()-> str:
    with open("./RVNUSD_data.txt", "r") as f:
        pog = f.readlines()
    return pog
def get_graph():
    graph_file = candle_plot.CandlePlot.make_graph(
        pair = 'RVNUSDT',
        interval = '5m',
        limit = 1000,
        GO_HEIGHT=900,
        GO_WIDTH=1900,
    )
    with open(graph_file) as f:
        # get a str with html graph
        f = f.read() 
    # crate new file for tempalte
    with open('./templates/graph.html', 'w+') as g:
        g.write('{% extends "base.html" %}{%block title%} Candle plot {%endblock%}{%block content%}{{content}}')
        g.write(f)
        g.write('{%endblock%}')

    return './templates/graph.html' 

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', content=datetime.datetime.today())

@app.route('/candle')
def candle():
    get_graph()
    return render_template('graph.html', content='date: ' + str(datetime.datetime.today())+ '; some place for info')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', content=read_file_db())

@app.route('/logs')
def logs():
    return render_template('logs.html', content='content logs' + str(datetime.datetime.today()))


# @app.route('/new')
# def new():
#     return render_template('new.html')
@app.route('/myendpoint', methods=['POST', 'GET'])
def myendpoint():
    return render_template('index.html')



@app.route('/admin')
def admin():
    # diif response for admin endpoint
    # on hoome page
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='', port=5000)
