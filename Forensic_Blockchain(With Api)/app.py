from flask import Flask, render_template, request, redirect, url_for, session, make_response, jsonify
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import MySQLdb.cursors, re, uuid, hashlib, datetime, os
from brownie import *
p = project.load("brownie", name="BrownieProject")
p.load_config()
from brownie.project.BrownieProject import *
from brownie.network import priority_fee, max_fee, web3
from brownie.convert import to_string
import json,asyncio,time,pytz,cv2,base64,os,hashlib
import numpy as np


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
app.config['DOMAIN'] = 'http://167.71.205.211:5000'

# Initialize MySQL & Mail
mysql = MySQL(app)
mail = Mail(app)

# Enable account activation & CSRF protection
account_activation_required = True
csrf_protection = False


# Connect to the blockchain network
network.connect("byteablock")

# Load the application binary interface (abi), required to get a deployed contract from the chain
rf = open("abi.json", "r")
abi = json.load(rf)
rf.close()

# Get the deployed contract from the chain as a brownie contract object
contract = Contract.from_abi("ByteABlock", "0x000e7cE22b6f63EA7E75408a61649F798538F05E", abi=abi)

# Get the deployed contract from the chain as a web3 contract object (required for using filters)
contract_w3 = web3.eth.contract(address="0x000e7cE22b6f63EA7E75408a61649F798538F05E", abi=abi)



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


# Reset PasswordPage
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


# Case Page
@app.route('/Case')
def Case():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT id FROM accounts  WHERE username = %s', (session['username'],))
        id = cursor.fetchone()
        cursor.execute('SELECT * FROM bitcase  WHERE account_id = %s', (id['id'],))
        case = cursor.fetchall()
        return render_template('case.html', username=session['username'], role=session['role'], case=case)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# Add Case Page
@app.route('/Case_Add', methods=['GET', 'POST'])
def Case_Add():
    # Output message if something goes wrong...
    msg = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT username FROM accounts')
    name = cursor.fetchall()
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'casename' in request.form and 'Assigned_To' in request.form \
            and 'Location' in request.form:
        # Create variables for easy access
        casename = request.form['casename']
        assigned = request.form['Assigned_To']
        cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor2.execute('SELECT id FROM accounts WHERE username = %s', (assigned,))
        account_id = cursor2.fetchone()
        mydate = request.form['Date']
        epoch_date = datetime.datetime.strptime(mydate, '%Y-%m-%d %H:%M')
        epoch_date = pytz.utc.localize(epoch_date).timestamp()
        location = request.form['Location']
        status = request.form['Status']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO bitcase VALUES (NULL, %s, %s, %s, %s, %s)',
                       (casename, epoch_date,location, status, account_id['id']))
        mysql.connection.commit()
        msg = 'You have successfully created a case!'
    return render_template('case-add.html', msg=msg, username=session['username'], role=session['role'], name=name)


# Error handling Page
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='404'), 404


# Admin logged-in check function
def admin_loggedin():
    if 'loggedin' in session and session['role'] == 'Admin':
        # admin logged-in
        return True
    # admin not logged-in return false
    return False


# Admin Page
@app.route('/admin/', methods=['GET', 'POST'])
def admin():
    # Check if admin is logged-in
    if not admin_loggedin():
        return redirect(url_for('login'))
    msg = ''
    # Retrieve all accounts from the database
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts')
    accounts = cursor.fetchall()
    return render_template('admin/index.html', username=session['username'], role=session['role'], accounts=accounts)


