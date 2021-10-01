from flask import Flask, render_template, request, redirect, url_for, session
from flaskext.mysql import MySQL
import re 

app = Flask(__name__)

# Enter your database connection details below
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'employees'

# Intialize MySQL
mysql = MySQL()
mysql.init_app(app)

# http://localhost:5000/index/ - this will be the home page, we need to use both GET and POST requests
@app.route('/index/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
# http://localhost:5000/add/ - this will be the login page, we need to use both GET and POST requests
@app.route('/add/', methods=['GET', 'POST'])
def add():
    # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'designation' in request.form and 'phone' in request.form and 'address' in request.form and 'hiredate' in request.form and 'salary' in request.form and 'managerId' in request.form and 'email' in request.form:
        # Create variables for easy access
        name = request.form['name']
        designation= request.form['designation']
        phone= request.form['phone']
        address= request.form['address']
        hiredate= request.form['hiredate']
        salary= request.form['salary']
        managerId= request.form['managerId']
        email = request.form['email']
        # Check if employee exists using MySQL
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM employees WHERE email = %s OR phone = %s', (email,phone))
        employee = cursor.fetchone()
        # If employee exists show error and validation checks
        if employee:
            msg = 'Record already exists for given email/phone!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not name or not email or not designation or not phone or not address or not hiredate or not salary or not managerId:
            msg = 'Please fill out the form!'
        else:
            # Record doesnt exists and the form data is valid, now insert new record into employees table
            cursor.execute('INSERT INTO employees VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)', (name, email, designation, address, int(salary), int(managerId), int(phone), hiredate))
            mysql.get_db().commit()
            msg = 'You have successfully inserted the record!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show employee add form with message (if any)
    return render_template('add.html', msg=msg)

# http://localhost:5000/delete/ - this will be the delete employee page, we need to use both GET and POST requests
@app.route('/delete/', methods=['GET', 'POST'])
def delete():
    # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST' and 'empid' in request.form:
        # Create variables for easy access
        empid = request.form['empid']
        
        # Check if employee exists using MySQL
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM employees WHERE id = %s', (empid))
        employee = cursor.fetchone()
        # If employee exists show error and validation checks
        if employee:
            # employee doesnt exists and the form data is valid, now insert new employee into employees table
            cursor.execute('DELETE FROM employees WHERE id = %s',(empid))
            mysql.get_db().commit()
            msg = 'You have successfully Deleted one record!'
        elif not empid:
            msg = 'Please fill out the valid empid!'
        else:
            msg = 'No employee exists in given empid'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the field!'
    # Show registration form with message (if any)
    return render_template('delete.html', msg=msg)
    
# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests
@app.route('/search/', methods=['GET', 'POST'])
def search():
    # Output message if something goes wrong...
    msg = ''
    data=''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'srch' in request.form:
        # Create variables for easy access
        srch = request.form['srch']
        
        # Check if employee exists using MySQL
        cursor = mysql.get_db().cursor()
        employee = cursor.execute('SELECT * FROM employees WHERE name = %s OR address = %s OR phone = %s', (srch,srch,srch))
        # If employee exists show error and validation checks
        if employee:
            # employee doesnt exists and the form data is valid, now insert new employee into employees table
            header = [i[0] for i in cursor.description]
            data = [list(i) for i in cursor.fetchall()]
            data.insert(0,header)
            msg = 'Successfully fetched Data !'
        elif not srch:
            msg = 'Please fill out the field!'
        else:
            msg = 'No employees exits for the given keyword'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the field!'
    #return data
    return render_template("search.html", data=data,msg=msg)

# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests
@app.route('/show/', methods=['GET', 'POST'])
def show():
    cursor = mysql.get_db().cursor()
    employee = cursor.execute('SELECT * FROM employees')
    data=''
    msg=''
    if employee:
        header = [i[0] for i in cursor.description]
        data = [list(i) for i in cursor.fetchall()]
        data.insert(0,header)
        msg= 'Sucessfully fetched records'
    else:
         msg = 'No employee records'
    #data = cursor.fetchall()
    #return data
    return render_template("show.html", data=data,msg=msg)

if __name__ == "__main__":
    app.run()