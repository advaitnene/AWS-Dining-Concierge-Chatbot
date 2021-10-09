
import json
import csv
import boto3

def lambda_handler(event, context):
    region = 'us-east-1'
    record_list = []
    
    try:
        s3 = boto3.client('s3')
        
        dynamodb = boto3.client('dynamodb',region_name = region)
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        
        print('Bucket: ', bucket, ' Key: ', key)
        
        csv_file = s3.get_object(Bucket = bucket, Key = key)
        
        record_list = csv_file['Body'].read().decode('utf-8').split('\n')
        
        csv_reader = csv.reader(record_list, delimiter=',', quotechar='"')
        
        for row in csv_reader:
            RestaurantID = row[0]
            Name = row[1]
            Cuisine = row[2]
            Rating = row[3]
            NumberOfReviews = row[4]
            Address = row[5]
            ZipCode = row[6]
            Latitude = row[7]
            Longitude = row[8]
            IsClosed = row[9]
            InsertTime = row[10]
            
            add_to_db = dynamodb.put_item(
                TableName = 'yelp_restaurants_final',
                Item = {
                    'RestaurantID': {'S': str(RestaurantID)},
                    'Name': {'S': str(Name)},
                    'Cuisine': {'S': str(Cuisine)},
                    'Rating': {'S': str(Rating)},
                    'NumberOfReviews': {'S': str(NumberOfReviews)},
                    'Address': {'S': str(Address)},
                    'ZipCode': {'S': str(ZipCode)},
                    'Latitude': {'S': str(Latitude)},
                    'Longitude': {'S': str(Longitude)},
                    'IsClosed': {'S': str(IsClosed)},
                    'InsertTime': {'S': str(IsClosed)},
                })
                
        
    except Exception as e:
        print(str(e))
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
