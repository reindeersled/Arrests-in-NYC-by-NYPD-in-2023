# flask --app data_server run
from flask import Flask
from flask import render_template
import json


app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    f = open("data/Excel_dataset.json", "r")
    data = json.load(f)

    f.close()

    boroughs = ["bronx", "brooklyn", "manhattan", "queens", "staten_island"]

    dictionary = {}
    for borough in boroughs:
        dictionary[borough] = []

    for id_key in data:
        if data[id_key][3] == "B":
            dictionary["bronx"].append(data[id_key])
        elif data[id_key][3] == "S":
            dictionary["staten_island"].append(data[id_key])
        elif data[id_key][3] == "K":
            dictionary["brooklyn"].append(data[id_key])
        elif data[id_key][3] == "M":
            dictionary["manhattan"].append(data[id_key])
        elif data[id_key][3] == "Q":
            dictionary["queens"].append(data[id_key]) 

    return render_template('index.html', boroughs=boroughs, dict=dictionary)

@app.route('/about')
def about():
    return render_template('/about.html')

@app.route('/micro/<borough>')
def micro(borough):
    boroughs = ["bronx", "brooklyn", "manhattan", "queens", "staten_island"]

    return render_template('/micro/<borough>.html', boroughs=boroughs)

app.run(debug=True)