@app.route('/admin/account/<int:id>', methods=['GET', 'POST'])
@app.route('/admin/account', methods=['GET', 'POST'], defaults={'id': None})
def admin_account(id):
    # Check if admin is logged-in
    if not admin_loggedin():
        return redirect(url_for('login'))
    page = 'Create'
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # Default input account values
    account = {
        'username': '',
        'password': '',
        'email': '',
        'activation_code': '',
        'rememberme': '',
        'role': 'Member'
    }
    roles = ['Member', 'Admin'];
    # GET request ID exists, edit account
    if id:
        # Edit an existing account
        page = 'Edit'
        # Retrieve account by ID with the GET request ID
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (id,))
        account = cursor.fetchone()
        if request.method == 'POST' and 'submit' in request.form:
            # update account
            password = account['password']
            if account['password'] != request.form['password']:
                hash = request.form['password'] + app.secret_key
                hash = hashlib.sha1(hash.encode())
                password = hash.hexdigest();
            cursor.execute(
                'UPDATE accounts SET username = %s, password = %s, email = %s, activation_code = %s, rememberme = %s, '
                'role = %s WHERE id = %s',
                (request.form['username'], password, request.form['email'], request.form['activation_code'],
                 request.form['rememberme'], request.form['role'], id,))
            mysql.connection.commit()
            return redirect(url_for('admin'))
        if request.method == 'POST' and 'delete' in request.form:
            # delete account
            cursor.execute('DELETE FROM accounts WHERE id = %s', (id,))
            mysql.connection.commit()
            return redirect(url_for('admin'))
    if request.method == 'POST' and request.form['submit']:
        # Create new account
        hash = request.form['password'] + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest();
        cursor.execute(
            'INSERT INTO accounts (username,password,email,activation_code,rememberme,role) VALUES (%s,%s,%s,%s,%s,%s)',
            (request.form['username'], password, request.form['email'], request.form['activation_code'],
             request.form['rememberme'], request.form['role'],))
        mysql.connection.commit()
        return redirect(url_for('admin'))
    return render_template('admin/account.html', username=session['username'], role=session['role'], account=account,
                           page=page, roles=roles)


# API Call - Basic Case Info
@app.route('/api/basic_case_info/', methods=['GET'])
def basic_case_info_api_call():
    # Retrieve the username & password from the "GET request"
    username = request.args.get("username")
    password = request.args.get("password")
    hash = password + app.secret_key
    hash = hashlib.sha1(hash.encode())
    password = hash.hexdigest()
    # Check if account exists using MySQL
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
    account = cursor.fetchone()
    
    final_case_list,evidence_list=[],[]
    case_dict,evidence_dict,final_case_dict = {},{},{}
    # Retrieve the case id that the user account is in charged of 
    if account:
        cursor.execute('SELECT id FROM bitcase WHERE account_id = %s', (account['id'],))
        case_id = cursor.fetchall() 
        # Loop through the different cases(identify by id) that the user is in charged of 
        for caseid in case_id:
            # Get the evidence data from the blockchain (filter by case id)
            add_item_filter = contract_w3.events.evidenceAdded.createFilter(fromBlock=1, argument_filters={"_caseId":caseid['id']})
            added_items = add_item_filter.get_all_entries()
            # Looping through the evidence data (1 case can have more than 1 evidence)
            if added_items:
                for num in range(len(added_items)):
                    cursor.execute('SELECT * FROM bitcase  WHERE id = %s', (caseid['id'],))
                    case_data = cursor.fetchone()
                    # storing the case data in a dictionary (case_dict)
                    if case_data:
                        case_dict['case_name'] = case_data['case_name']
                        case_dict['date'] = case_data['case_date']
                        case_dict['location'] = case_data['location']
                        case_dict['case_status'] = case_data['status']
                    #storing the evidence data in a dictionary (evidence_dict)
                    evidence_dict['evid_id'] = added_items[num]["args"]["_evidId"]
                    evidence_dict['handler'] = username
                    evidence_dict['curr_status'] = added_items[num]["args"]["_currStatus"]
                    evidence_dict['serial_no'] = added_items[num]["args"]["_serialNo"]
                    evidence_list.append(evidence_dict.copy())
                    evidence_dict.clear()
            else:
                cursor.execute('SELECT * FROM bitcase  WHERE id = %s', (caseid['id'],))
                case_data = cursor.fetchone()
                # storing the case data in a dictionary (case_dict)
                if case_data:
                    case_dict['case_name'] = case_data['case_name']
                    case_dict['date'] = case_data['case_date']
                    case_dict['location'] = case_data['location']
                    case_dict['case_status'] = case_data['status']
            case_dict['evidence'] = evidence_list.copy()
            final_case_list.append(case_dict.copy())
            evidence_list.clear()

        final_case_dict['cases'] = final_case_list
        return jsonify(final_case_dict)    

    else:
        return "No user account"


