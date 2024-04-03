import json


f1 = open("arrests dataset - NYPD_Arrest_Data__Year_to_Date__20240401.csv", "r")
lines = f1.readlines()

dictionary ={}

# Create the dictionary here

f1.close()

#Save the json object to a file
f2 = open("arrests dataset - NYPD_Arrest_Data__Year_to_Date__20240401.json", "w")
json.dump(dictionary, f2, indent = 4)

f2.close()
