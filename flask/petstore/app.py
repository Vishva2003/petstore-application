import os
import re
import ibm_db
from flask import Flask, session, render_template, request, redirect, send_from_directory, url_for
import ibm_boto3
from ibm_botocore.client import Config, ClientError
import requests
# from helpers import login_required

app=Flask(__name__)
app.secret_key = os.urandom(24)
conn =ibm_db.connect("DATABASE=bludb;HOSTNAME=824dfd4d-99de-440d-9991-629c01b3832d.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30119;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=yfh72182;PWD=DwWAownlgevsMym5", " "," ")
print("connected")

#Routing to the home page

@app.route("/")
def home():
    return render_template("pethome.html")

#Routing the User login page


@app.route("/userlogin")
def userlogin():
    return render_template("userlogin.html")

@app.route('/login1', methods=['GET', 'POST'])
def login1():
    msg =""
    if request.method =='POST':
        USERNAME = request.form['username']
        PASSWORD=request.form['password']
        sql = "SELECT * FROM USER1 WHERE USERNAME=? AND PASSWORD=?"
        stmt=ibm_db.prepare (conn, sql)
        ibm_db.bind_param(stmt, 1, USERNAME)
        ibm_db.bind_param(stmt, 2, PASSWORD)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print (account)
        if account:
            session ["USERNAME"] = account ["USERNAME"]
            session ['USERID'] = account [ 'USERID']
            msg = 'Logged in successfully !'
            return redirect(url_for('product'))
        else:
            msg='Incorrect username/password !'
            return render_template('userlogin.html')
        
    return render_template('userlogin.html', msg=msg)

#Routing to the admin Login page
@app.route("/adminlogin")
def adminlogin():
    return render_template("adminlogin.html")

@app.route("/adminlogin1", methods=["GET", "POST"])
def admin_login1():
    if request.method=="POST":
        # session.clear()
        USERNAME = request.form.get("username")
        PASSWORD= request.form.get("password")
        sql="SELECT * FROM USER1 WHERE USERNAME=? AND PASSWORD=?" 
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, USERNAME)
        ibm_db.bind_param(stmt, 2, PASSWORD)
        ibm_db.execute(stmt) 
        result = ibm_db.fetch_assoc(stmt)
        print(result)
        if result:
            session ['Loggedin']=True
            session ["USERID"]=result['USERID']
            Userid =result['USERNAME']
            session ['USERNAME']=result['USERNAME']
            msg="logged in successfully !"
            return redirect(url_for('product'))
        else:
            msg="Incorrect username/password!"
            return render_template('adminlogin.html', msg=msg)
    return render_template('adminlogin.html')

#Routing to the merchant Login page

@app.route("/merchantlogin")
def merchantlogin():
    return render_template("merchantlogin.html")

@app.route("merchantlogin1", methods=["GET", "POST"])
def merchantlogin1():
    if request.method=="POST":
        # session.clear()
        USERNAME = request.form.get("username")
        PASSWORD= request.form.get("password")
        sql="SELECT * FROM USER1 WHERE USERNAME=? AND PASSWORD=?" 
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, USERNAME)
        ibm_db.bind_param(stmt, 2, PASSWORD)
        ibm_db.execute(stmt) 
        result = ibm_db.fetch_assoc(stmt)
        print(result)
        if result:
            session ['Loggedin']=True
            session ["USERID"]=result['USERID']
            Userid =result['USERNAME']
            session ['USERNAME']=result['USERNAME']
            msg="logged in successfully !"
            return redirect(url_for('product'))
        else:
            msg="Incorrect username/password!"
            return render_template('merchantlogin.html', msg=msg)
        
    return render_template('merchantlogin.html')
#Routing to user register page
@app.route("/userreg")
def userreg():
    return render_template("userreg.html")

