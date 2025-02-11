
from flask import Flask, render_template, request
import mysql.connector
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.relativedelta import relativedelta
from secrets import secrets
from utils import get_plant_hashmap, get_upper_plant_hashmap

app = Flask(__name__)


try:
    conn = mysql.connector.connect(
    host = secrets.get('HOST') ,
    user = secrets.get('DATABASE_USER') ,
    password = secrets.get('DATABASE_PASSWORD') ,
    database = secrets.get('DATABASE_NAME')
    )

    message =  'Successfully connected'
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM plant_info")
    results1 = mycursor.fetchall()
    conn.commit()
    mycursor = conn.cursor()
    mycursor.execute("Select DateTime FROM data_360 WHERE ID=1")
    todays_date = mycursor.fetchall()
    d1 = datetime.strptime(todays_date[0][0], '%m/%d/%Y %H:%M:%S AM')
    todays_date = d1.strftime("%m/%d/%Y")
    conn.commit()

    query = "SELECT DateTime FROM historian_data WHERE ID=1;"
    mycursor = conn.cursor()
    mycursor.execute(query)
    first_available_date = mycursor.fetchall()
    conn.commit()
    first_available_date = datetime.strptime(first_available_date[0][0], '%m/%d/%Y')
    first_available_date = first_available_date.strftime("%m/%d/%Y")
except mysql.connector.Error as e:
    results1 = ["#"]
    message = 'NOT CONNECTED'
    todays_date = 'Error'


@app.route('/')
def index():
    return render_template('index.html', results1 = results1, todays_date = todays_date, first_available_date = first_available_date)


@app.route('/get_plot', methods = ['GET', 'POST'])
def get_plot():
    if request.method == "POST":
        plant_hashmap = get_upper_plant_hashmap()
        plant_name_plot = request.form['plant_name_plot']
        plant_name = plant_name_plot
        plant_name_plot = plant_name_plot.upper()
        start_date_plot = request.form['start_date_plot']
        end_date_plot = request.form['end_date_plot']
        start_date_plot = datetime.strptime(start_date_plot, '%m/%d/%Y')
        end_date_plot = datetime.strptime(end_date_plot, '%m/%d/%Y')
        simp_plant_name = "plant_" + str(plant_hashmap[plant_name_plot])
        temp_string = "SELECT DateTime, " + simp_plant_name + " FROM historian_data;"
        conn = mysql.connector.connect(
        host = secrets.get('HOST') ,
        user = secrets.get('DATABASE_USER') ,
        password = secrets.get('DATABASE_PASSWORD') ,
        database = secrets.get('DATABASE_NAME')
        )
        mycursor = conn.cursor()
        mycursor.execute(temp_string)
        conn.commit
        y_values_from_database = mycursor.fetchall()
        datelist = []
        power_list = []
        flag = 0
        for rows in y_values_from_database:
            for i, value in enumerate(rows):
                if i == 0:
                    current_date = datetime.strptime(value, '%m/%d/%Y')
                    if end_date_plot >= current_date >= start_date_plot:
                        datelist.append(current_date)
                        flag = 1
                else:
                    if flag == 1:
                        power_list.append(int(value))
                        flag = 0

        x_axis = datelist
        y_axis = power_list
        plt.plot( x_axis, y_axis, '-' )
        plt.title(plant_name + " Power Plot")
        plt.gcf().autofmt_xdate(rotation=25)
        plt.grid()
        plt.xlabel("Dates")
        plt.ylabel("Power (%)")
        plt.ylim(0, 110)
        plt.xlim(datelist[0], datelist[len(datelist)-1])
        plt.savefig('/home/ultrallama7/flask/static/plot.png')
        plt.clf()

        start_date = start_date_plot.strftime("%m/%d/%Y")
        end_date = end_date_plot.strftime("%m/%d/%Y")

        return render_template('get_plot.html', plant_name = plant_name, start_date = start_date, end_date = end_date, plot_url="/static/plot.png")
    else:
        return render_template('get_plot.html')


