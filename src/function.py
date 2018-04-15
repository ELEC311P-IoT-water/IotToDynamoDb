import os
from time import time
import boto3

def lambda_handler(event, context):
    timestamp = time() # time of arrival
    table = os.environ["tablename"]
    client = boto3.client("dynamodb")

    item = {}
    item["sensorId"] = {"N" : str(event["id"]) }
    item["timestamp"] = { "N" : str(timestamp) }
    item["moisture"] = {"N" : str(event["moisture"]) }
    resp = client.put_item(TableName = table, Item = item)
    return resp