@app.route('/userreg1', methods=['GET', 'POST'])
def userreg1(): 
    msg = ""
    if request.method=='POST':
        USERNAME = request.form["username"] 
        PASSWORD= request.form["password"]
        EMAIL = request.form["email"]
        ROLE=0
        sql = "SELECT* FROM USER1 WHERE USERNAME= ? AND PASSWORD=?" 
        stmt = ibm_db.prepare (conn, sql)
        ibm_db.bind_param(stmt, 1, USERNAME)
        ibm_db.bind_param(stmt, 2, PASSWORD)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print (account)
        if account:
            msg = 'Account already exists !' 
        elif not re.match(r'[^@]+@ [^@]+\ . [^@]+', EMAIL):
            msg = 'Invalid email address !' 
        elif not re.match(r'[A-Za-z0-9]+', USERNAME):
            msg = 'Username must contain only characters and numbers !'
        elif not USERNAME or not PASSWORD or not EMAIL:
            msg = 'Please fill out the form !'
        else:
            sql2 = "SELECT count(*) FROM USER1" 
            stmt2 =ibm_db.prepare (conn, sql2)
            ibm_db.execute(stmt2) 
            length = ibm_db.fetch_assoc(stmt2) 
            print (length)
            sql = "INSERT INTO USER1 VALUES (?, ?, ?, ?, ?)"
            stmt=ibm_db.prepare (conn, sql)
            ibm_db.bind_param(stmt, 1, USERNAME)
            ibm_db.bind_param(stmt, 2, EMAIL)
            ibm_db.bind_param(stmt, 3, PASSWORD) 
            ibm_db.bind_param(stmt, 4, length['1']+1)
            ibm_db.bind_param(stmt, 5, ROLE)
            ibm_db.execute(stmt)
            
        return render_template('userreg.html', msg=msg)        
    
       
#Routing to admin register page

@app.route("/adminreg")
def adminreg():
    return render_template("adminreg.html")

@app.route("/adminreg1", methods=["GET", "POST"])
def adminreg1():
    msg =""
    if request.method =="POST":
        # session.clear()
        USERNAME = request.form.get("username")
        EMAIL=request.form.get("email")
        PASSWORD = request.form.get("password")
        ROLE=1
        # password = request.form.get("password")
        sql = "SELECT * FROM USER1 WHERE USERNAME=? AND PASSWORD=?"
        stmt = ibm_db.prepare (conn, sql)
        ibm_db.bind_param(stmt, 1, USERNAME) 
        ibm_db.bind_param(stmt, 2, PASSWORD)
        ibm_db.execute(stmt)
        data = ibm_db.fetch_assoc(stmt) 
        if data:
            return render_template("adminreg.html", message="Username already exists!")
        else:
            sql2 = "SELECT count(*) FROM USER1"
            stmt2=ibm_db.prepare (conn, sql2)
            ibm_db.execute(stmt2) 
            length=ibm_db.fetch_assoc(stmt2)
            print (length)
            sql="INSERT INTO USER1 VALUES (?, ?, ?, ?, ?)"
            stmt = ibm_db.prepare (conn, sql)
            ibm_db.bind_param(stmt, 1, USERNAME)
            ibm_db.bind_param(stmt, 2, EMAIL)
            ibm_db.bind_param(stmt, 3, PASSWORD)
            ibm_db.bind_param(stmt, 4, length['1']+1)
            ibm_db.bind_param(stmt, 5, ROLE)
    else :
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('adminreg.html', msg=msg)       
            
#Routing to Logout page

@app.route("/logout") 
def admin_logout():
    session.clear() 
    return redirect("/")

#Routing to user home page after login

@app.route("/product")
def product():
    return render_template("product.html")

#Routing to upload after login

@app.route("/pets")
def pets():
    return render_template("pets.html")

