from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection strinig
# connect to local host now
client = MongoClient()
db=client.tweet_db

def insert_document(tweet_doc):
	tweets = db.tweets
	#TODO: use insert_many 
	result = tweets.insert_one(tweet_doc)
	print(result)

def get_total_positive_sentiment(topic):
	result = list(db.tweets.aggregate([ { "$match": {"$and":[{"sentiment":{"$gt":0}},{"$text":{"$search":topic}}]} }, { "$group":{"_id":"null", "count":{"$sum":"$sentiment"}} } ]))
	#print(result)
	return result[0]["count"]

def get_total_negative_sentiment(topic):
	result = list(db.tweets.aggregate([ { "$match": {"$and":[{"sentiment":{"$lt":0}},{"$text":{"$search":topic}}]} }, { "$group":{"_id":"null", "count":{"$sum":"$sentiment"}} } ]))
	return result[0]["count"]
