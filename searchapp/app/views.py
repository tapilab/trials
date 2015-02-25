from flask import render_template
from app import app
from app import forms

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/search')
def search():
    user = { 'nickname': 'Miguel' } # fake user
    return render_template("index.html",
    		title = 'Home',
    		user = user)

@app.route('/query')
def query():
    form = SearchQueryForm()
    return render_template('login.html', 
                           title='Search',
                           form=form)