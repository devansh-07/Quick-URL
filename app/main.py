from flask import Flask, render_template, url_for, request, redirect
import sqlite3

#######

def base62enc(n, b=62):
    vals = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    s = '0' if n == 0 else ''
    while n >= 1:
        r = n%b
        n //= b
        s = str(vals[r]) + s
    return s

def base62dec(s, b=62):
    vals = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    n = 0
    for i, v in enumerate(s[::-1]):
        n += (vals.index(v))*(b**i)
    return n
    
#######

def create_table():
    con = sqlite3.connect('app/urlDetails.db')
    cursorObj = con.cursor()
    try:
        cursorObj.execute("CREATE TABLE urls(ID INTEGER PRIMARY KEY AUTOINCREMENT, URL TEXT)")
        con.commit()
    except:
        pass

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        givenUrl = request.form.get('url')
        con = sqlite3.connect('app/urlDetails.db')
        cursorObj = con.cursor()
        try:
            mycursor = cursorObj.execute("INSERT INTO urls(URL) VALUES('{}')".format(givenUrl))
            con.commit()
            short_url = base62enc(mycursor.lastrowid)
            return render_template('home.html', newurl='https://url-engine.herokuapp.com/'+str(short_url))
        except:
            return render_template('home.html')
    return render_template('home.html')

@app.route('/<url>')
def newpage(url):
    idx = base62dec(url)
    con = sqlite3.connect('app/urlDetails.db')
    cursorObj = con.cursor()

    mycursor = cursorObj.execute("SELECT URL FROM urls WHERE ID={}".format(idx))
    con.commit()
    org_url = mycursor.fetchone()[0]

    if (not org_url.startswith("http")):
        org_url = "http://" + org_url

    return redirect(org_url)

