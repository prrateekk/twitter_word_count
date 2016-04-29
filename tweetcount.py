from flask import Flask,redirect,url_for,request,render_template
import tweepy
import sys
import datetime
import time
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

consumer_key = 'Your consumer key here'
consumer_secret = 'Your consumer secret here'
access_token = 'Your access token here'
access_secret = 'Your access secret here'

auth = OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)

api = tweepy.API(auth)

app = Flask(__name__)


count=None

class MyListener(StreamListener):
    def __init__(self, time_limit):
        global count
        count = 0
        self.time = time.time()
        self.limit = time_limit

    def on_data(self, data):
        global count
        while ((time.time() - self.time) < self.limit):
            try:
                count+=1
                return True
            except BaseException as e:
                time.sleep(5)
                pass
        return False

def past(name,d):
	global count
	count = 0
	u=datetime.date.today()
	for tweet in tweepy.Cursor(api.search,q=name,since=u-datetime.timedelta(d),until=u,lang='en').items():
		count+=1

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/success/<name>/<tme>')
def success(name,tme):
	global count

	d,waste1,waste2 = tme.split()
	d=eval(d)

	if d>7:
		twitter_stream = Stream(auth, MyListener(time_limit=d))
		twitter_stream.filter(track=[name])
	else:
		past(name,d)

	return render_template('welcome.html',count=count,name=name,duration=tme)

@app.route('/login',methods = ['POST', 'GET'])
def login():
	if request.method == 'POST':
		user = request.form['nm']
		tme = request.form['tm']
		return redirect(url_for('success',name=user,tme=tme))
	else:
		user = request.args.get('nm')
		tme = request.args.get('tm')
		return redirect(url_for('success',name=user,tme=tme))

if __name__ == '__main__':
	app.run(debug = True)

