from flask import Flask, render_template, request, redirect, url_for
import sqlite3, os

app = Flask(__name__)

db_path = '/var/www/html/flaskapp/mydatabase.db'

conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute('''
        CREATE TABLE IF NOT EXISTS users (
	    username TEXT, password TEXT, firstname TEXT, lastname TEXT, email TEXT)''')
conn.commit()
conn.close()


@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO user (username, password, firstname, lastname, email) VALUES (?,?,?,?,?)",
    (username, password, firstname, lastname, email))
    conn.commit()
    conn.close()

    return redirect(url_for('profile', username=username))

@app.route('/profile/<username>')
def profile(username):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM user WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()

    if user:
        return render_template('profile.html',firstname=user[3],lastname=user[4],username=user[1],email=user[5])
    else:
        return "User not Found"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        c.execute("SELECT * FROM user WHERE username=? AND password=?", (username,password,))
        user = c.fetchone()
        conn.close()

        if user:
            return render_template('profile.html',user=user)
        else:
            return redirect(url_for('login',error='Invalid Username or Password'))
    error_message = request.args.get("error")
    return render_template('login.html', error=error_message)

if __name__ == '__main__':
    app.run(debug=True)
