import boto3
import json

def get_dynamodb_table():
    dynamodb = boto3.resource("dynamodb")
    return dynamodb.Table("test-sls-dynamodb")

def create_response(status_code, message):
    return {"statusCode": status_code, "body": json.dumps(message)}

def put_item(event):
    table = get_dynamodb_table()
    table.put_item(
        Item={
            "userID": event["userID"],
            "address": event["address"],
            "age": event["age"],
            "name": event["name"],
            "phone": event["phone"],
        }
    )
    return create_response(200, "Item added successfully")



def get_item(event):
    table = get_dynamodb_table()
    response = table.get_item(Key={"userID": event["userID"]})
    item = response.get("Item")
    if item:
        return create_response(200, item)
    else:
        return create_response(404, "Item not found")

def update_item(event):
    table = get_dynamodb_table()
    table.update_item(
        Key={"userID": event["userID"]},
        UpdateExpression="set address=:a",
        ExpressionAttributeValues={":a": event["address"]},
        ReturnValues="UPDATED_NEW",
    )
    return create_response(200, "Item updated successfully")

def delete_item(event):
    table = get_dynamodb_table()
    table.delete_item(Key={"userID": event["userID"]})
    return create_response(200, "Item deleted successfully")

def lambda_handler(event, context):
    httpMethod = event["httpMethod"]
    if httpMethod == "POST":
        return put_item(event)
    elif httpMethod == "GET":
        return get_item(event)
    elif httpMethod == "PUT":
        return update_item(event)
    elif httpMethod == "DELETE":
        return delete_item(event)
    else:
        return create_response(400, "Invalid HTTP method")
