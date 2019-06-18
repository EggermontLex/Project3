try:
    from tools.CloudManager import CloudManager
except:
    from cloud_manager import CloudManager

cmng = CloudManager("Project3-ML6","data_register")
cmng.publish_to_topic("+1,2019-06-13 13:07:05.604307")