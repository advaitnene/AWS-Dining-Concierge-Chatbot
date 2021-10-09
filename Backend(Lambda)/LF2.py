
import json, boto3
import requests
from requests_aws4auth import AWS4Auth

senderEmailId = "advaitnene@gmail.com"

"""
def verify_email_identity():
    ses_client = boto3.client("ses", region_name="us-east-1")
    response = ses_client.verify_email_identity(
        EmailAddress="advaitnene@gmail.com"
    )
    print(response)


def send_plain_email(EmailType, msg):
    ses_client = boto3.client("ses", region_name="us-east-1")
    CHARSET = "UTF-8"

    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                EmailType,
            ],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": msg,
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "Recommendations for restaurants",
            },
        },
        Source="advaitnene@gmail.com",
    )
"""

# Lambda execution starts here
def lambda_handler(event, context):
    print(event)
    
    CuisineType = event['Records'][0]['messageAttributes']['CuisineType']['stringValue']
    DateType = event['Records'][0]['messageAttributes']['DateType']['stringValue']
    PhoneNumber = event['Records'][0]['messageAttributes']['PhoneNumber']['stringValue']
    TotalCountType = event['Records'][0]['messageAttributes']['TotalCountType']['stringValue']
    TimeType = event['Records'][0]['messageAttributes']['TimeType']['stringValue']
    AreaType = event['Records'][0]['messageAttributes']['AreaType']['stringValue']
    EmailType = event['Records'][0]['messageAttributes']['EmailType']['stringValue']
    
    region = 'us-east-1' # For example, us-west-1
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
    
    ses = boto3.client('ses')
    verifiedResponse = ses.list_verified_email_addresses()
    if EmailType not in verifiedResponse['VerifiedEmailAddresses']:
        verifyEmailResponse = ses.verify_email_identity(EmailAddress=EmailType)
        print(verifyEmailResponse)
        return
    
    
    #sqs = boto3.client('sqs')
    #queue_url = 'https://sqs.us-east-1.amazonaws.com/837466521382/Q1'
    # The OpenSearch domain endpoint with https://
    host = 'https://search-restaurants-yweibjjzcdubo3tnlsc6ey5wne.us-east-1.es.amazonaws.com'
    index = 'restaurants'
    url = host + '/' + index + '/_search'
    
    #qry = event['queryStringParameters']['q']
    #qry = 'test'
    qry = CuisineType
    print(qry)

    # Put the user query into the query DSL for more accurate search results.
    # Note that certain fields are boosted (^).
    query = {
        "size": 3,
        "query": {
            "multi_match": {
                "query": qry,
                "fields": ["cuisines"]
            }
        }
    }

    # Elasticsearch 6.x requires an explicit Content-Type header
    headers = { "Content-Type": "application/json" }

    # Make the signed HTTP request
    r = requests.get(url, auth=awsauth, headers=headers, data=json.dumps(query))
    
    response_data = []
    response_data = r.json()
    
    hits = []
    restIdList = []
    result_data = []
    
    
    hits = response_data["hits"]["hits"]
    print('I am here 3 ', hits)
    for hit in hits:
        source = hit["_source"]
        name = source["id"]
        restIdList.append(name)
    print("restIdList is ", restIdList)
    
    dynamoClient = boto3.client('dynamodb')
    for restaurantId in restIdList:
        res = dynamoClient.get_item(Key={'RestaurantID': { 'S': restaurantId } }, TableName='yelp_restaurants')
        result_data.append(res)
    
    print("Result data is ", result_data)
    
    if(len(result_data) > 0 and result_data[0]['Item']):
        msg = "Hello! Here are my " + str(CuisineType) + " type restaurant suggestions for " + str(TotalCountType) + " people, for " + str(DateType) + " at " + str(TimeType) + "."
        for m in range(len(result_data)):
            L = result_data[m]['Item']['Address']
            print(L)
            S1 = L['S']
            print(S1)
            msg = msg + " " + str(m + 1) + ") " +  str(result_data[m]['Item']['Name']['S']) + " located in " + str(S1) + "."
        
        msg = msg + "Enjoy your meal!"
        print(msg)
    else:
        msg = "Sorry there are no restaurants matching your description."
        print(msg)
    
        
    
    mailResponse = ses.send_email(
        Source=senderEmailId,
        Destination={'ToAddresses': [EmailType]},
        Message={
            'Subject': {
                'Data': "Dining Conceirge Chatbot has a message for you!",
                'Charset': 'UTF-8'
            },
            'Body': {
                'Text': {
                    'Data': msg,
                    'Charset': 'UTF-8'
                },
                'Html': {
                    'Data': msg,
                    'Charset': 'UTF-8'
                }
            }
        }
    )
    
    # Create the response and add some extra content to support CORS
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": '*'
        },
        "isBase64Encoded": False
    }

    response['body'] = "Hello"
    return response
    
