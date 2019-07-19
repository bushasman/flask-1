from flask import Flask, render_template, request, redirect,url_for

import pprint
from flask import  flash
app = Flask(__name__)
import psycopg2 as pg2
from pprint import pprint
import db
connect = pg2.connect(database=db.db, user=db.user, password=db.password)
cur = connect.cursor()
connect.autocommit=True
pprint("connected succesfuly")
@app.route('/')
def home():
   return render_template('new_flask.html')

"""this url presents a form for the user to save data into the company database"""

@app.route('/',methods = ['POST'])
def enter_data():
    if request.method=='POST':
        data=request.form
        car_type=data['car_type']
        make=data['make']
        reg=data['vehicle_reg_no']
        driver_name=data['driver_name']
        driver_contact=data['driver_contact']
        year=data['year_of_make']
        license=data['driver_license_no']
        cur.execute("insert into car_data (car_type,make,vehicle_reg_no,driver_name,driver_contact,year_of_make,driver_license_no)VALUES('"+car_type+"','"+make+"','"+reg+"','"+driver_name+"','"+driver_contact+"','"+year+"','"+license+"')")
        connect.commit()


    return render_template('new_flask.html')


""""this url allows the user to search for the particular details of a certain driver"""

@app.route('/emp')
def moir():
    return render_template('trial.html')
@app.route('/emp',methods = ['POST'])
def search():
    data = request.form
    driver_name = data['driver_name']
    sql_update_query = "SELECT * FROM car_data where driver_name = '" + driver_name + "'"
    cur.execute(sql_update_query, (driver_name))
    car_records = cur.fetchall()
    print(car_records)
    return render_template('results.html', car_records=car_records)

@app.route('/emporium',methods = ['GET','POST'])
def search_data():
    if request.method == 'POST':
            data = request.form
            driver_name=data['driver_name']
            sql_update_query = "SELECT * FROM car_trips where driver_name = '"+driver_name+"'"
            cur.execute(sql_update_query,(driver_name))
            car_record = cur.fetchall()
            return render_template('results2.html', car_record=car_record ,)

    else:
        return render_template('search.html')

#this is where the driver can rent a car

@app.route('/driver_login',methods=['GET','POST'])
def jobs():
    if request.method == 'POST':
        data = request.form
        days = (data['day'])
        driver_name = data['driver_name']
        cas=((int(days))*1500)
        cash=str(cas)
        sql_update_query = "SELECT * FROM car_data where driver_name = '" + driver_name + "'"
        cur.execute(sql_update_query, (driver_name))
        car_records = cur.fetchall()
        sql_update_query = "SELECT * FROM car_trips where driver_name = '" + driver_name + "'"
        cur.execute(sql_update_query, (driver_name))
        car_record = cur.fetchall()
        for car in car_records:
            q=car[2]

        print(cash)
        print(driver_name)


        cur.execute("insert into car_trips(ammount_racked,driver_name,car_registration_number)VALUES('"+cash+"','"+driver_name+"','"+q+"')")
        return render_template('driver_login2.html',cash=cash,days=days)
    else:
        return render_template('driver_login.html')

if __name__ == '__main__':
   app.run(debug = True)