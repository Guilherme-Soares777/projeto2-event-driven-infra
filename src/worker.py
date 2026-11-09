import os
import json
import time
import boto3
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv("AWS_ENDPOINT_URL", "http://127.0.0.1:4566")
region = os.getenv("AWS_REGION", "us-east-1")
queue_name = os.getenv("QUEUE_NAME", "fila-pedidos")
table_name = os.getenv("TABLE_NAME", "tabela-pedidos")

sqs = boto3.client(
    'sqs',
    endpoint_url=endpoint,
    region_name=region,
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url=endpoint,
    region_name=region,
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

def processar_mensagens():
    queue_url = sqs.get_queue_url(QueueName=queue_name)['QueueUrl']
    table = dynamodb.Table(table_name)
    
    print("⚙️ Worker ativado! Aguardando mensagens na fila SQS...")

    while True:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=5
        )

        messages = response.get('Messages', [])
        for message in messages:
            body = json.loads(message['Body'])
            print(f"\n📥 Mensagem recebida da SQS: Pedido {body['pedido_id']} ({body['cliente']})")

            # Persistir no DynamoDB
            item_dynamo = {
                "pedido_id": body['pedido_id'],
                "cliente": body['cliente'],
                "item": body['item'],
                "valor": str(body['valor']),
                "status": "CONCLUIDO"
            }
            table.put_item(Item=item_dynamo)
            print(f"💾 Pedido {body['pedido_id']} persistido no DynamoDB!")

            # Deletar da SQS após processar
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=message['ReceiptHandle']
            )
            print(f"🗑️ Mensagem removida da fila SQS com sucesso.")

        time.sleep(1)

if __name__ == "__main__":
    processar_mensagens()