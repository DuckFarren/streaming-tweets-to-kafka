# Streaming Tweets Using Kafka
A simple demo using Twitter Streaming API to send messages to Kafka and process them out to Elasticsearch for data analysis.

## Installation and Configuration
This project uses Tweepy library to get tweets from twitter, and Kafka to stream data into Bonsai Elasticsearch. 

#### Python libraries:
```
conda install -c conda-forge tweepy  /  pip install tweepy
```
```
conda install -c conda-forge kafka-python / pip install kafka-python
```
```
conda install -c conda-forge elasticsearch  /  pip install elasticsearch
```
#### Kafka configuration
We assume you have Kafka installed somewhere, first start Zookeeper and Kafka server, then create a new topic

#### Config file
A Twitter developer account is required to access Twitter APIs.
If you do not wish to install Elasticsearch on your local machine, you may register an account on Bonsai.io and use its free tier service.

Paste all the access token and secret key to conf.py

### Running
After installing all the neccessary libraries, run the script to start streaming
```
python main.py
```
