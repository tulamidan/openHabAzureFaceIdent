#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
########### Python 2.7 #############
import httplib, urllib, base64, json

personGroupID = "group2" #TODO replace with your PersonGroupID

headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '000000000000000000000000', #TODO in the current version, the subscription key is found as "key1" in the Azure console
}

params = urllib.urlencode({
    # Request parameters
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'recognitionModel': 'recognition_02',
    'returnRecognitionModel': 'false',
    'detectionModel': 'detection_01',
})

try:
	img_filename = "/opt/openhab2/conf/scripts/current.jpg" #TODO Update your Path the file is stored in the current directory
        with open(img_filename, 'rb') as f:
          img_data = f.read()
	conn = httplib.HTTPSConnection('westeurope.api.cognitive.microsoft.com') #TODO choose your region
	conn.request("POST", "/face/v1.0/detect?%s" % params, img_data, headers)
	response = conn.getresponse()
	data = response.read()
	data = data[1:-1]	#the json parsing fails otherwise
	jsonResponse=json.loads(data)
	recognizedFace=jsonResponse["faceId"]	#in this case we will deal with only one face, if several faces are regonized the Azure algorithm decides which face comes first.
	#print("recognizedFace: ",recognizedFace) #the recognized faceId will be store on the server for 24h and can be access by the id for further analysis
	conn.close()

	################Here we create the second request to put a name -or rather ID- to the recognized face############
	headers = {
    	# Request headers
    	'Content-Type': 'application/json',
    	'Ocp-Apim-Subscription-Key': '000000000000000000000000', #TODO in the current version, the subscription key is found as "key1" in the Azure console
	}
	body2 = '{"personGroupId":"'+personGroupID+'", "faceIds": ["'+recognizedFace+'"],"maxNumOfCandidatesReturned": 1,"confidenceThreshold": 0.65}' # the confidence threshold will tell you how likely the person was identified. you might need to tweak the value to your needs.
	conn2 = httplib.HTTPSConnection('westeurope.api.cognitive.microsoft.com') #TODO choose your region
	conn2.request("POST", "/face/v1.0/identify?%s" % params, body2, headers)
	response = conn2.getresponse()
        data2 = response.read()
	data2 = data2[1:-1]
	#print("raw data 2: ", data2)
	identifiedFace=json.loads(data2)
	face =  identifiedFace['candidates'][0]['personId']
	print(face) #this will give you the ID of the face that you have previously created most likely via Postman. You need to keep a record of these IDs. In a subsequent step you can map this ID to a name

	conn2.close
except Exception as e:
	print(e)
