from flask import Flask, render_template, request, redirect, url_for, session, abort, Response
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import json
import psutil

app = Flask(__name__)


# ====== SIMPLE APP CONFIG ======

is_maintenance_mode = True

# ===============================





# ------- API CONFIG --------


app.secret_key = 'cn9m89tyy3b789vryn0v9gybhm98vyc097tng'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'lucya'

# Intialize MySQL
mysql = MySQL(app)


# ----------------------------

# ===== SERVER SCRIPTS INCLUDES

import server_scripts.database_lib as dbhandlerlib
import server_scripts.web_api

# ===== MAIN INCLUDE END





# =================== MAIN WEBSITE ROUTES ===================


# General checks
@app.before_request
def general_check():
    loadtime = psutil.getloadavg()[0] + psutil.getloadavg()[1] + psutil.getloadavg()[2]

    if loadtime > 3:
        return render_template("Error/maintenance.html"), 503

    if is_maintenance_mode: 
        return render_template("Error/maintenance.html"), 503
    


@app.route('/home')
def homepage():
    if 'loggedin' in session:
        return render_template("Home.html", username=session['username'], userid=session['id'])
    
    return redirect(url_for('login'))

@app.route('/users/<userid>/profile')
def userprofile(userid):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (userid,))
        # Fetch one record and return result
        account = cursor.fetchone()
        
        if account:
            return render_template("User/profile.html", username=session['username'], userid=session['id'], profilename=account['username'], profileid=account['id'], profilefollowers=account['followers'], profilefollowing=account['following'], profilejoindate=account['created'])
        else:
            abort(404)
    
    return redirect(url_for('login'))


@app.route('/catalog/<itemid>/')
def itempage(itemid):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM items WHERE id = %s', (itemid,))
        # Fetch one record and return result
        item = cursor.fetchone()
        
        if item:
            return render_template("new/catalogitem.html", username=session['username'], userbalance=session['balance'], userid=session['id'], itemid=item['id'], itemname=item['itemname'], itemtype=item['type'], itemprice=item['price'], itemdesc=item['itemdesc'], thumburl="/static/funny_blob.png", itemfav=item['favs'])
        else:
            abort(404)
    
    return redirect(url_for('login'))


@app.route('/catalog')
def catalog():
    if 'loggedin' in session:
        return render_template("new/catalog.html", username=session['username'], userid=session['id'])
    
    return redirect(url_for('login'))

@app.route('/users/friends')
def user_friends():
    if 'loggedin' in session:
        return render_template("User/friends.html", username=session['username'], userid=session['id'])
    
    return redirect(url_for('login'))

@app.route('/my/messages/')
def user_messages():
    if 'loggedin' in session:
        return render_template("User/messages.html", username=session['username'], userid=session['id'])
    
    return redirect(url_for('login'))

@app.route('/trades')
def user_trades():
    if 'loggedin' in session:
        return render_template("User/trades.html", username=session['username'], userid=session['id'])
    
    return redirect(url_for('login'))

@app.route('/discover')
def games():
    if 'loggedin' in session:
        return render_template("new/games.html", username=session['username'], userid=session['id'])
    
    return redirect(url_for('login'))

@app.route('/develop')
@app.route('/create')
def createpage():
    if 'loggedin' in session:
        return render_template("user/create.html", username=session['username'], userid=session['id'])
    
    return redirect(url_for('login'))

@app.route('/upgrades')
@app.route('/robux')
def robuxpage():
    if 'loggedin' in session:
        return render_template("market/robux.html", username=session['username'], userid=session['id'])
    
    return redirect(url_for('login'))

@app.route('/premium/membership')
def premiumpage():
    if 'loggedin' in session:
        return render_template("market/premium.html", username=session['username'], userid=session['id'])
    
    return redirect(url_for('login'))

@app.route('/my/avatar')
def avatar():
    if 'loggedin' in session:
        return render_template("User/avatar.html", username=session['username'], userid=session['id'])
    
    return redirect(url_for('login'))

