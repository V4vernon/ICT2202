from flask import Flask, render_template, request, redirect, url_for, session, make_response
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import MySQLdb.cursors, re, uuid, hashlib, datetime, os

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'T7fQFF3m5X'

# App Settings
app.config['threaded'] = True

# Database connection settings
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'forensic_blockchain'

# Email server settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ICT1002DigitalForensic@gmail.com'
app.config['MAIL_PASSWORD'] = 'M2-NrAd)Yws2g*qf'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# Domain name settings
app.config['DOMAIN'] = 'http://127.0.0.1:5000'

# Initialize MySQL & Mail
mysql = MySQL(app)
mail = Mail(app)

# Enable account activation & CSRF protection
account_activation_required = True
csrf_protection = False


# Login Page (http://localhost:5000/)
@app.route('/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'token' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        token = request.form['token']
        # Retrieve hashed password
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            if account_activation_required and ['activation_code'] != 'activated' and account['activation_code'] != '':
                msg = 'Please activate your account to login!'
            if csrf_protection and str(token) != str(session['token']):
                msg = 'Invalid token!'
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['role'] = account['role']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Generate random token that will prevent CSRF attacks
    token = uuid.uuid4()
    session['token'] = token
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg, token=token)


# Logout Page (http://localhost:5000/logout)
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('role', None)
    # Redirect to login page
    return redirect(url_for('login'))


# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'cpassword' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        cpassword = request.form['cpassword']
        email = request.form['email']
        # Hash the password
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        hashed_password = hash.hexdigest()
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
        elif not username or not password or not cpassword or not email:
            msg = 'Please fill out the form!'
        elif password != cpassword:
            msg = 'Passwords do not match!'
        elif len(username) < 5 or len(username) > 20:
            msg = 'Username must be between 5 and 20 characters long!'
        elif len(password) < 5 or len(password) > 20:
            msg = 'Password must be between 5 and 20 characters long!'
        elif account_activation_required:
            # Account activation enabled
            # Generate a random unique id for activation code
            activation_code = uuid.uuid4()
            cursor.execute('INSERT INTO accounts (username, password, email, activation_code) VALUES (%s, %s, %s, %s)',
                           (username, hashed_password, email, activation_code,))
            mysql.connection.commit()
            # Create Email message
            email_info = Message('Account Activation Required', sender=app.config['MAIL_USERNAME'],
                                 recipients=[email])
            activate_link = app.config['DOMAIN'] + url_for('activate', email=email, code=str(activation_code))
            # change the email body below
            email_info.body = 'Please click the following link to activate your account:' + str(activate_link)
            mail.send(email_info)
            msg = 'Please check your email to activate your account!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, "")', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


# Account Activation Page
@app.route('/activate/<string:email>/<string:code>', methods=['GET'])
def activate(email, code):
    # Check if the email and code provided exist in the accounts table
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE email = %s AND activation_code = %s', (email, code,))
    account = cursor.fetchone()
    if account:
        # account exists, update the activation code to "activated"
        cursor.execute('UPDATE accounts SET activation_code = "activated" WHERE email = %s AND activation_code = %s',
                       (email, code,))
        mysql.connection.commit()
        # automatically log the user in and redirect to the home page
        session['loggedin'] = True
        session['id'] = account['id']
        session['username'] = account['username']
        session['role'] = account['role']
        return redirect(url_for('home'))
    return 'Account doesn\'t exist with that email or incorrect activation code!'


# Dashboard Page
@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'], role=session['role'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# Profile Page
@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', role=session['role'], username=session['username'], account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# Edit_Profile Page
@app.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Output message
        msg = ''
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
            # Create variables for easy access
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            # Retrieve account by the username
            cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
            account = cursor.fetchone()
            # validation check
            if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            elif not username or not email:
                msg = 'Please fill out the form!'
            elif session['username'] != username and account:
                msg = 'Username already exists!'
            elif len(username) < 5 or len(username) > 20:
                msg = 'Username must be between 5 and 20 characters long!'
            elif len(password) < 5 or len(password) > 20:
                msg = 'Password must be between 5 and 20 characters long!'
            else:
                cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
                account = cursor.fetchone()
                current_password = account['password']
                if password:
                    # Hash the password
                    hash = password + app.secret_key
                    hash = hashlib.sha1(hash.encode())
                    current_password = hash.hexdigest();
                # update account with the new details
                cursor.execute('UPDATE accounts SET username = %s, password = %s, email = %s WHERE id = %s',
                               (username, current_password, email, session['id'],))
                mysql.connection.commit()
                msg = 'Updated!'
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile-edit.html', account=account, username=session['username'], role=session['role'],
                               msg=msg)
    return redirect(url_for('login'))


# Forget Password Page
@app.route('/forgotpassword', methods=['GET', 'POST'])
def forgotpassword():
    msg = ''
    if request.method == 'POST' and 'email' in request.form:
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = %s', (email,))
        account = cursor.fetchone()
        if account:
            # Generate unique ID
            reset_code = uuid.uuid4()
            # Update the reset column in the accounts table to reflect the generated ID
            cursor.execute('UPDATE accounts SET reset = %s WHERE email = %s', (reset_code, email,))
            mysql.connection.commit()
            # Change your_email@gmail.com
            email_info = Message('Password Reset', sender=app.config['MAIL_USERNAME'], recipients=[email])
            # Generate reset password link
            reset_link = app.config['DOMAIN'] + url_for('resetpassword', email=email, code=str(reset_code))
            # change the email body below
            email_info.body = 'Please click the following link to reset your password: ' + str(reset_link)
            email_info.html = '<p>Please click the following link to reset your password: <a href="' + str(
                reset_link) + '">' + str(reset_link) + '</a></p>'
            mail.send(email_info)
            msg = 'Reset password link has been sent to your email!'
        else:
            msg = 'An account with that email does not exist!'
    return render_template('forgotpassword.html', msg=msg)


@app.route('/resetpassword/<string:email>/<string:code>', methods=['GET', 'POST'])
def resetpassword(email, code):
    msg = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # Retrieve the account with the email and reset code provided from the GET request
    cursor.execute('SELECT * FROM accounts WHERE email = %s AND reset = %s', (email, code,))
    account = cursor.fetchone()
    # If account exists
    if account:
        # Check if the new password fields were submitted
        if request.method == 'POST' and 'npassword' in request.form and 'cpassword' in request.form:
            npassword = request.form['npassword']
            cpassword = request.form['cpassword']
            # Password fields must match
            if npassword == cpassword and npassword != "":
                # Hash new password
                hash = npassword + app.secret_key
                hash = hashlib.sha1(hash.encode())
                npassword = hash.hexdigest();
                # Update the user's password
                cursor.execute('UPDATE accounts SET password = %s, reset = "" WHERE email = %s', (npassword, email,))
                mysql.connection.commit()
                msg = 'Your password has been reset, you can now <a href="' + url_for('login') + '">login</a>!'
            else:
                msg = 'Passwords must match and must not be empty!'
        return render_template('resetpassword.html', msg=msg, email=email, code=code)
    return 'Invalid email and/or code!'


@app.route('/blank')
def blank():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('blank.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='404'), 404


if __name__ == '__main__':
    app.run(debug=True)