@app.route("/pets1", methods=["GET", "POST"], endpoint='home')
def pets1():
    if request.method =="POST":
        f = request.files['image'] 
        PROID = request.form.get("proid")
        CATOGERY = request.form.get("category")
        SUB_CATOGERY = request.form.get("Sub-category")
        DESCRIPTION = request.form.get("description")
        PRICE_RANGE = request.form.get("price_range")
        COMMENTS = request.form.get("comments")
        
        # Constants for IBM COS values
        COS_ENDPOINT = "https://s3.us-south.cloud-object-storage.appdomain.cloud"
        COS_API_KEY_ID = "PKJi4GNB6i5fbHrtuPol7rMrfCDkiargXENYo9Gh67Ee"
        COS_INSTANCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/7583e14b8ab848698452224c4d7b8671:94a47c1d-7d48-4a73-b87d-985f5b18ead5::"
        # Create resource
        cos=ibm_boto3.client("s3",
            ibm_api_key_id=COS_API_KEY_ID,
            ibm_service_instance_id=COS_INSTANCE_CRN,
            config=Config(signature_version="oauth"),
            endpoint_url=COS_ENDPOINT
        )
        Cos.upload_file(Filename="filepath",Bucket="vishva",Key="useruplads")
        
        # current user = session ["USERNAME"]
        sql= "SELECT * FROM USER1 WHERE USERID="+str(session ['USERID'])
        stmt=ibm_db.prepare (conn, sql)
        ibm_db.execute(stmt)
        data=ibm_db.fetch_tuple (stmt)
        print (data)
        
        insert_sql = "INSERT INTO PETS VALUES (?,?,?,?,?, ?, ?, ?) "
        stmt1 = ibm_db.prepare (conn, insert_sql)
        ibm_db.bind_param(stmt1, 1, data[3]) 
        ibm_db.bind_param(stmt1, 2, PROID)
        ibm_db.bind_param(stmt1, 3, data[0])
        ibm_db.bind_param(stmt1, 4, CATOGERY) 
        ibm_db.bind_param(stmt1, 5, SUB_CATOGERY)
        ibm_db.bind_param(stmt1, 6, DESCRIPTION) 
        ibm_db.bind_param(stmt1, 7, PRICE_RANGE)
        ibm_db.bind_param(stmt1, 8, COMMENTS)
        ibm_db.execute(stmt1)
        print("valuessent")
    
        sql = 'SELECT * FROM PETS'
        stmt2 =ibm_db.prepare (conn, sql)
        ibm_db.execute(stmt2)
        data = ibm_db.fetch_assoc(stmt2)
        print (data)
        print("Latest product id:", data)
        
    return render_template("pets.html")

#Routing to about page

@app.route("/about")
def about():
    return render_template("about.html")

#Routing to contact page
@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/contact1", methods=["GET", "POST"])
def contact1():
    msg =""
    if request.method =="POST":
        # session.clear()
        USERNAME = request.form.get("username")
        EMAIL=request.form.get("email")
        MESSAGE = request.form.get("password")
        ROLE=1
        # password = request.form.get("password")
        sql = "SELECT * FROM USER1 WHERE USERNAME=? AND PASSWORD=?"
        stmt = ibm_db.prepare (conn, sql)
        ibm_db.bind_param(stmt, 1, USERNAME) 
        ibm_db.bind_param(stmt, 2, PASSWORD)
        ibm_db.execute(stmt)
        data = ibm_db.fetch_assoc(stmt) 
        
        sql="INSERT INTO POST VALUES (?, ?, ?, ?, ?)"
        stmt = ibm_db.prepare (conn, sql)
        ibm_db.bind_param(stmt, 1, USERNAME)
        ibm_db.bind_param(stmt, 2, EMAIL)
        ibm_db.bind_param(stmt, 3, PASSWORD)
        ibm_db.bind_param(stmt, 4, length['1']+1)
        ibm_db.bind_param(stmt, 5, ROLE)
    else :
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('contact.html', msg=msg) 
        
if __name__=="__main__":
    app.run(debug=True)