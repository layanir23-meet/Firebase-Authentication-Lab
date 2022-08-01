from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase 

config = {
  "apiKey": "AIzaSyBjxBUvDHXuHy7uFagDSDPUIifkBayAnTE",
  "authDomain": "fir-lab-layani.firebaseapp.com",
  "projectId": "fir-lab-layani",
  "storageBucket": "fir-lab-layani.appspot.com",
  "messagingSenderId": "280741768998",
  "appId": "1:280741768998:web:8707941bf58ff45029dbe7",
  "measurementId": "G-F72Z11Q9GH","databaseURL" : "https://fir-lab-layani-default-rtdb.europe-west1.firebasedatabase.app/" 

}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()




app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error=""
    if request.method == "POST":
        email= request.form['email']
        password = request.form ['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email,password)
            return redirect (url_for('add_tweet'))

        except:
            error = "Authentication failed"
    return render_template("signin.html")



    


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == "POST":
        email= request.form['email']
        password = request.form ['password']
        full_name = request.form['full_name']
        user_name = request.form['user_name']
        bio = request.form ['bio']
        
        try :
            login_session['user'] = auth.create_user_with_email_and_password(email,password)
            user = {"full_name" : full_name , "user_name" : user_name , "bio" : bio }
            db.child("users").child(login_session['user']['localId']).set(user)



            return redirect (url_for('add_tweet'))

        except:
            error = "Authentication failed"
    return render_template("signup.html")



    


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == "POST":
        tweetf =request.form['tweet']
        try:
            tweet = {"tweet" : tweetf, "uid" : login_session['user']['localId']}
            db.child("tweets").push(tweet)
            return redirect(url_for("all_tweet"))
        except:
            error = "Authentication failed"
            return render_template("add_tweet.html")
        

    else:
        return render_template("add_tweet.html")


        
    

 

    

@app.route ('/all_tweets' , methods = ['GET', 'POST'])
def all_tweet():
     tweet = db.child("tweets").get().val()
     return render_template ("tweets.html", tweet = tweet )

if __name__ == '__main__':
    app.run(debug=True)