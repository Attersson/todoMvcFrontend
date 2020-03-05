import json
import logging
import boto3

dynamodb = boto3.client('dynamodb')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_all_todos_ids():
    res = dynamodb.scan(
        TableName='todos',
        AttributesToGet=['id', 'description','completed'],
        Limit=10000
    )
    return list(sorted(int(todo["id"]["N"]) for todo in res.get("Items",[])))

def first_missing(lst, start, end): 
    if (start > end): 
        return end + 1
    if (start != lst[start]): 
        return start; 
    mid = int((start + end) / 2) 
    if (lst[mid] == mid): 
        return first_missing(lst, mid+1, end) 
    return first_missing(lst, start, mid)

def find_least_unused_id():
    ids = get_all_todos_ids()
    n = len(ids)
    logger.info("All ids are {} and their length is {}".format(str(ids),str(n)))
    return 0 if n == 0 else first_missing(ids, 0, n-1)

def insert_data(event):
    if any(x not in event for x in ("description", "completed")):
        return 405, 'Request does not contain description or completed'
    if 'id' not in event:
        event['id'] = find_least_unused_id()
    try:
        dynamodb.update_item(
            TableName='todos',
            Key={
                'id': {
                    'N': str(event['id'])
                }
            },
            UpdateExpression="SET description = :ds, completed = :cm",
            ExpressionAttributeValues={
                ":ds": {
                    "S": str(event["description"])
                },
                ":cm": {
                    "BOOL": event["completed"]
                }
            })
    except Exception as e:
        return 409, 'insert_data() dynamodb.update_item exception' + str(e)
    return 200, ""

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
    st, error = insert_data(event)
    b = 'TodoNew request ' + ('was successful.' if st == 200 else error)
    return reply(st, b)