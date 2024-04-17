# flask --app data_server run
from flask import Flask
from flask import render_template
import json


app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bx.html')
def borough(): #ok. need a seperate thing for each borough
    return render_template('bx.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

app.run(debug=True)