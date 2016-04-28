from flask import Flask,redirect,url_for,request,render_template
import tweepy
import sys
import time
from tweepy import OAuthHandler

consumer_key = 'Your consumer key here'
consumer_secret = 'Your consumer secret here'
access_token = 'Your access token here'
access_secret = 'Your access secret here'

auth = OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)

api = tweepy.API(auth)

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/success/<name>/<last>')
def success(name,last):
	c=0
	for tweet in tweepy.Cursor(api.search,q=name,since='2016-04-25',until='2016-04-26',lang='en').items():
		c+=1
	return render_template('welcome.html',count=c)

@app.route('/login',methods = ['POST', 'GET'])
def login():
	if request.method == 'POST':
		user = request.form['nm']
		last = request.form['tm']
		return redirect(url_for('success',name=user,last=last))
	else:
		user = request.args.get('nm')
		last = request.args.get('tm')
		return redirect(url_for('success',name=user,last=last))

if __name__ == '__main__':
	app.run(debug = True)
