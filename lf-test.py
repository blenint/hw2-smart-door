import base64
import boto3
import json
import cv2
#serious bug
import time
import sys
from datetime import datetime
from botocore.exceptions import ClientError

sys.path.append("/opt")
dynamodb = boto3.resource('dynamodb')


def getRawData(fragNumber):
    client = boto3.client('kinesisvideo')
    response = client.get_data_endpoint(
        StreamARN='arn:aws:kinesisvideo:us-east-1:376885051186:stream/KVS1/1606199325135',
    )
    videoClient = boto3.client('kinesis-video-archived-media',endpoint_url=response['DataEndpoint'])
    stream = videoClient.get_media_for_fragment_list(
        StreamName='KVS1',
        Fragments=[fragNumber]
    )
    chunk = stream['Payload'].read()
    return chunk


def imgToS3(img, fileName):
    s3Client = boto3.client('s3')
    if fileName is None:
        s3Client.put_object(Body=img, Bucket='cs-gy-9223-hw2-b1', Key=str(int(time.time())), ContentType='image/jpeg')
    else:
        s3Client.put_object(Body=img, Bucket='cs-gy-9223-hw2-b1', Key=fileName, ContentType='image/jpeg')


def allFaces():
    rekognition_client = boto3.client('rekognition')
    response = rekognition_client.list_faces(
        CollectionId='faces',
        MaxResults=10
    )
    print(response)


def visitorIndex(visitor_img):
    client = boto3.client('rekognition')
    response = client.index_faces(
        CollectionId='faces',
        Image={'Bytes': visitor_img},
        DetectionAttributes=['ALL'],
        MaxFaces=1,
        QualityFilter='AUTO'
    )
    faceId = response['FaceRecords'][0]['Face']['FaceId']
    return faceId


def searchDynamoDB(face_id):
    print('TD')
    # TD


def sendEmail():
    client = boto3.client('ses')
    response = client.send_email(
        Source='xzj354@gmail.com',
        Destination={'ToAddresses': ['xzj354@gmail.com']},
        Message={
            'Subject': {
                'Charset': 'UTF-8',
                'Data': 'Face Dectected'
            },
            'Body': {
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': 'Face Dectected! Maya 99.7652'
                },
            }
        }
    )
    print(response)
    # print(response)


def getPicArray(faceId):
    table = dynamodb.Table('visitor')
    try:
        response = table.get_item(Key={'faceId': faceId})
    except ClientError as e:
        print('e', e)
    else:
        item = response['Item']
        photoArray = item['photos']
        return photoArray


def addPic(bucket, objectKey, createdTimestamp, old_array):
    item = dict()
    item['bucket'] = bucket
    item['objectKey'] = objectKey
    item['createdTimestamp'] = createdTimestamp
    old_array.append(item)
    return old_array


def updateDynamoDB(faceId, new_array):
    table = dynamodb.Table('visitors')
    response = table.update_item(
        Key={'faceId': faceId},
        UpdateExpression="set photos=:a",
        ExpressionAttributeValues={':a': new_array},
        ReturnValues="UPDATED_NEW"
    )
    print(response)
    # print(response)


def sendSMS(phoneNumber, name, OTP):
    client = boto3.client("sns", region_name='us-west-2')
    message = 'Hello, {}!\r\nYou are allowed to enter with OTP'.format(name, OTP)
    response = client.publish(
        PhoneNumber=phoneNumber,
        Message=message
    )
    print(response)


def lambda_handler(event, context):
    records = event["Records"]
    data = json.loads(
        base64.b64decode(records[0]["kinesis"]["data"]).decode("utf-8")
    )
    allFaces()
    face = data['FaceSearchResponse'][0]
    if len(face['MatchedFaces']) == 0 or face['MatchedFaces'][0]['Similarity'] < 10:
        print('Email sent time:' + str(time.time()))
    else:
        faceID = face['MatchedFaces'][0]['Face']['FaceId']
        (visitorName, visitorPhone) = searchDynamoDB(faceID)
        timeStr = str(time.time()).split(".")
        visitorFilename = timeStr[0]
        datetimeObj = datetime.now()
        visitorTimeStamp = str(datetimeObj)
        imgToS3(visitorImg, visitorFilename)
        # imgToS3(visitorImg, visitor_photo_filename)
        photos_array = addPic('cs-gy-9223-hw2-b1', visitorFilename, visitorTimeStamp, getPicArray(faceID))
        updateDynamoDB(faceID, photos_array)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
