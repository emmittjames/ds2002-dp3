import boto3
from botocore.exceptions import ClientError
import requests
import json

url = "https://sqs.us-east-1.amazonaws.com/440848399208/gwu8ek"
sqs = boto3.client('sqs')

def delete_message(handle):
    try:
        sqs.delete_message(
            QueueUrl=url,
            ReceiptHandle=handle
        )
        print("Message deleted")
    except ClientError as e:
        print(e.response['Error']['Message'])

def get_message():
    try:
        response = sqs.receive_message(
            QueueUrl=url,
            AttributeNames=[
                'All'
            ],
            MaxNumberOfMessages=1,
            MessageAttributeNames=[
                'All'
            ]
        )
        if "Messages" in response:
            order = response['Messages'][0]['MessageAttributes']['order']['StringValue']
            word = response['Messages'][0]['MessageAttributes']['word']['StringValue']
            handle = response['Messages'][0]['ReceiptHandle']

            print(f"Order: {order}")
            print(f"Word: {word}")
            return {"order":order, "word":word, "handle":handle}

        else:
            print("No messages in the queue")
            return -1
            
    except ClientError as e:
        print(e.response['Error']['Message'])

messages = []
for i in range(9):
    message = get_message()
    if(message):
        messages.append(message)
    else:
        break

print(messages)