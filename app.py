# Import flask and its componests
from flask import *

# import the pymysql module : it helps us crate connections btw python and mysql database
import pymysql

#create a flask application and give it a name
app = Flask(__name__)

# below is a signup route
@app.route("/api/signup", methods = ["POST"])
def signup():
    if request.method=="POST":
        # Exract the different details entered on the form
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        phone = request.form["phone"]

        # by use of the print function lets print all those details sent with the upcoming request
        #print(username, email, password, phone)

        #establish a connection between flask/python and mysql
        connection = pymysql.connect(host="localhost", user="root", password="", database="sokogardenonline")

        #create a cursor to execute the sql queries
        cursor = connection.cursor()

        # structure an sql to insert the details received from  the form
        # The %s is a placeholder ->actual values (prevents SQL injection)
        sql = "INSERT INTO users(username,email,phone,password) VALUES(%s, %s, %s, %s)"

        #create a tuple that will hold all the data gotten from the form
        data =(username, email, phone, password)

        # by the use of cursor execute the sql as you replace the placeholder with the actual values
        cursor.execute(sql, data)

        # commit the changes to the database
        connection.commit()


        return jsonify({"message" : "user registered successfully."})

# Below is the login/sign in route
@app.route("/api/signin", methods=["POST"])
def signin():
    if request.method == "POST":
        # Extract the two details entered on the form
        email = request.form["email"]
        password = request.form["password"]

        #print out the details entered
        #print(email,password)

        #create / establish a connection to the database
        connection = pymysql.connect(host="localhost", user="root", password="", database="sokogardenonline" )

        #create a cursor
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        # structure the sql query that will check whether the email or password entered are corrct
        sql="SELECT * FROM users WHERE email = %s AND password = %s"

        # put the data received from the form into a tuple
        data = (email,password)

        # by use of the cursor execute the sql
        cursor.execute(sql,data)

        #check whether there are rows returned and store on a variable
        count = cursor.rowcount


        # if there are records returned it means the password and the email are correct otherwise it means they are vwrong\
        if count == 0:
            return jsonify({"message" : "Login Failed"})
        else:
            # there must be a user so we create a variable that will hold the details of the user fetched from the database
    
            user=cursor.fetchone()
            # return the details to the frontend as well as a message
            return jsonify({"message" : " User Logged in successfully", "user":user})



       


# run the application
app.run(debug=True)