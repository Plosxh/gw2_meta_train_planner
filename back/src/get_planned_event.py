import boto3
import os
import json

def handler(event,context):

    session = boto3.Session(region_name="eu-west-1")
    dynamo = session.resource("dynamodb")
    event_table = dynamo.Table(os.environ["DynamoDBEventTable"])

    response = event_table.scan(
        ProjectionExpression="#name, #next_occurrence, #link, #waypoint",
        ExpressionAttributeNames={
            "#name": "name",
            "#next_occurrence": "next_occurrence",
            "#link": "link",
            "#waypoint": "waypoint"
        }
    )
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(response["Items"])
    }




if __name__ == '__main__':
    handler("","")