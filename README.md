# Projeto 2: Arquitetura Orientada a Eventos (Event-Driven)

Arquitetura desacoplada e assíncrona utilizando FastAPI, Amazon SQS e Amazon DynamoDB, provisionada localmente via LocalStack.

## Fluxo da Solução

1. Cliente HTTP (Swagger) -> POST /pedidos
2. FastAPI (Produtor) -> Envia mensagem para a fila SQS
3. Amazon SQS (Fila) -> Retém o evento de forma assíncrona
4. Worker Python (Consumidor) -> Lê a mensagem da fila SQS
5. Worker Python -> Grava no Amazon DynamoDB e remove a mensagem da fila

## Conceitos Chave (AWS SAA-C03)

- Desacoplamento: API e banco de dados funcionam de forma independente.
- Processamento Assíncrono: Resposta HTTP 201 Created imediata ao cliente.
- Ciclo de Vida SQS: Remoção da mensagem via ReceiptHandle após confirmação de escrita.

## Tecnologias

- Python 3.10+ (FastAPI, Boto3, Pydantic, Uvicorn)
- AWS LocalStack (SQS e DynamoDB)
- Docker & Docker Compose

## Como Executar

1. Subir contêineres:
   docker compose up -d

2. Criar recursos AWS:
   python src/setup_aws_local.py

3. Rodar API:
   uvicorn src.api:app --reload

4. Rodar Worker:
   python src/worker.py

5. Consultar Banco:
   python src/check_db.py