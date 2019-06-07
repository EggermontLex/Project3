from google.cloud import pubsub_v1

project_id = "Project3-ML6"
topic_name = "telemetry-topic"

publisher = pubsub_v1.PublisherClient()
# The `topic_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/topics/{topic_name}`
topic_path = publisher.topic_path(project_id, topic_name)

data = "twerkt"
data = data.encode('utf-8')
future = publisher.publish(topic_path, data=data)
print('Published {} of message ID {}.'.format(data, future.result()))

print('Published messages.')
