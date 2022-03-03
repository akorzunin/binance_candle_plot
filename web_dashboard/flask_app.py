
from flask import Flask, app, redirect, url_for, render_template
from datetime import datetime
from flask import request

import os
from dotenv import load_dotenv
load_dotenv()
PWD = os.getenv("PWD")
import sys
sys.path.insert(1, PWD + "\\modules")

app = Flask(__name__)
# Import Dash application
from realtime_dashboard import init_dashboard as init_rt_dashboard
from trading_dashboard import init_dashboard as init_trd_dashboard

# render dashboard template
from jinja2 import Environment, FileSystemLoader

# dict w/ common data to be rendered in templates
defaults = {
    # 'members': members,
    # 'folder_content_html': folder_content_html,
    # 'url_for': url_for,
}

env = Environment(loader=FileSystemLoader(f'{PWD}/web_dashboard/templates'))
template = env.get_template('dashboard.html')

# attach dashboard to flask
app = init_rt_dashboard(
    app,
    # dashboard template content
    html_layout=template.render(
        content='_',
        page_title='Real time dashboard',
        **defaults,
        )
    )
app = init_trd_dashboard(
    app,
    # dashboard template content
    html_layout=template.render(
        content='_',
        page_title='Trading dashboard',
        **defaults,
        )
    )


@app.route('/')
def home():
    # return '123'
    return render_template(
        '/index.html', content=datetime.now(), 
        # url_for,
    )
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    
@app.route('/shutdown')     
def shutdown():
    shutdown_server()
    return 'Server shutting down...'
@app.route('/is_alive')
def is_alive():
    return {'is_alive': True}

if __name__ == '__main__':
    app.run(debug=1, host='0.0.0.0', port=5005)