@app.route('/plant_database')
def plant_database():
    conn = mysql.connector.connect(
    host = secrets.get('HOST') ,
    user = secrets.get('DATABASE_USER') ,
    password = secrets.get('DATABASE_PASSWORD') ,
    database = secrets.get('DATABASE_NAME')
    )

    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM plant_info_all")
    table_results = mycursor.fetchall()
    conn.commit()
    return render_template('full_database_list.html', table_results = table_results)


@app.route('/specific_plant', methods = ['GET'])
def specific_plant():
    if request.method == "GET":
        plant_hashmap = get_plant_hashmap()
        plant_name = request.args['name']
        plant_number = plant_hashmap[plant_name]
        plant_query = "plant_" + str(plant_number)
        power = request.args['power']
        stability = request.args['stab']
        conn = mysql.connector.connect(
        host = secrets.get('HOST') ,
        user = secrets.get('DATABASE_USER') ,
        password = secrets.get('DATABASE_PASSWORD') ,
        database = secrets.get('DATABASE_NAME')
        )
        mycursor = conn.cursor()
        request_string = "SELECT * FROM plant_info_all WHERE all_plant_name='" + plant_name + "'"
        mycursor.execute(request_string)
        table_results = mycursor.fetchall()
        conn.commit()

        request_string = "SELECT DateTime, " + plant_query + " FROM historian_data ORDER BY id DESC LIMIT 1095;"
        mycursor = conn.cursor()
        mycursor.execute(request_string)
        power_data_results = mycursor.fetchall()
        conn.commit()

        datelist = []
        power_list = []
        for rows in power_data_results:
            for i, value in enumerate(rows):
                if i == 0:
                    current_date = datetime.strptime(value, '%m/%d/%Y')
                    datelist.append(current_date)
                else:
                    power_list.append(int(value))

        x_axis = datelist[0:60]
        y_axis = power_list[0:60]
        plt.plot( x_axis, y_axis, '-' )
        plt.title(plant_name + " Power: Last Two Months of Data")
        plt.gcf().autofmt_xdate(rotation=25)
        plt.grid()
        plt.xlabel("Dates")
        plt.ylabel("Power (%)")
        plt.ylim(0, 110)
        plt.xlim(datelist[59], datelist[0])
        plt.savefig('/home/ultrallama7/flask/static/two_month.png')
        plt.clf()

        x_axis = datelist[0:365]
        y_axis = power_list[0:365]
        plt.plot( x_axis, y_axis, '-' )
        plt.title(plant_name + " Power: Last Year of Data")
        plt.gcf().autofmt_xdate(rotation=25)
        plt.grid()
        plt.xlabel("Dates")
        plt.ylabel("Power (%)")
        plt.ylim(0, 110)
        plt.xlim(datelist[364], datelist[0])
        plt.savefig('/home/ultrallama7/flask/static/one_year.png')
        plt.clf()

        x_axis = datelist[0:730]
        y_axis = power_list[0:730]
        plt.plot( x_axis, y_axis, '-' )
        plt.title(plant_name + " Power: Last Two Years of Data")
        plt.gcf().autofmt_xdate(rotation=25)
        plt.grid()
        plt.xlabel("Dates")
        plt.ylabel("Power (%)")
        plt.ylim(0, 110)
        plt.xlim(datelist[729], datelist[0])
        plt.savefig('/home/ultrallama7/flask/static/two_year.png')
        plt.clf()

        # % Capacity
        perc_capacity = np.mean(power_list)
        perc_capacity = np.round(perc_capacity, 2)

        # Last Outage Estimate
        for i, powers in enumerate(power_list):
            if np.sum(power_list[i:(i+10)]) == 0:
                temp_date = datelist[i]
                outage_distance = table_results[0][7]
                outage_date = temp_date.strftime("%m/%d/%Y")
                temp_date_2 = temp_date + relativedelta(months=+int(outage_distance)) - relativedelta(days=+20)
                next_outage_date = temp_date_2.strftime("%m/%d/%Y")
                break

        return render_template('specific_plant.html', plant_name = plant_name, power = power, stability = stability, table_results = table_results, perc_capacity = perc_capacity, outage_date = outage_date, next_outage_date = next_outage_date, plot_url1="/static/two_month.png", plot_url2="/static/one_year.png", plot_url3="/static/two_year.png")
    else:
        return render_template('specific_plant.html')



if __name__ == "__main__":
    app.run()



