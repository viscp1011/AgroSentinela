"""
lambda_alerta.py - AgroSentinela (AWS Lambda SIMULADO). Caps. 5 e 6.
Acionada pela fila SQS quando o ESP32 envia leitura; avalia risco e publica
alerta no SNS (SMS/voz) + grava no DynamoDB.
"""
import os, json, datetime as dt
try:
    import boto3
    sns = boto3.client("sns"); dynamo = boto3.resource("dynamodb")
except Exception:
    sns = None; dynamo = None
LIMIAR = float(os.environ.get("LIMIAR_CRITICO", "0.20"))
TOPICO = os.environ.get("TOPICO_ALERTAS", "")
TABELA = os.environ.get("TABELA", "agrosentinela-leituras")

def avaliar(leitura): return leitura["umidade_solo"] < LIMIAR

def handler(event, context):
    processadas = 0; alertas = 0
    for registro in event.get("Records", []):
        leitura = json.loads(registro["body"]); processadas += 1
        if dynamo:
            dynamo.Table(TABELA).put_item(Item={"id_fazenda":leitura["id_fazenda"],
                "timestamp":dt.datetime.utcnow().isoformat(),"umidade_solo":str(leitura["umidade_solo"])})
        if avaliar(leitura):
            alertas += 1
            msg = ("Risco hidrico na fazenda " + leitura["id_fazenda"] + ": umidade " +
                   str(leitura["umidade_solo"]) + " m3/m3 (limiar " + str(LIMIAR) + ").")
            if sns and TOPICO: sns.publish(TopicArn=TOPICO, Subject="AgroSentinela - Alerta", Message=msg)
            print("[SNS] " + msg)
    return {"processadas": processadas, "alertas": alertas}

if __name__ == "__main__":
    ev = {"Records":[{"body":json.dumps({"id_fazenda":"campo-soja","umidade_solo":0.15})},
                     {"body":json.dumps({"id_fazenda":"campo-soja","umidade_solo":0.27})}]}
    print(handler(ev, None))
