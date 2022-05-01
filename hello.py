from asyncio.windows_events import NULL
from pickle import TRUE
from unicodedata import name
from flask import jsonify
from flask import Flask, request
from flask_mysqldb import MySQL

# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'Dhanush'
app.config['MYSQL_PASSWORD'] = 'ttpod123'
app.config['MYSQL_DB'] = 'mysql'
mysql = MySQL(app)

@app.route('/instituteform')
def form():
    return """<form action="/ilogin" method = "POST">
   <p>School name <input type = "text" name = "name" /></p>
   <p>School code<input type = "integer" name = "age" /></p>
   <p><input type = "submit" value = "Submit" /></p>
</form>"""

@app.route('/studentform')
def sform():
    return """<form action="/slogin" method = "POST">
   <p>Student name <input type = "text" name = "name" /></p>
   <p>student roll no<input type = "text" name = "age" /></p>
   <p>school name <input type = "text" name = "sname" /></p>
   <p><input type = "submit" value = "Submit" /></p>
</form>"""

@app.route('/slogin', methods = ['POST', 'GET'])
def slogin():
    if request.method == 'GET':
        return "Login via the login Form"
     
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        sname = request.form['sname']
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO student VALUES(%s,%s,%s)''',(age,name,sname))
        mysql.connection.commit()
        cursor.close()
        return f"Done!!"

@app.route('/ilogin', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return "Login via the login Form"
     
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO institute VALUES(%s,%s)''',(age,name))
        mysql.connection.commit()
        cursor.close()
        return f"Done!!"

@app.route('/rating/<rno>/<icode>/<dish>/<stars>',methods = ['POST', 'GET'])
def rating(rno,icode,dish,stars):
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO rating VALUES(%s,%s,%s,%s)''',(rno,icode,dish,stars))
        mysql.connection.commit()
        cursor.close()
        return f"Done!!"

@app.route('/')
def json():
    return jsonify("home")

@app.route('/schoolsearch/<age>',methods = ['POST', 'GET'])
def result(age):
        cursor = mysql.connection.cursor()
        sql = "SELECT SchoolName FROM institute WHERE InstituteCode = {}".format(age)
        cursor.execute(sql)
        result=cursor.fetchone() 
        mysql.connection.commit()
        cursor.close()
        str='{}'.format(result)
        if str=='None':
            return jsonify(False)
        else:
            return jsonify(SchoolName = "{}".format(result))

@app.route('/studentsearch/<age>/<name>',methods = ['POST', 'GET'])
def resul(age,name):
        cursor = mysql.connection.cursor()
        sql = "SELECT StudentName FROM student WHERE rollno = '{0}' AND SchoolName = '{1}'".format(age,name)
        cursor.execute(sql)
        result=cursor.fetchone() 
        mysql.connection.commit()
        cursor.close() 

        return jsonify("{}".format(result))

 
app.run(host='0.0.0.0', port=5000,debug=False)