import boto
import boto.sqs
import sys

from boundary_aws_plugin.cloudwatch_plugin import CloudwatchPlugin
from boundary_aws_plugin.cloudwatch_metrics import CloudwatchMetrics


class SqsCloudwatchMetrics(CloudwatchMetrics):
    def __init__(self, access_key_id, secret_access_key):
        return super(SqsCloudwatchMetrics, self).__init__(access_key_id, secret_access_key, 'AWS/SQS')

    def get_region_list(self):
        # Some regions are returned that actually do not support SQS.  Skip those.
        return [r for r in boto.sqs.regions() if r.name not in ['cn-north-1', 'us-gov-west-1']]

    def get_entities_for_region(self, region):
        sqs = boto.connect_sqs(self.access_key_id, self.secret_access_key, region=region)
        return sqs.get_all_queues()

    def get_entity_dimensions(self, region, q):
        return dict(QueueName=q.name)

    def get_entity_source_name(self, q):
        return q.name

    def get_metric_list(self):
        return (
            ('NumberOfMessagesSent', 'Sum', 'AWS_SQS_NUMBER_OF_MESSAGES_SENT'),
            ('SentMessageSize', 'Sum', 'AWS_SQS_SENT_MESSAGE_SIZE'),
            ('NumberOfMessagesReceived', 'Sum', 'AWS_SQS_NUMBER_OF_MESSAGES_RECEIVED'),
            ('NumberOfEmptyReceives', 'Sum', 'AWS_SQS_NUMBER_OF_EMPTY_RECEIVES'),
            ('NumberOfMessagesDeleted', 'Sum', 'AWS_SQS_NUMBER_OF_MESSAGES_DELETED'),
            ('ApproximateNumberOfMessagesDelayed', 'Average', 'AWS_SQS_NUMBER_OF_MESSAGES_DELAYED'),
            ('ApproximateNumberOfMessagesVisible', 'Average', 'AWS_SQS_NUMBER_OF_MESSAGES_VISIBLE'),
            ('ApproximateNumberOfMessagesNotVisible', 'Average', 'AWS_SQS_NUMBER_OF_MESSAGES_NOT_VISIBLE'),
        )

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '-v':
        import logging
        logging.basicConfig(level=logging.INFO)

    plugin = CloudwatchPlugin(SqsCloudwatchMetrics, '', 'boundary-plugin-aws-sqs-python-status')
    plugin.main()