@app.route('/transactions')
def moneypage():
    if 'loggedin' in session:
        return render_template("User/money.html", username=session['username'], userid=session['id'])
    
    return redirect(url_for('login'))

@app.route('/my/groups')
@app.route('/search/groups')
def groups():
    if 'loggedin' in session:
        return render_template("new/groups.html", username=session['username'], userid=session['id'])
    
    return redirect(url_for('login'))
# =========================================================









# =================== AUTH ROUTES ===================

@app.route('/')
@app.route('/account/signupredir')
def singup():
    if 'loggedin' in session:
            return redirect(url_for('homepage'))

    return render_template("new/signup.html")

@app.route('/api/v1/auth/v2/signup', methods=['POST'])
def signupapi():
    if 'loggedin' in session:
            return redirect(url_for('homepage'))

    parsedata = json.loads(request.data)
    
    try:
        username = parsedata["username"]
        password = parsedata["password"]
        gender = parsedata["gender"]
        birthday = parsedata["birthday"]
    except:
        return '{"errors":[{"code":1,"message":"Please fill out the form!"}]}'
    
    username = str(parsedata["username"])
    password = str(parsedata["password"])
    gender = str(parsedata["gender"])
    birthday = str(parsedata["birthday"])
    
    birthday = birthday.replace(" ", "")
    
    checkacc = dbhandlerlib.check_existing_account_by_name(username)
    
    if checkacc:
        return '{"errors":[{"code":1,"message":"Username is already in use!"}]}'
    elif not re.match(r'[A-Za-z0-9]+', birthday):
        return '{"errors":[{"code":1,"message":"Invalid birthday!"}]}'
    elif not re.match(r'[A-Za-z0-9]+', username):
        return '{"errors":[{"code":1,"message":"Invalid username!"}]}'
    else:
        dbhandlerlib.create_account(username, password, "Undefined", gender, birthday)
        return '[]'


@app.route('/api/v1/auth/v2/login', methods=['POST'])
def loginapi():
    if 'loggedin' in session:
            return redirect(url_for('homepage'))

    parsedata = json.loads(request.data)
    
    try:
        username = parsedata["cvalue"]
        password = parsedata["password"]
    except:
        return '{"errors":[{"code":1,"message":"Please fill out the form!"}]}'
    
    username = str(parsedata["cvalue"])
    password = str(parsedata["password"])
    
    checkacc = dbhandlerlib.check_account_login(username, password)
    
    if not checkacc:
        return Response('{"errors":[{"code":1,"message":"Incorrect username or password. Please try again.","userFacingMessage":"Something went wrong"}]}', status=403, mimetype='application/json')
    else:
        logindata = dbhandlerlib.get_account_login_data(username)
        
        # Create session data, we can access this data in other routes
        session['loggedin'] = True
        session['balance'] = logindata[2]
        session['id'] = logindata[1]
        session['username'] = logindata[0]
        
        return "[]"
    

@app.route('/login')
def loginpage():
    if 'loggedin' in session:
            return redirect(url_for('homepage'))

    return render_template("new/login.html")

@app.route('/login/old', methods=['GET', 'POST'])
def login():
    return redirect(url_for('loginpage'))

    if 'loggedin' in session:
        return redirect(url_for('homepage'))

    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('homepage'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('hidden/login.html', msg=msg)

@app.route('/register/old', methods=['GET', 'POST'])
def oldregister():
    return "depricated."

    if 'loggedin' in session:
        return redirect(url_for('homepage'))

    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            #cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, NULL)', (username, password, email, 0, 15, "Yeah...", 0, 0))
            #mysql.connection.commit()
            dbhandlerlib.create_account(username, password, email)
            msg = 'You have successfully registered!'
            return redirect(url_for('login'))
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('hidden/register.html', msg=msg)


# =================== =================== ===================



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)