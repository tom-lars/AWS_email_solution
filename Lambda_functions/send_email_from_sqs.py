import boto3
import json
import os
import time
from botocore.exceptions import ClientError

ses = boto3.client('ses')
MAX_RETRIES = 5

def send_email(sender, recipients, subject, body_text):
    retry_count = 0
    backoff_time = 1

    while retry_count < MAX_RETRIES:
        try:
            response = ses.send_email(
                Source=sender,
                Destination={
                    'ToAddresses': recipients
                },
                Message={
                    'Subject': {'Data': subject},
                    'Body': {
                        'Text': {'Data': body_text},
                        'Html': {'Data': f"<p>{body_text}</p>"}
                    }
                }
            )
            print(f"Email sent! Message ID: {response['MessageId']}")
            return True

        except ClientError as e:
            error_code = e.response['Error']['Code']
            print(f"Error: {error_code}")

            if error_code in ['Throttling', 'ThrottlingException', 'LimitExceededException']:
                time.sleep(backoff_time)
                retry_count += 1
                backoff_time *= 2
            else:
                raise e

    print("Email send failed after retries.")
    return False

def lambda_handler(event, context):
    sender = os.environ['SENDER_EMAIL']

    for record in event['Records']:
        body = json.loads(record['body'])

        subject = body['subject']
        message_body = body['body']
        recipients = body['recipients']

        success = send_email(sender, recipients, subject, message_body)

        if not success:
            raise Exception("Failed to send email after retries.")

    return {
        'statusCode': 200,
        'body': json.dumps('Emails sent successfully.')
    }
