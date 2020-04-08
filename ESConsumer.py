import re
import json
from elasticsearch import Elasticsearch
from kafka import KafkaConsumer
from datetime import datetime
from conf import BONSAI_URL,KAFKA_BOOTSRAP_SERVER

def connect_elasticsearch():
    auth = re.search('https\:\/\/(.*)\@', BONSAI_URL).group(1).split(':')
    host = BONSAI_URL.replace('https://%s:%s@' % (auth[0], auth[1]), '')
    
    # optional port
    match = re.search('(:\d+)', host)
    if match:
        p = match.group(0)
        host = host.replace(p, '')
        port = int(p.split(':')[1])
    else:
        port=443

    # Connect to cluster over SSL:
    es_header = [{'host': host,'port': port,'use_ssl': True,'http_auth': (auth[0],auth[1])}]
    es = Elasticsearch(es_header)

    # Verify that Python can talk to Bonsai (optional):
    if es.ping():
        print('Bonsai Elasticsearch connected')
    else:
        print('Connection Failed!')
    return es


if __name__ == "__main__":
    
    es = connect_elasticsearch()
    es.indices.create(index='tweets', ignore=400)
    
    consumer = KafkaConsumer(bootstrap_servers=[KAFKA_BOOTSRAP_SERVER],
                            group_id='kafka-es-demo',
                            auto_offset_reset='latest',
                            value_deserializer=lambda m: json.loads(m.decode('utf-8')))

    consumer.subscribe('twitter_tweets')

    for message in consumer:
        message = message.value
        # print(message)

        res = es.index(index='tweets',body=message)
        print(res['_id'])


