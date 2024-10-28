import pandas # type: ignore # This still works, dw
import os
import json
import math

# Math assumptions
g = 9.81 # m/(s**2)
mu = 0 # radians
path_radius = 0.25 # meters

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

        #
        # ANGULAR VELOCITY
        #

        csv = pandas.read_csv(f"DataSets/{file}")
        [w_x , w_y, w_z] = [csv["Angular velocity X(°/s)"].mean(), csv["Angular velocity Y(°/s)"].mean(), csv["Angular velocity Z(°/s)"].mean()]
        ang_velocity = math.sqrt(w_x**2 + w_y**2 + w_z**2)

        # print(f"{valueSet} : {[w_x , w_y, w_z]}") # Remove "#" for debug!

        #
        # ROLLING FRICTION
        #

        mu_rA = g * math.sin(mu)
        mu_rB = (ang_velocity * fileValue["radius"])**2; mu_rB = mu_rB/(2 * distance)
        mu_rC = g * math.cos(mu)

        # print(f" mu_rA -> {mu_rA} \n mu_rB -> {mu_rB} \n mu_rC -> {mu_rC} \n ") # Remove "#" for debug!

        mu_r = (mu_rA - mu_rB) / mu_rC # calculation
        mu_r = abs(mu_r) # get the ratio (0 <= mu <= 1)

        calcualtion_dictonary[f"{valueSet}"] = mu_r

#
# Write Results into a JSON
#

with open("results.json","w") as results:
    json.dump(calcualtion_dictonary,results,indent=1)