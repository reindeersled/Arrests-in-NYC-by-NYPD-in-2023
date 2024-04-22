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
    boroughs = ["bronx", "brooklyn", "manhattan", "queens", "staten_island"]
    
    return render_template('/about.html', boroughs=boroughs)

@app.route('/micro/<borough>')
def micro(borough):
    boroughs = ["bronx", "brooklyn", "manhattan", "queens", "staten_island"]

    f = open("data/Excel_dataset.json", "r")
    data = json.load(f)

    f.close()

    letter=""

    if borough=="bronx":
        letter="B"
    if borough=="brooklyn":
        letter="K"
    if borough=="queens":
        letter="Q"
    if borough=="manhattan":
        letter="M"
    if borough=="staten_island":
        letter="S"

    bor_dictionary = {}

    for id_key in data:
        if data[id_key][3]==letter:
            bor_dictionary[id_key] = data[id_key]

    details=["ARREST_DATE","OFNS_DESC","LAW_CAT_CD","ARREST_BORO","AGE_GROUP","PERP_SEX","PERP_RACE","X_COORD_CD","Y_COORD_CD","Latitude","Longitude"]
    
    dictionary={}
    
    for id in bor_dictionary:
        for detail_id in range(0, len(details)):
            if details[detail_id] not in dictionary.keys():
                dictionary[details[detail_id]] = []
                dictionary[details[detail_id]].append(bor_dictionary[id][detail_id])
            else:
                dictionary[details[detail_id]].append(bor_dictionary[id][detail_id])

    print(dictionary)
    return render_template('micro.html', boroughs=boroughs, borough=borough, dictionary=dictionary)

app.run(debug=True)