import json
import boto3
import logging

dynamodb = boto3.client('dynamodb')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def delete_todo(id):
    #if get_todo(id) is None:
    #    return 409, 'Item does not exist' # Ma ce ne frega relativamente poco
    try:
        dynamodb.delete_item(
            TableName='todos',
            Key={'id': {
                'N': str(id),
            }}
        )
        return 200,'Deleted successfully'
    except Exception as e:
        return 405, 'Exception at deleting item' + str(e)

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
    st, opt = delete_todo(event['id'])
    return reply(st,json.dumps(opt))