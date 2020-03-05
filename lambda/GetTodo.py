import json
import boto3
import logging

dynamodb = boto3.client('dynamodb')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_todo(id):
  try:
    res = dynamodb.get_item(
        TableName='todos',
        Key={'id': {
            'N': str(id),
        }},
        AttributesToGet=['id', 'description','completed'],
        ConsistentRead=False,
        ReturnConsumedCapacity='NONE',
    )
    return res
  except:
    return None

def get_t(event):
    if event.get("id","") == "": # List all
      res = dynamodb.scan(
          TableName='todos',
          AttributesToGet=['id', 'description','completed'],
          Limit=10000
      )
      return 200, res.get("Items","")
    a = get_todo(int(event["id"]))
    if a is None:
        return 409 , 'Wrong id'
    logger.info(a["Item"])
    return 200, a["Item"]

def reply(code,message):
    return {'statusCode': int(code),'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT,DELETE"
                },
            'body': message}

def lambda_handler(event, context):
    if "body" in event.keys(): # hits True when sending an API, False in test
        if event["body"] is None:
            return reply(200,"Options ")
        event = json.loads(event["body"])
    st, opt = get_t(event)
    return reply(st,json.dumps(opt))