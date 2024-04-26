import boto3
from botocore.exceptions import ClientError
import requests, json, time

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
            print("no messages in queue")
            return None

    except ClientError as e:
        print(e.response['Error']['Message'])

messages = []
blanks = 0
while len(messages)<10 and blanks<50:
    message = get_message()
    if(message):
        messages.append(message)
    else:
        time.sleep(0.5)
        blanks+=1

sorted_messages = sorted(messages, key=lambda x: x["order"])

for message in sorted_messages:
    print(message["word"]
    delete_message(message["handle"])