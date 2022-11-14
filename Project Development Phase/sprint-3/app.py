from flask import Flask, render_template, request, redirect, url_for, session
import os
import re
import ibm_db

app = Flask(__name__)

app.secret_key = 'my secret key'

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=815fa4db-dc03-4c70-869a-a9cc13f33084.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30367;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=mmt12018;PWD=0E1LdotobXSoI8u6",'','')

picFolder = os.path.join('static','pics')
app.config['UPLOAD_FOLDER'] = picFolder

@app.route("/dashboard")
def dashboard():
	dashboardPic = os.path.join(app.config['UPLOAD_FOLDER'],'dashboard.jpg')
	return render_template('dashboard.html', dashboard=dashboardPic)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ' '
	loginPic = os.path.join(app.config['UPLOAD_FOLDER'],'images.jfif')
	if request.method == 'POST' and 'usrname' in request.form and 'password' in request.form:
		username = request.form['usrname']
		password = request.form['password']
		sql = "SELECT * FROM account WHERE ID = '"+username+"' AND pass = '"+password+"'"
		stmt = ibm_db.exec_immediate(conn, sql)
		account = ibm_db.fetch_both(stmt)
		if account:
			session['loggedin'] = True
			session['id'] = account[0]
			session['username'] = account[1]
			msg = 'Logged in successfully !'
			return redirect(url_for('dashboard'))
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', errorMsg = msg,loginpic = loginPic)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	registerImg = os.path.join(app.config['UPLOAD_FOLDER'],'login.jpg')
	if request.method == 'POST' and 'usrname' in request.form and 'password' in request.form and 'email' in request.form :
		username = request.form['usrname']
		password = request.form['password']
		email = request.form['email']
		sql = "SELECT * FROM account WHERE ID = '"+username+"'"
		stmt = ibm_db.exec_immediate(conn, sql)
		account = ibm_db.fetch_both(stmt)

		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		elif not username or not password or not email:
			msg = 'Please fill out the form !'
		else:
			ins = "INSERT INTO account VALUES ('"+username+"','"+email+"','"+password+"')"
			prep_stmt = ibm_db.prepare(conn, ins)
			ibm_db.execute(prep_stmt)
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out form !'
	return render_template('register.html', errorMsg = msg,registerImg=registerImg)

if __name__ == '__main__':
	app.run()
