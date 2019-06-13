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
        self.cache_file = "publish-message.cache"
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(project_id, topic_name)

    def publish_to_topic_new(self,data:str):
        logging.info("Sending attempt for data: %s"% data)
        message = data.encode('utf-8')
        if self.check_internet():
            publish_message = self.publisher.publish(self.topic_path,data=message)
            publish_message.add_done_callback(self.callback_status) #validate if it was sent succesfully
        else:
            self.save_to_local_storrage(data)

    def publish_to_topic_old(self,data:str):
        logging.info("Sending attempt for data: %s"% data)
        message = data.encode('utf-8')
        publish_message = self.publisher.publish(self.topic_path,data=message)
        publish_message.add_done_callback(self.callback_status) #validate if it was sent succesfully


    def callback_status(self, publish_message):
        if not publish_message.exception(timeout=5):
            logging.info("Message Confirmation: %s"%publish_message.result())
            self.sent_local_storrage()
        else:
            logging.info("Message sending failed...")

    def save_to_local_storrage(self, data):
        logging.info("Localy caching the following message: %s"%data)
        cache = open(self.cache_file, "a")
        cache.write("%s \n" % data)
        cache.close()

    def get_all_local_storrage(self):
        lines = [line.rstrip('\n') for line in open(self.cache_file)]
        open(self.cache_file, 'w').close()
        logging.info("Retrieved all local data: %s" % lines)
        return lines

    def sent_local_storrage(self):
        lines_failed = []
        lines = self.get_all_local_storrage()
        if lines:
            for line in lines:
                if self.check_internet():
                    self.publish_to_topic_old(line)
                else:
                    lines_failed.append(line)
        else:
            logging.info("No local cache")
        cache = open(self.cache_file, "a")
        for line in lines_failed:
            cache.write("%s \n" % line)

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







