import requests
from google.cloud import pubsub_v1
import logging
import os

logging.basicConfig(filename='tools/CloudManager.log',level=logging.INFO)

class CloudManager():
    def __init__(self, project_id, topic_name):
        logging.info("Initialized cloud manager with project-id: %s and topic-name: %s"% (project_id,topic_name))
        self.cache_file = "tools/publish-message.cache"
        self.cache_file_local = "publish-message.cache"
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(project_id, topic_name)


    """
    The following function is there to send the data to the cloud, this function will be the only one that is used outside of the class.
    """
    def publish_to_topic(self,data:str):
        logging.info("Sending attempt for data: %s"% data)
        message = data.encode('utf-8')
        if self.check_internet():
            publish_message = self.publisher.publish(self.topic_path,data=message)
            logging.info("Message Confirmation: %s" % publish_message.result())
            if not publish_message.result() == None:
                lines = self.get_all_local_storage()
                if lines:
                    self.sent_local_storage(lines)
            #publish_message.add_done_callback(self.callback_status) #validate if it was sent succesfully
        else:
            self.save_to_local_storage(data)

    """
    This callback function is unused, since it did create some problems, now we simply use the .result() as verification if it got send succesfully.
    This causes the error handeling to be less effecient, however the change that google cloud is unavailable is so low that this should not 
    drasticly interfere the propper functioning of our program.
    """
    def callback_status(self, publish_message):
        if not publish_message.exception(timeout=5):
            logging.info("Message Confirmation: %s"%publish_message.result())
            #self.sent_local_storrage()
        else:
            logging.info("Message sending failed...")

    """ 
    This function will write the `data` to the local cache file 
    """
    def save_to_local_storage(self, data):
        logging.info("Localy caching the following message: %s"%data)
        cache = open(self.cache_file, "a")
        cache.write("%s \n" % data.replace('"',""))
        cache.close()


    """
    This function will read the local data from the CloudManager.cache and clear the entire file.
    """
    def get_all_local_storage(self):
        try:
            lines = [line.rstrip('\n') for line in open(self.cache_file)]
            open(self.cache_file, 'w').close()
        except:
            lines = [line.rstrip('\n') for line in open(self.cache_file_local)]
            open(self.cache_file_local, 'w').close()
        logging.info("Retrieved all local data: %s" % lines)
        return lines
    """
    This function will retreave all the messages in the CloudManager.cache and send them to the cloud one by one
    """
    def sent_local_storage(self, lines):
        lines_failed = []
        if lines:
            for line in lines:
                if self.check_internet():
                    self.publish_to_topic(line)
                else:
                    lines_failed.append(line)
        else:
            logging.info("No local cache")
        try:
            cache = open(self.cache_file, "w")
        except:
            cache = open(self.cache_file_local, "w")
        for line in lines_failed:
            cache.write("%s \n" % line)
    """
    This function will check if there is internet connectivity
    """
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
