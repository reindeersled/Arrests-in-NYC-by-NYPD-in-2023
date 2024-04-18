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

    boroughs = ["Bronx", "Brooklyn", "Manhattan", "Queens", "Staten_Island"]

    dictionary = {}
    for borough in boroughs:
        dictionary[borough] = []

    for id_key in data:
        print(data[id_key][3]) #THE BOROUGH CODE

        if data[id_key][3] 



        # for id in data: #those are each individual arrests
        #     arrest = id.split(",")
        #     print(arrest)
            
        #     if arrest[3] == "B":
        #         dictionary["Bronx"].append(arrest)
        #     elif arrest[3] == "S":
        #         dictionary["Staten_Island"].append(arrest)
        #     elif arrest[3] == "K":
        #         dictionary["Brooklyn"].append(arrest)
        #     elif arrest[3] == "M":
        #         dictionary["Manhattan"].append(arrest)
        #     elif arrest[3] == "Q":
        #         dictionary["Queens"].append(arrest) 

    print(dictionary)
        




    return render_template('index.html')

@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/micro/bronx')
def bronx(): #ok. need a seperate thing for each borough??
    return render_template('/micro/bronx.html')

app.run(debug=True)