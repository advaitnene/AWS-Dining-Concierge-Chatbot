import json
import boto3
import datetime

sqs = boto3.client('sqs')
queue_url = 'https://sqs.us-east-1.amazonaws.com/837466521382/Q1'

def get_slots(intent_request):
    return intent_request['currentIntent']['slots']

def lambda_handler(event, context):
    print(event)
    flag = True
    #slots = {}
    response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText"    
            }
        }
    }
    
    if event["currentIntent"]["name"] == "GreetingIntent":
        response["dialogAction"]["message"]["content"] = "Hi there, how can I help you?"
    elif event["currentIntent"]["name"] == "ThankYouIntent":
        response["dialogAction"]["message"]["content"] = "Until next time :)"
    elif event["currentIntent"]["name"] == "DiningSuggestionIntent":
        CuisineType = event["currentIntent"]["slots"]["CuisineType"]
    
        TotalCountType = event["currentIntent"]["slots"]["TotalCountType"]
        """
        if(isinstance(TotalCountType, int)):
            if(TotalCountType < 0):
                flag = False
                response["dialogAction"]["message"]["content"] = "Invalid input for number of people"
        else:
            flag = False
            response["dialogAction"]["message"]["content"] = "Invalid input for number of people"
        """
        
        PhoneNumber = event["currentIntent"]["slots"]["PhoneNumber"]
        AreaType = event["currentIntent"]["slots"]["AreaType"]
        
        DateType = event["currentIntent"]["slots"]["DateType"]
        
        """
        d = date.today()
        format = '%Y/%m/%d'
        dt = datetime.datetime.strptime(DateType, format)
        user_date = dt.date()
        
        
        if(user_date < d):
            flag = False
            response["dialogAction"]["message"]["content"] = "You have entered an incorrect date."
        """
        
        TimeType = event["currentIntent"]["slots"]["TimeType"]
        EmailType = event["currentIntent"]["slots"]["EmailType"]
        
        if(flag is True):
            response["dialogAction"]["message"]["content"] = "You’re all set. Expect my suggestions shortly! Have a good day."
    
        # Send message to SQS queue
        if(flag is True):
            result = sqs.send_message(
                QueueUrl=queue_url,
                DelaySeconds=10,
                MessageAttributes={
                    'CuisineType': {
                        'DataType': 'String',
                        'StringValue': CuisineType
                    },
                    'TotalCountType': {
                        'DataType': 'String',
                        'StringValue': TotalCountType
                    },
                    'PhoneNumber': {
                        'DataType': 'String',
                        'StringValue': PhoneNumber
                    },
                    'AreaType': {
                        'DataType': 'String',
                        'StringValue': AreaType
                    },
                    'DateType': {
                        'DataType': 'String',
                        'StringValue': DateType
                    },
                    'TimeType': {
                        'DataType': 'String',
                        'StringValue': TimeType
                    },
                    'EmailType': {
                        'DataType': 'String',
                        'StringValue': EmailType
                    }
                },
                MessageBody="Dining Concierge message from LF1 "
            )
            
        #print(result['MessageId'])
    
    
    return response
    
