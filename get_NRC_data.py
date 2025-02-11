import requests
import numpy as np
import mysql.connector
from pathlib import Path
import time
from datetime import datetime
from utils import get_plant_hashmap, get_reverse_plant_hashmap
from secrets import secrets

# Check the write_to_database.py if there is ever a plant added to the list

target_url = "https://www.nrc.gov/reading-rm/doc-collections/event-status/reactor-status/powerreactorstatusforlast365days.txt"

def get_data_365(url):
    response = requests.get(url)
    out_string = response.text
    return out_string


# pulling from this website: https://www.nrc.gov/reactors/operating/list-power-reactor-units.html
plant_hashmap = get_plant_hashmap()

#plant_hashmap_reverse = dict((v, k) for k, v in plant_hashmap.items())
plant_hashmap_reverse = get_reverse_plant_hashmap()

text = get_data_365(target_url)


array = np.zeros([365, 95], dtype=object)


beginning = 0
DT_compare = "starter"
m = -1
x = 0
for i in range(len(text)):

    if text[i:i+1] == "\n":
        secondary_beginning = 0
        secondary_text = text[beginning:i-1]
        k = 0
        x = x + 1
        for j in range(len(secondary_text)):
            if secondary_text[j] == "|":
                if k == 0:
                    DT = secondary_text[secondary_beginning:j]
                elif k == 1:
                    plant = secondary_text[secondary_beginning:j]

                k = k + 1
                secondary_beginning = j + 1
                beginning = i + 1

            elif (k == 2) and (x > 1):
                power = secondary_text[secondary_beginning:len(secondary_text)]
                k = k + 1
                beginning = i + 1
                if DT != DT_compare:
                    DT_compare = DT
                    m = m + 1
                    array[m, 0] = DT
                array[m, plant_hashmap[plant]] = power



conn = mysql.connector.connect(
    host = secrets.get('HOST') ,
    user = secrets.get('DATABASE_USER') ,
    password = secrets.get('DATABASE_PASSWORD') ,
    database = secrets.get('DATABASE_NAME')
)


for columns in range(95):
    if columns > 0:
        five_days_of_data = [int(array[0][columns]), int(array[1][columns]), int(array[2][columns]), int(array[3][columns]), int(array[4][columns])]
        five_day_average = np.mean(five_days_of_data)
        stability_value = int(array[0][columns]) - five_day_average
        if stability_value > 10:
            stability = "Increasing"
        elif stability_value < -10:
            stability = "Decreasing"
        else:
            stability = "Stable"

        plant_input = plant_hashmap_reverse[columns]
        mycursor = conn.cursor()
        mycursor.execute("UPDATE plant_info SET stability=%s where plant_name=%s", (stability, plant_input))
        conn.commit()



mycursor = conn.cursor()
for z in range(94):
    plant_input = plant_hashmap_reverse[z+1]
    power_input = int(array[0][plant_hashmap[plant_input]])
    #print(plant_input)
    #print(power_input)
    mycursor.execute("UPDATE plant_info SET power=%s where plant_name=%s", (power_input, plant_input))

conn.commit()


for z in range(95):
    if z == 0:
        plant_input = "DateTime"
    else:
        plant_input = "plant_" + str(z)
    for ii in range(360):
        if z == 0:
            power_input = array[ii][z]
        else:
            power_input = int(array[ii][z])
        #print(plant_input)
        #print(power_input)
        string_temp = "UPDATE data_360 SET " + plant_input + "=%s where ID=%s"
        mycursor = conn.cursor()
        mycursor.execute(string_temp, (power_input, ii+1))
        conn.commit()


#Update historian table with most up to date data
# Get current date of highest increment ID
query_string = "SELECT DateTime FROM historian_data ORDER BY id DESC LIMIT 0, 1;"
mycursor = conn.cursor()
mycursor.execute(query_string)
historian_last_date_table = mycursor.fetchall()
conn.commit()

historian_last_date = historian_last_date_table[0][0]

# Check first increment id of 360 table
query_string = "SELECT DateTime FROM data_360 WHERE ID=1;"
mycursor = conn.cursor()
mycursor.execute(query_string)
data_360_last_date_table = mycursor.fetchall()
conn.commit()

data_360_last_date = data_360_last_date_table[0][0]

# See the difference in date
d1 = datetime.strptime(historian_last_date, "%m/%d/%Y")
d2 = datetime.strptime(data_360_last_date, "%m/%d/%Y %H:%M:%S AM")

date_diff = (d2 - d1).days

date_1_str = d1.strftime("%m/%d/%Y")
date_2_str = d2.strftime("%m/%d/%Y")


# add that many rows to historian and populate them with that the data from 360
if date_diff != 0:
    for i in range(int(date_diff)):
        ID_to_get = date_diff - i
        query_string = "SELECT * FROM data_360 WHERE ID=" + str(ID_to_get) + ";"
        mycursor = conn.cursor()
        mycursor.execute(query_string)
        row_from_data_360_table = mycursor.fetchall()
        conn.commit()

        query_string = "INSERT INTO historian_data (ID) VALUES (NULL);"
        mycursor = conn.cursor()
        mycursor.execute(query_string)
        conn.commit()

        query_string = "SELECT MAX(ID) FROM historian_data;"
        mycursor = conn.cursor()
        mycursor.execute(query_string)
        row_to_insert_data = mycursor.fetchall()
        conn.commit()
        row_to_insert_data = row_to_insert_data[0][0]

        for rows in row_from_data_360_table:
            for j in range(95):
                if j == 0:
                    plant_input = "DateTime"
                    d2 = datetime.strptime(rows[0], "%m/%d/%Y %H:%M:%S AM")
                    date_str = d2.strftime("%m/%d/%Y")
                else:
                    plant_input = "plant_" + str(j)
                current_data = rows[j]
                query = "UPDATE historian_data SET " + plant_input + "=%s where ID=%s;"
                mycursor = conn.cursor()
                if j == 0:
                    mycursor.execute(query, (date_str, row_to_insert_data))
                else:
                    mycursor.execute(query, (current_data, row_to_insert_data))
                conn.commit()

print("Data Successfully Added to Database")


