import requests
from google.cloud import pubsub_v1
import logging
import os

#environment variable in code aanmaken (linux zelf gaf problemen)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/mendel/project3/Project3-ML6-515024366790.json"
logging.basicConfig(filename='CloudManager.log',level=logging.INFO)

class CloudManager():
    def __init__(self, project_id, topic_name):
        logging.info("Initialized cloud manager with project-id: %s and topic-name: %s"% (project_id,topic_name))
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(project_id, topic_name)

    def publish_to_topic(self,data:str):
        logging.info("Sending attempt for data: %s"% data)
        message = data.encode('utf-8')
        if self.check_internet():
            publish_message = self.publisher.publish(self.topic_path,data=message)
            publish_message.add_done_callback(self.callback_status) #validate if it was sent succesfully
        else:
            self.save_to_local_storrage(data)

    def save_to_local_storrage(self, data):
        logging.info("Localy caching the following message: %s"%data)
        cache = open("publish-message.cache", "a")
        cache.write(data)

    def get_all_local_storrage(self):
        lines = [line.rstrip('\n') for line in open("publish-message.cache")]
        logging.info("Retriieved all local data: %s" % lines)
        return lines

    def callback_status(self, publish_message):
        if not publish_message.exception(timeout=30):
            logging.info("Message Confirmation: %s"%publish_message.result())
        else:
            logging.info("Message")

    def check_internet(self):
        url = 'http://www.google.com/'
        timeout = 5
        try:
            _ = requests.get(url, timeout=timeout)
            logging.info("Internet connectivity")
            return True
        except requests.ConnectionError:
            logging.info("No internet connectivity")
            return False







