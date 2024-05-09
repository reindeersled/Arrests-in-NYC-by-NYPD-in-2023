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
    boro_key = {"B":"Bronx", "S":"Staten Island", "K":"Brooklyn", "M":"Manhattan", "Q":"Queens"}

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

    color_dict={"B": "firebrick", "K": "blue", "Q": "green", "M": "orange", "S": "purple"}

    del data["ARREST_KEY"]
    for id_key in data:
        data[id_key][9] = float(data[id_key][9])
        data[id_key][10] = float(data[id_key][10]) #do i need to get rid of the /n?

    return render_template('index.html', boroughs=boroughs, dict=dictionary, data=data, color_dict=color_dict, boro_key=boro_key)

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

    female = float(str(female / (female+male) * 100)[:3])

    perp_race = {}
    for race in dictionary["PERP_RACE"]:
        if race not in perp_race.keys():
            perp_race[race] = 1
        else:
            perp_race[race] += 1

    race_total=0
    for race in perp_race:
        race_total += perp_race[race]
    for race in perp_race:
        perp_race[race] = (perp_race[race]/race_total) * 100 #converting to percentages
    
    races=[]
    for key in perp_race:
        races.append(key)
    
    n = len(races)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if perp_race[races[j]] > perp_race[races[j+1]]:
                perp_race[races[j]], perp_race[races[j+1]] = perp_race[races[j+1]], perp_race[races[j]] #sorting my perp_races by value
                swapped = True
        if (swapped == False):
            break

    pie_race = {}
    for key in perp_race:
        if key not in pie_race.keys():
            pie_race[key] = perp_race[key]
        
    for i in range(len(races)):
        if i > 0:
            for j in range(0, i):
                pie_race[races[i]] += perp_race[races[j]]
    races.reverse()

    for race in perp_race:
        perp_race[race] = float(str(perp_race[race])[:3])

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
    boro_avg = int(boro_avg/5)

    crime_level = {"F":0, "M":0, "V":0}
    for offense in dictionary["LAW_CAT_CD"]:
        if offense in crime_level.keys():
            crime_level[offense] += 1

    level_total=0
    for level in crime_level:
        level_total+=crime_level[level]
    for level in crime_level:
        crime_level[level] = (crime_level[level]/level_total) * 100

    c_levels=[]
    for key in crime_level:
        c_levels.append(key)

    for i in range(len(c_levels)):
        swapped=False
        for j in range(0, (len(c_levels)-i-1)):
            if crime_level[c_levels[j]]>crime_level[c_levels[j+1]]:
                crime_level[c_levels[j]], crime_level[c_levels[j+1]] = crime_level[c_levels[j+1]], crime_level[c_levels[j]]
    #c_levels is going from low to high
    c_levels.reverse()

    for crime in crime_level:
        crime_level[crime] = float(str(crime_level[crime])[:3])
    
    level_key={"F":"Felony", "M":"Misdemeanor", "V":"Violation"}

    crime_desc = {}
    for desc in dictionary["OFNS_DESC"]:
        if desc not in crime_desc.keys():
            crime_desc[desc] = 1
        else:
            crime_desc[desc] += 1

    b_key = {"B":"bronx", "S":"staten_island", "K":"brooklyn", "M":"manhattan", "Q":"queens"}

    total_crime_pie = {}
    for boro in boroughs:
        if boro == borough:
            total_crime_pie[boro] = 1
        else:
            total_crime_pie[boro] = .5
    print(total_crime_pie)

    return render_template('micro.html', boroughs=boroughs, borough=borough, total_crime_pie=total_crime_pie, female=female, perp_race=perp_race, races=races, pie_race=pie_race, age_group=age_group, ages=ages, borough_arrests=borough_arrests, crime_level=crime_level, c_levels=c_levels, level_key=level_key, crime_desc=crime_desc, b_key=b_key, boro_avg=boro_avg)

app.run(debug=True)