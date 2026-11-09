import os
import json
import boto3
from dotenv import load_dotenv

load_dotenv()

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url=os.getenv("AWS_ENDPOINT_URL", "http://127.0.0.1:4566"),
    region_name=os.getenv("AWS_REGION", "us-east-1"),
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

table = dynamodb.Table("tabela-pedidos")
response = table.scan()

print("📊 Registos gravados no DynamoDB:")
print(json.dumps(response.get('Items', []), indent=2))