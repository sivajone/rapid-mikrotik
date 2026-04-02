from flask import Flask, render_template
import requests
from turbo_flask import Turbo
import threading
import time

app = Flask(__name__)
turbo = Turbo(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.context_processor
def inject_data():
    r = requests.get("https://timeapi.io/api/v1/time/current/unix")
    data = r.json()
    return {'data': data}

@app.before_request
def before_first_request():
    threading.Thread(target=update_data).start()

def update_data():
    with app.app_context():
        while True:
            time.sleep(5)
            turbo.push(turbo.replace(render_template('index.html'), 'data'))
