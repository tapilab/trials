from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/search')
def search():
    user = { 'nickname': 'Miguel' } # fake user
    return '''
<html>
  <head>
    <title>Home Page</title>
  </head>
  <body>
    <h1>Hello, ''' + user['nickname'] + '''</h1>
  </body>
</html>
'''