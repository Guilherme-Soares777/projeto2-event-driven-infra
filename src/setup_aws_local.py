import os
import boto3
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

endpoint = os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566")
region = os.getenv("AWS_REGION", "us-east-1")

# Conectores boto3 apontados para o LocalStack
sqs = boto3.client('sqs', endpoint_url=endpoint, region_name=region, aws_access_key_id='test', aws_secret_access_key='test')
dynamodb = boto3.client('dynamodb', endpoint_url=endpoint, region_name=region, aws_access_key_id='test', aws_secret_access_key='test')

def setup():
    print("🚀 Inicializando recursos da AWS local (LocalStack)...")

    # 1. Criar Fila SQS
    try:
        res_sqs = sqs.create_queue(QueueName=os.getenv("QUEUE_NAME", "fila-pedidos"))
        print(f"✅ Fila SQS criada/validada: {res_sqs['QueueUrl']}")
    except Exception as e:
        print(f"❌ Erro SQS: {e}")

    # 2. Criar Tabela DynamoDB
    try:
        res_db = dynamodb.create_table(
            TableName=os.getenv("TABLE_NAME", "tabela-pedidos"),
            KeySchema=[{'AttributeName': 'pedido_id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'pedido_id', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        print(f"✅ Tabela DynamoDB criada: {os.getenv('TABLE_NAME', 'tabela-pedidos')}")
    except dynamodb.exceptions.ResourceInUseException:
        print(f"✅ Tabela DynamoDB já existente.")
    except Exception as e:
        print(f"❌ Erro DynamoDB: {e}")

if __name__ == "__main__":
    setup()