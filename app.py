from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
import os
import tempfile

firebaseConfig = {
  'apiKey': "AIzaSyBeikazStTzsgzNxvgcXniLJYAE4xN0rl4",
  'authDomain': "iasa-website.firebaseapp.com",
  #'databaseURL': "https://iasa-website-default-rtdb.europe-west1.firebasedatabase.app",
  'projectId': "iasa-website",
  'storageBucket': "iasa-website.appspot.com",
  'messagingSenderId': "628030739943",
  'appId': "1:628030739943:web:997f144c47acf40cc4d942",
  'measurementId': "G-NERBP2YRD4",
  "databaseURL": 'https://iasa-website-default-rtdb.europe-west1.firebasedatabase.app/'
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'iasa2000'
###################################

@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method == 'POST':
		#login thing
		error=''
	else:
		return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  error=''
  if request.method=='POST':
    if request.form['password']==request.form['confirmPassword']:
      try:
        user = {'name': request.form['name'], 'account-type': 1}
        login_session['user'] = auth.create_user_with_email_and_password(request.form['email'], request.form['password'])
        db.child('Users').child(login_session['user']['localId']).set(user)
        return render_template('add-review.html')
      except:
        error = 'Authentication error'
        print(error)
        return render_template('signup.html')
    else:
      return render_template('signup.html', error='confirm-password')
  else:
    return render_template('signup.html')

@app.route('/login', methods=['GET','POST'])
def login():
  error=''
  if request.method=='POST':
    try:
      email = request.form['email']
      pwd = request.form['password']
      login_session['user'] = auth.sign_in_with_email_and_password(email, pwd)
      return redirect(url_for('home'))
    except:
      error='Authentication error'
      print(error)
      return render_template('login.html')
  else:
      print('hahahhaha')
      return render_template('login.html')

@app.route('/logout')
def logout():
  login_session['user'] = None
  auth.current_user = None
  return redirect(url_for('signin'))

@app.route('/post-review', methods=['GET', 'POST'])
def post_review():
  error=''
  if request.method=='POST':
    if request.form['type']=='1':
      thing = request.form['title']
      name = 'rooms/'+thing
    else:
      thing = request.form['title']
      name = 'food/'+thing
    picture = request.files['image']
    firebase.storage().child(name).put(picture)
    url = firebase.storage().child(name).get_url(None)

    post = {'title': request.form['title'], 'text':request.form['review'], 'url':url, 'type':request.form['type']}
    try:
      if request.form['type'] == '1':
        db.child('RoomsRev').push(post)
      else:
        db.child('FoodRev').push(post)
      roomposts = db.child('RoomsRev').get().val()
      foodposts = db.child('FoodRev').get().val()
      return render_template('reviews.html', roomposts=roomposts, foodposts=foodposts, post=post)

    except:
      error='authentication error'
      print(error)
      return render_template('add-review.html')
  else:
    return render_template('add-review.html')

@app.route('/menu')
def menu():
  return render_template('menu.html')

@app.route('/reviews')
def reviews():
  return render_template('reviews.html')
###################################
if __name__ == '__main__':
    app.run(debug=True)