# API Call - add_evidence
@app.route('/api/add_evidence/', methods=['POST'])
def add_evidence_api_call():
    content = request.get_json(silent=True)
    case_id = content['case_id']
    handler = content['handler']
   
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id FROM accounts WHERE username = %s', (handler,))
    account_id = cursor.fetchone()
    if account_id:
        handler_id = account_id['id']
        latest_evidence_in_case = contract_w3.events.evidenceAdded.createFilter(fromBlock=1, argument_filters={"_caseId":case_id})
        latest_evidence = latest_evidence_in_case.get_all_entries()
        current_case_latest_evid_id = 0
       
        if len(latest_evidence) != 0:
            current_case_latest_evid_id = latest_evidence[len(latest_evidence)-1]["args"]["_evidId"]

        for dict_item in content['draft_evid']:
            # If current case already has evidences
            if current_case_latest_evid_id != 0:
                add_evid_id = dict_item["draft_evid_id"] + current_case_latest_evid_id
            else:
                add_evid_id = dict_item["draft_evid_id"]

            # Receiving image & saving it to its directories 
            img_str = dict_item['image']
            jpg_original = base64.b64decode(img_str)
            jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
            img = cv2.imdecode(jpg_as_np, flags=1)
            dirname = "Case/" + "case_id "+ str(case_id) + "/" + "Evidence_id " + str(add_evid_id)
            os.makedirs(dirname,exist_ok=True)
            cv2.imwrite(os.path.join(dirname,"1.jpg"), img)
            # Caculate Image Hash
            with open(dirname +"/1.jpg","rb") as f:
                bytes = f.read() # read entire file as bytes
                image_hash = hashlib.sha256(bytes).hexdigest();
            # Sending Case & Evidence data to the blockchain
            contract.addEvidenceItem(case_id,add_evid_id,handler_id,dict_item["location"],image_hash,dict_item["evid_type"],dict_item["serial_no"],"",dict_item["condition"],"",dict_item["notes"], {'from': accounts[0], 'gas_price':0})
    
        add_item_filter = contract_w3.events.evidenceAdded.createFilter(fromBlock=1, argument_filters={"_caseId":case_id})
        added_items = add_item_filter.get_all_entries()
        final_case_list,evidence_list=[],[]
        case_dict,evidence_dict,final_case_dict = {},{},{}

        if added_items:
            for num in range(len(added_items)):
                case_id = added_items[num]["args"]["_caseId"]
                cursor.execute('SELECT * FROM bitcase  WHERE id = %s', (case_id,))
                case_data = cursor.fetchone()
                # storing the case data in a dictionary (case_dict)
                if case_data:
                    case_dict['case_name'] = case_data['case_name']
                    case_dict['date'] = case_data['case_date']
                    case_dict['location'] = case_data['location']
                    case_dict['case_status'] = case_data['status']
                #storing the evidence data in a dictionary (evidence_dict)
                evidence_dict['evid_id'] = added_items[num]["args"]["_evidId"]
                evidence_dict['handler'] = handler
                evidence_dict['curr_status'] = added_items[num]["args"]["_currStatus"]
                evidence_dict['serial_no'] = added_items[num]["args"]["_serialNo"]
                evidence_list.append(evidence_dict.copy())
                evidence_dict.clear()
        else:
            cursor.execute('SELECT * FROM bitcase  WHERE id = %s', (caseid['id'],))
            case_data = cursor.fetchone()
            # storing the case data in a dictionary (case_dict)
            if case_data:
                case_dict['case_name'] = case_data['case_name']
                case_dict['date'] = case_data['case_date']
                case_dict['location'] = case_data['location']
                case_dict['case_status'] = case_data['status']
            
        case_dict['evidence'] = evidence_list.copy()
        final_case_list.append(case_dict.copy())
        evidence_list.clear()
        final_case_dict['cases'] = final_case_list
        return jsonify(final_case_dict)
    else:
        return "No user account"


