from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/search')
def search():
    return "Do search here"
