import boto3

pic = 'Jessica-Meir.JPG'

client = boto3.client('rekognition', 
                       aws_access_key_id = 'your aws access key id', 
                       aws_secret_access_key = 'your aws secret access key',
                       region_name = 'us-east-1')
                       
with open(pic, 'rb') as source_image:
	source_bytes = source_image.read()

response = client.detect_labels(Image={'Bytes': source_bytes}, MaxLabels=10, MinConfidence=90)

def label():
    for label in response['Labels']:
        print ("Label: " + label['Name'])
        print ("Confidence: " + str(label['Confidence']) + " %")
            
label()
