from flask import Flask,flash, render_template,session, redirect, url_for, request
from functools import wraps
import requests
app = Flask(__name__)

app.secret_key = "my precious"

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            #flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/', methods=['GET', 'POST']) #@login_required
def home():
    #35.188.64.208:80/create
    if request.method == 'POST':
        flash("TEST")
    return render_template("welcome.html")

@app.route('/welcome')
def welcome():
    
    url = "http://35.188.64.208:80/stats"

    payload = "{\n\t\"space_id\": \"12345\",\n\t\"plate_num\": \"DZVG49\"\n}"
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'Postman-Token': "76bc076b-49bb-4145-9300-8b0472e5a6b9"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    payload = "{\n\t\"space_id\": \"12345\",\n\t\"plate_num\": \"BKTP665\"\n}"
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'Postman-Token': "76bc076b-49bb-4145-9300-8b0472e5a6b9"
    }

    response1 = requests.request("POST", url, data=payload, headers=headers)


    payload = "{\n\t\"space_id\": \"12345\",\n\t\"plate_num\": \"SSTARZZ\"\n}"
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'Postman-Token': "76bc076b-49bb-4145-9300-8b0472e5a6b9"
    }

    response2 = requests.request("POST", url, data=payload, headers=headers)

    payload = "{\n\t\"space_id\": \"12345\",\n\t\"plate_num\": \"N0GSTNK\"\n}"
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'Postman-Token': "76bc076b-49bb-4145-9300-8b0472e5a6b9"
    }

    response3 = requests.request("POST", url, data=payload, headers=headers)
    
    return render_template("welcome.html", var=response.text, var1=response1.text, var2=response2.text, var3=response3.text)

@app.route('/api', methods=['GET', 'POST'])
def api():
    error = None
    if request.method == 'POST':
            #session['logged_in'] = True
            flash('You registered')
            url = "http://35.188.64.208:80/create"

            payload = "first_name=%s&last_name=%s&plate_num=%s" %(request.form['firstname'],request.form['lastname'],request.form['lpn'])
            #print(payload)
            headers = {
                'Content-Type': "application/x-www-form-urlencoded",
                'cache-control': "no-cache",
                'Postman-Token': "ef1ecc98-41eb-42cb-bb1b-290cdd7a6e15"
                }

            response = requests.request("POST", url, data=payload, headers=headers)
            #error = 'yp'
            #print(response.text)
            return redirect(url_for('welcome'))
    return render_template('api.html',error=error)
    #return render_template('login.html', error=error)
    
    

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'park' or request.form['password'] != 'me':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            #flash('You were just logged in')
            flash('You logged in')
            url = "http://35.188.64.208:80/create"

            payload = "plate_num=%s" %(request.form['lpn'])
            #print(payload)
            headers = {
                'Content-Type': "application/x-www-form-urlencoded",
                'cache-control': "no-cache",
                'Postman-Token': "ef1ecc98-41eb-42cb-bb1b-290cdd7a6e15"
                }

            response = requests.request("POST", url, data=payload, headers=headers)
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    #flash('You were just logged out')
    return redirect(url_for('welcome'))

if __name__ == "__main__":
    app.run(debug=True)