import json


f1 = open("data/Excel_dataset.csv", "r")
lines = f1.readlines()

# Create the dictionary here
dictionary ={}

for arrest in lines:
    arrest_details = arrest.split(',') #each arrest with details as elements in a list

    dict_input = arrest_details[1:]
    dictionary[arrest_details[0]] = dict_input

f1.close()

#Save the json object to a file
f2 = open("data/Excel_dataset.json", "w")
json.dump(dictionary, f2, indent = 4)

f2.close()
