from flask import Flask
import db
from flask import jsonify
from flask_socketio import SocketIO,emit,send
import random
#from flask_cors import CORS

app = Flask(__name__)
#CORS(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app,cors_allowed_origins="*")

@app.route("/")
def home():
	total_positive_sentiment_biden = db.get_total_positive_sentiment("biden")
	total_negative_sentiment_biden = db.get_total_negative_sentiment("biden")
	total_positive_sentiment_trump = db.get_total_positive_sentiment("trump")
	total_negative_sentiment_trump = db.get_total_negative_sentiment("trump")
	return_body = {}
	trump = {}
	biden = {}
	trump["positive_sentiment"] = total_positive_sentiment_trump
	trump["negative_sentiment"] = total_negative_sentiment_trump	
	biden["positive_sentiment"] = total_positive_sentiment_biden
	biden["negative_sentiment"] = total_negative_sentiment_biden
	return_body["trump"] = trump
	return_body["biden"] = biden
	return jsonify(return_body)

@socketio.on('connect', namespace='/test')
def test_connect():
    print("I am here")
    #while True:
    	#socketio.emit('test', 14)

@socketio.on("subscribeToTimer",namespace="/test")
def handle_message(json):
	#val = print(get_sentiments())
	emit("test",get_sentiments())

def get_sentiments():
	total_positive_sentiment_biden = db.get_total_positive_sentiment("@JoeBiden")
	total_negative_sentiment_biden = db.get_total_negative_sentiment("@JoeBiden")
	total_positive_sentiment_trump = db.get_total_positive_sentiment("@realDonaldTrump")
	total_negative_sentiment_trump = db.get_total_negative_sentiment("@realDonaldTrump")
	return_body = {}
	trump = {}
	biden = {}
	trump["positive_sentiment"] = total_positive_sentiment_trump
	trump["negative_sentiment"] = total_negative_sentiment_trump
	biden["positive_sentiment"] = total_positive_sentiment_biden
	biden["negative_sentiment"] = total_negative_sentiment_biden
	return_body["trump"] = trump
	return_body["biden"] = biden
	return return_body

if __name__ == "__main__":
	socketio.run(app,host="localhost")
