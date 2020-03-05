import json
import logging
import boto3

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
        AttributesToGet=['id','description', 'completed'],
        ConsistentRead=False,
        ReturnConsumedCapacity='NONE',
    )
    return res
  except:
    return None

def set_todo(event):
    if any(x not in event for x in ("id","description","completed")):
        return 405, 'error: Request does not contain all fields.'
    if get_todo(int(event['id'])) is None:
        return 406, ' error: Todo does not exist.'
    try:
        dynamodb.update_item(
            TableName='todos',
            Key={'id':{'N':str(event['id'])}},
            UpdateExpression="SET description = :ds, completed = :cmp",
            ExpressionAttributeValues={
                ":ds":{"S":event["description"]},
                ":cmp":{"BOOL":event["completed"]},
            }
        )
    except Exception as e:
        return 409, 'Error: dynamodb.update_item exception ' + str(e)
    return 200, 'was successful.'

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
    logger.info('got event{}'.format(event))
    st, msg = set_todo(event)
    b = 'EditTodo request ' + msg
    return reply(st,b)