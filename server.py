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
    f = open("data/Excel_dataset.json", "r")
    data = json.load(f)

    f.close()

    boroughs = ["bronx", "brooklyn", "manhattan", "queens", "staten_island"]

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

    female=0
    male=0
    for gender in dictionary["PERP_SEX"]:
        if gender=="F":
            female+=1
        elif gender=="M":
            male+=1

    female = female / (female+male) * 100
    print(female)

    perp_race = {}
    for race in dictionary["PERP_RACE"]:
        if race not in perp_race.keys():
            perp_race[race] = 1
        else:
            perp_race[race] += 1

    age_group = {}
    for age in dictionary["AGE_GROUP"]:
        if age not in age_group.keys():
            age_group[age] = 1
        else:
            age_group[age] += 1
    ages=[]
    for group in age_group:
        ages.append(group)
    ages=sorted(ages)
    temp=ages[-1]
    ages.pop()
    ages.insert(0,temp)


    borough_arrests = {}
    for arrest in data:
        if data[arrest][3] not in borough_arrests.keys():
            borough_arrests[data[arrest][3]] = 1
        else:
            borough_arrests[data[arrest][3]] += 1
    del borough_arrests["ARREST_BORO"]
    del borough_arrests["F"]

    boro_avg = 0
    for key in borough_arrests:
        boro_avg += borough_arrests[key]
    boro_avg = boro_avg/5

    crime_level = {}
    for offense in dictionary["LAW_CAT_CD"]:
        if offense not in crime_level.keys():
            crime_level[offense] = 1
        else:
            crime_level[offense] += 1

    crime_desc = {}
    for desc in dictionary["OFNS_DESC"]:
        if desc not in crime_desc.keys():
            crime_desc[desc] = 1
        else:
            crime_desc[desc] += 1

    b_key = {"B":"bronx", "S":"staten_island", "K":"brooklyn", "M":"manhattan", "Q":"queens"}

    return render_template('micro.html', boroughs=boroughs, borough=borough, female=female, perp_race=perp_race, age_group=age_group, ages=ages, borough_arrests=borough_arrests, crime_level=crime_level, crime_desc=crime_desc, b_key=b_key, boro_avg=boro_avg)

app.run(debug=True)