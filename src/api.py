import os
import json
import uuid
import boto3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="API de Pedidos - Event Driven Architecture")

# Configurações AWS LocalStack
endpoint = os.getenv("AWS_ENDPOINT_URL", "http://127.0.0.1:4566")
region = os.getenv("AWS_REGION", "us-east-1")
queue_name = os.getenv("QUEUE_NAME", "fila-pedidos")

# Cliente SQS direcionado ao LocalStack
sqs = boto3.client(
    'sqs',
    endpoint_url=endpoint,
    region_name=region,
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

# Schema de entrada do Pedido
class PedidoRequest(BaseModel):
    cliente: str
    item: str
    valor: float

@app.post("/pedidos", status_code=201)
def criar_pedido(pedido: PedidoRequest):
    try:
        # 1. Obter a URL da Fila SQS
        queue_url = sqs.get_queue_url(QueueName=queue_name)['QueueUrl']
        
        # 2. Gerar ID único para o pedido e criar o payload do evento
        pedido_id = str(uuid.uuid4())
        payload = {
            "pedido_id": pedido_id,
            "cliente": pedido.cliente,
            "item": pedido.item,
            "valor": pedido.valor,
            "status": "PROCESSANDO"
        }

        # 3. Enviar mensagem para a Fila SQS (Produtor de Evento)
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(payload)
        )

        return {
            "mensagem": "Pedido recebido e enviado para a fila SQS com sucesso!",
            "pedido_id": pedido_id,
            "sqs_message_id": response.get("MessageId")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao publicar no SQS: {str(e)}")

@app.get("/")
def health_check():
    return {"status": "API Event-Driven ativa"}