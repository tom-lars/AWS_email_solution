import json
import boto3
import os

sqs = boto3.client('sqs')

def lambda_handler(event, context):
    queue_url = os.environ['SQS_QUEUE_URL']

    try:
        body = json.loads(event['body'])
        
        subject = body['subject']
        message_body = body['body']
        recipients = body['recipients']

        # Send message to SQS
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps({
                'subject': subject,
                'body': message_body,
                'recipients': recipients
            })
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'messageId': response['MessageId']})
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
