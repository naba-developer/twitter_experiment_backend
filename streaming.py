from __future__ import absolute_import, print_function
#from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from tweepy import OAuthHandler, Stream, StreamListener
import db

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="qIiWJNdCT72osTiuzc3tD9E1V"
consumer_secret="5QCjM9oxlPl9wl4MtXB3fwAxUXcNjrSiKDsSbu8kGNnbWMQbpt"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="1437787351-u7aCt6jSZNDWHxeVU2WIsayuXXx1tqFH3r1VHKk"
access_token_secret="PGsopzZicpvd1LKD9gLeAmDUblgx27vdIZCtFifQTQTkS"

analyzer = SentimentIntensityAnalyzer()

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_status(self, status):
        #if hasattr(status,'retweeted_status'):
        #    return False
        #if (("@realDonaldTrump" not in status.text) or ("@JoeBiden" not in status.text)):
        #    return False    
        blob = analyzer.polarity_scores(status.text)
        mongo_db_doc = {}
        mongo_db_doc["tweet"] = status.text
        mongo_db_doc["sentiment"] = blob['compound']
        #mongo_db_doc["location"] = status.place
        mongo_db_doc["coordinates"] = status.coordinates
        mongo_db_doc["created_at"] = status.created_at
        db.insert_document(mongo_db_doc)
        #print(status.user.screen_name+","+status.text+","+str(blob['compound']) + ","+str(hasattr(status,'retweeted_status'))+","+str(status.created_at))
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['@realDonaldTrump,@JoeBiden'])
