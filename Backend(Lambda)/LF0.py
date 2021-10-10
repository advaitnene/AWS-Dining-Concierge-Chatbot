import json, boto3

def lambda_handler(event, context):
    print(event)
    
    client = boto3.client('lex-runtime')
    
    """
    response = client.post_content(
        botName='BookHotel',
        botAlias='bookHotel',
        userId='1234',
        contentType='text/plain; charset=utf-8',
        accept='text/plain; charset=utf-8',
        inputStream='bytes'
        th0mazwn0nmg6z2jdtiwc91w41apcj5h
    )  
    """
    response = client.post_text(
        botName='BookHotel',
        botAlias='bookHotel',
        userId='123',
        inputText=event['messages'][0]['unstructured']['text'],
        activeContexts=[]
    )
    
    print(response)
    
    
    result = {
        "messages":[
            {
                "type":"unstructured",
                "unstructured":{
                "text":response['message']
                }
            }
        ]
            
    }
    
    return result
