import json
import boto3
import datetime
import dateutil.parser
import math
import os
import time

sqs = boto3.client('sqs')
queue_url = 'https://sqs.us-east-1.amazonaws.com/837466521382/Q1'

def get_slots(event):
    return event['currentIntent']['slots']
    
def assign(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }
    
def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }
    return response


def check_for_errors(is_valid, violated_slot, message_content):
    if message_content is None:
        return {
            "isValid": is_valid,
            "violatedSlot": violated_slot
        }

    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }

def isvalid_date(date):
    try:
        dateutil.parser.parse(date)
        return True
    except ValueError:
        return False


def parse_int(n):
    try:
        return int(n)
    except ValueError:
        return float('nan')


def validate_inputs(totalCount, date):
    if totalCount is not None:
        if(int(totalCount) < 0):
            return check_for_errors(False, 'TotalCountType',
                                        'Incorrect input for number of people.')
        

    if date is not None:
        if not isvalid_date(date):
            return check_for_errors(False, 'DateType',
                                           'I did not understand that, what date would you like to book?')
        elif datetime.datetime.strptime(date, '%Y-%m-%d').date() < datetime.date.today():
            return check_for_errors(False, 'DateType', 'Sorry wrong date inserted, please enter date again')

    return check_for_errors(True, None, None)



def lambda_handler(event, context):
    print(event)
    #slots = {}
    
    if event["currentIntent"]["name"] == "GreetingIntent":
        response = {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText", 
                    "content": "Hi there, how can I help you?"
                }
            }
        }
        return response
        #response["dialogAction"]["message"]["content"] = "Hi there, how can I help you?"
    elif event["currentIntent"]["name"] == "ThankYouIntent":
        response = {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",   
                    "content": "Until next time :)"
                }
            }
        }
        return response
    elif event["currentIntent"]["name"] == "DiningSuggestionIntent":
        CuisineType = event["currentIntent"]["slots"]["CuisineType"]
        TotalCountType = event["currentIntent"]["slots"]["TotalCountType"]
        PhoneNumber = event["currentIntent"]["slots"]["PhoneNumber"]
        AreaType = event["currentIntent"]["slots"]["AreaType"]
        DateType = event["currentIntent"]["slots"]["DateType"]
        TimeType = event["currentIntent"]["slots"]["TimeType"]
        EmailType = event["currentIntent"]["slots"]["EmailType"]
        
        source = event['invocationSource']
        if source == 'DialogCodeHook':
            slots = get_slots(event)
            validation_result = validate_inputs(TotalCountType, DateType)
    
            if not validation_result['isValid']:
                slots[validation_result['violatedSlot']] = None
                return elicit_slot(event['sessionAttributes'],
                                   event['currentIntent']['name'],
                                   slots,
                                   validation_result['violatedSlot'],
                                   validation_result['message'])
    
            if event['sessionAttributes'] is not None:
                output_session_attributes = event['sessionAttributes']
            else:
                output_session_attributes = {}
    
            return assign(output_session_attributes, get_slots(event))
    
        # Send message to SQS queue
        
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
        
        response = {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",    
                    "content": "You’re all set. Expect my suggestions shortly! Have a good day."
                }
            }
        }
    
    
    return response
    
