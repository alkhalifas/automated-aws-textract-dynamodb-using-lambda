import json
import boto3
import os
import urllib.parse
import json
import uuid
from decimal import Decimal
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
def lambda_handler(event, context): 
    print("Starting Transfer:")
    bucket = event['Records'][0]['s3']['bucket']['name']
    json_file_name = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    json_object = s3_client.get_object(Bucket = bucket, Key = json_file_name)
    jsonFileReader = json_object['Body'].read()
    jsonDict = json.loads(jsonFileReader, parse_float=Decimal)
    table = dynamodb.Table('s3-json-textract-table') 
    finalObject = jsonDict[0]
    finalObject["key"] = json_file_name
    finalObject['id'] = str(uuid.uuid4())
    table.put_item(Item = jsonDict[0])