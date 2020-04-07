from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from kafka import KafkaProducer
import json
import conf

topic_name = "twitter_tweets"
KAFKA_ENDPOINT = 'localhost:9092'

class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(conf.CONSUMER_KEY, conf.CONSUMER_SECRET)
        auth.set_access_token(conf.ACCESS_TOKEN,conf.ACCESS_TOKEN_SECRET)
        return auth

class TwitterStreamer():
    """
    Class for streaming and processing live tweets
    """
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, hash_tag_list):
        # This handles Twitter authentication and the connection to the Twitter Streaming API
        listener = TwitterListener()
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        stream.filter(track=hash_tag_list)
        return listener.dat

class TwitterListener(StreamListener):

    producer = KafkaProducer(bootstrap_servers=KAFKA_ENDPOINT, acks=1,linger_ms=20)
    # compression_type='snappy'

    def on_data(self,data):
        tweet = json.loads(data)
        if 'text' in tweet:
            message = tweet['text'].encode("utf-8").rstrip()
        self.producer.send(topic_name, message)
        print(message)

    def on_status(self, status):
        print(status.text)
    
    def on_error(self, status_code):
        if status_code == 420:
            return False

if __name__ == "__main__":
    hash_tag_list = ['bitcoin']
    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(hash_tag_list)