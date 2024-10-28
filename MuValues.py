import pandas # type: ignore # This still works, dw
import os
import json
import math

# Math assumptions
g = 9.81 # m/(s**2)
theta = 0 # radians
path_radius = 0.017 # meters

# prefunction calculations
distance = 2 * math.pi * path_radius

# MatLab Stuff
mat = None
DataSets_fldr = os.listdir(f"DataSets\\")
DataSetVal_fldr = os.listdir(f"DataSet_values\\")

calcualtion_dictonary = {}

for file in DataSets_fldr:
    with open(f"DataSets\\{file}","r") as file_obj:
        valueSet = file.split(".")[0] # (Name | File-type), "|" denotes a split
        with open(f"DataSet_values\\{valueSet}.json","r") as setValues:
            fileValue = json.load(setValues)

        print(f"\nWheel Name: {valueSet}")

        #
        # ANGULAR VELOCITY
        #

        csv = pandas.read_csv(f"DataSets/{file}")
        [w_x , w_y, w_z] = [csv["Angular velocity X(°/s)"].mean(), csv["Angular velocity Y(°/s)"].mean(), csv["Angular velocity Z(°/s)"].mean()]
        ang_velocity = math.sqrt(w_x**2 + w_y**2 + w_z**2)

        print(f"Magnitude of Angular Velocity = {ang_velocity}")

        #print(f"{valueSet} : {[w_x , w_y, w_z]}") # Remove "#" for debug!

        #
        # ROLLING FRICTION
        #

        radius = fileValue["radius"]
        print(f"Wheel Radius: {radius}")

        # print(f" ({g * math.sin(theta)}) - ({(ang_velocity * radius)**2}/{2 * distance}) \n --------------- \n ({g * math.cos(theta)})") # Remove "#" for debug!

        mu_r = ((g*math.sin(theta)) - ((ang_velocity * radius)**2)/2*distance)/(g*math.cos(theta));# calculation
        mu_r = abs(mu_r) # get the ratio (0 < mu < 1)

        print(f"Rolling Friction: {mu_r}")

        calcualtion_dictonary[f"{valueSet}"] = mu_r

#
# Write Results into a JSON
#

print("\n NOTE! Lower Rolling Friction is Better \n")
print("Results (Also in \"results.json\"): ")
for key in calcualtion_dictonary.keys():
    print(f"{key} : {calcualtion_dictonary[key]}")

with open("results.json","w") as results:
    json.dump(calcualtion_dictonary,results,indent=1)