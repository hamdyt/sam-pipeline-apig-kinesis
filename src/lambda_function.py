import json
import base64
import datetime
import uuid
import boto3
from decimal import Decimal

print('Loading function')

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
	print('------------------------')
	print(event)
	#1. Iterate over each record
	
	#print("test")
	
	try:
		for kinesisRecord in event['Records']:
			#2. Handle event by type
			
			record = base64.b64decode(kinesisRecord["kinesis"]["data"])
			record = json.loads(record.decode('utf-8'))
			partitionKey = kinesisRecord["kinesis"]["partitionKey"]
			
			epochTime = datetime.datetime.utcnow().timestamp()
			epochTime = json.loads(json.dumps(epochTime), parse_float=Decimal)
			
			pk = str(uuid.uuid1())
			
			print('Decoded record: {}, Partition Key: {}, Creation time: {}, Primary Key: {}'.format(record, partitionKey, epochTime, pk))
			
			table = dynamodb.Table("KinesisStreamData")
			# print(table.table_status)
			
			response = table.put_item(Item= {'pk': pk,'partitionKey':  partitionKey, 'data':  record, 'creationTime':  epochTime})
			# print(response)

		print('Success')
		# return "Success!"
	except Exception as e: 
		print(e)
		print('------------------------')
		# return "Error"