# API Call - Get Evidence
@app.route('/api/view_evidence/', methods=['GET'])
def view_evidence_api_call():
    # Retrieve the caseid from the "GET request"
    CaseId = request.args.get("caseid")
    EvidenceId = request.args.get("evidenceid")
    
    # Check the validity of the Case Id 
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM bitcase WHERE id = %s', (CaseId,))
    case = cursor.fetchone()

    if case:
        # Fill in the case data information to the dictionary
        case_dict = {}
        case_dict['case_id'] = CaseId
        case_dict['evid_id'] = EvidenceId
        case_dict['location'] = case['location']
        account_id = case['account_id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT username FROM accounts WHERE id = %s', (account_id,))
        username = cursor.fetchone()
        case_dict['handler'] = username['username']
        case_dict['evid_type'] = (contract.centralStore(int(CaseId),int(EvidenceId))[3])
        case_dict['serial_no'] = (contract.centralStore(int(CaseId),int(EvidenceId))[4])
        case_dict['notes'] = (contract.centralStore(int(CaseId),int(EvidenceId))[8])
        case_dict['curr_status'] = (contract.centralStore(int(CaseId),int(EvidenceId))[6])

        add_item_filter = contract_w3.events.evidenceAdded.createFilter(fromBlock=1, argument_filters={"_caseId":int(CaseId),"_evidId": int(EvidenceId)})
        first_added_evidence = add_item_filter.get_all_entries()

        change_filter = contract_w3.events.statusChanged.createFilter(fromBlock=1, argument_filters={"_caseId": int(CaseId),"_evidId": int(EvidenceId)})
        modified_evidence = change_filter.get_all_entries()
    
        dirname = "Case/" + "case_id "+ str(CaseId) + "/" + "Evidence_id " + str(EvidenceId)
        # Caculate Image Hash
        with open(dirname +"/1.jpg","rb") as f:
            bytes = f.read() # read entire file as bytes
            image_hash = hashlib.sha256(bytes).hexdigest();
        storage_image_hash = (contract.centralStore(int(CaseId),int(EvidenceId))[2])
         
        if image_hash == storage_image_hash:
            case_dict["image"] = image_hash
        else:
            case_dict["image"] = "corrupted"
        
        evidence_dict = {}
        evidence_list = []

        if first_added_evidence:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT username FROM accounts WHERE id = %s', (first_added_evidence[0]["args"]["_handlerId"],))
            username = cursor.fetchone()
            transHash = first_added_evidence[len(first_added_evidence)-1]["transactionHash"].hex()
            tx = chain.get_transaction(transHash)
            evidence_dict['time'] = first_added_evidence[0]["args"]["date"]
            evidence_dict['handler'] = username['username']
            evidence_dict['status'] = first_added_evidence[0]["args"]["_currStatus"]
            evidence_dict['purpose'] = contract.decode_input(tx.input)[1][9]
            evidence_list.append(evidence_dict.copy())
            evidence_dict.clear()
            
            if modified_evidence:
                for num in range(len(modified_evidence)):
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('SELECT username FROM accounts WHERE id = %s', (modified_evidence[num]["args"]["_handlerId"],))
                    username = cursor.fetchone()
                    evidence_dict['time'] = modified_evidence[num]["args"]["date"]
                    evidence_dict['handler'] = username['username']
                    evidence_dict['status'] = modified_evidence[num]["args"]["_currStatus"]
                    evidence_dict['purpose'] = modified_evidence[num]["args"]["_purpose"]
                    evidence_list.append(evidence_dict.copy())
                    evidence_dict.clear()

        case_dict['evidence'] = evidence_list.copy()
        return jsonify(case_dict)

    else:
        return "No User Accounts"

        

# API Call - check in/check out
@app.route('/api/check_evidence/', methods=['POST'])
def check_evidence_api_call():
    content = request.get_json(silent=True)
    case_id = content['case_id']
    evid_id = content['evid_id']
    handler = content['handler']
    new_status = content['new_status']
    purpose = content['purpose']
    b64_image = content['image']


    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id FROM accounts WHERE username = %s', (handler,))
    account_id = cursor.fetchone()
    if account_id:
        handler_id = account_id['id']
        jpg_original = base64.b64decode(b64_image)
        jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
        img = cv2.imdecode(jpg_as_np, flags=1)
        dirname = "Case/" + "case_id "+ str(case_id) + "/" + "Evidence_id " + str(evid_id)
        os.makedirs(dirname,exist_ok=True)
        cv2.imwrite(os.path.join(dirname,"1.jpg"), img)
        # Caculate Image Hash
        with open(dirname +"/1.jpg","rb") as f:
            bytes = f.read() # read entire file as bytes
            image_hash = hashlib.sha256(bytes).hexdigest();
        # Sending Case & Evidence data to the blockchain
        contract.modifyEvidenceStatus(case_id,evid_id,handler_id,new_status,image_hash,purpose,{'from': accounts[0], 'gas_price':0})
        return "Success"
    else:
        return "No User Account"


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
