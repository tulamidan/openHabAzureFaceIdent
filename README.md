# OpenHab with Azure Face Identification
A set of tools to help you identify faces via your Openhab2 and a camera in your network using MS Azure cognitive AI.

Most of this applies no matter if you use Openhab. The core is a python script that takes an image as input and the result is an ID. This makes sense in an home automation environment to trigger a personalized set of rules depending on the person triggering it.


First you need an Azure account. You can register one for free. You can register one and sign up for the Cognitive service here: http://bit.ly/msCognitiveService

Then you will need to sign up for the Cognitive Services which is free too.  an add the "Face" Service


Here you need to set up the account which is pretty staight forward: Just make sure that you use the "Free" Version with 30k requests/month. Or feel free to pay if you need more. Also make sure to chose a datacenter near you to speed up processing.

Then you need to make sure to note down the key. We need Key1 for our entire task

The next thing you will need is a REST Client like Postman. For this exercise I have created a set of commands that are supposed to help you to get things going. You will first need to import the .json from the github repo and import it into Postman.

Next you need to update a few things as I did not create a global environment:

- The key: Ocp-Apim-Subscription-Key with your "Key1" , Azure does not use Oauth or SAML for these requests the key identifies you and your account.
- Your data center (e.g. westeurope)
- The person group
- The personId
- And basically you need to adapt each request with keys and IDs that are created in the process.

Make sure to read the API documentation: http://bit.ly/CognitiveAPI in combination with the postman collection you should be able to create your model in no time.

## Creating and training your model:

Here is the set of instructions you need to go through in order to get a working machine learning model:

- The first thing we need to create is a Person Group. This private Group can hold up to 1000 individuals. If you need more there is the LargePeronsGroup.
- In the Person Group we create a new Person (with the second post request) which will return a cryptic ID. KEEP THIS IN YOUR NOTES. Even when you add a name to the person you create - the Identification process will only tell you this ID when it recognizes someone. Do this step for each person you'd like to recognize.
- Add Face to Person: Here we will upload a good quality image of the (face of) the individual person. Only one face is allowed. This is the crutial part - if the image are bad - the recignizion is bad. I have uplaoaded only one image per person(make sure to update the personID) and got fairly good results. However you can upload up to 248 to tweak the algorithm even more.
- Info and delete requests do what they say on the tin
- Tain Model -  once you have added all the people you need and provided at least one image for each person - you can train the algorithm. To check if the training is finised use the Status Get request.
- Finally we can try and do our first test. Which is a two step process. 
	- First the algorism needs to "find" the face in the image. Second it need to identify the face to a person in your person group.
	- Detect face from Image - upload the image here. This will create a resonse with a faceID
	- Provide this faceID to the Identify API - no need for the image again. The ID refers to a set of vectors stored on the Azure servers. -> The result will be the personID and the confidence value. This tells you how likely it identified the right person (0-1)

## Look who's there
### Adding things to Openhab

*Prerequisits: Python 2.7 must be set up and running, the computer needs to be able to connect to the internet, an image with a face needs to be placed in a location where the script can access it.*

This little python script (detect.py) does all the required steps for you:
It uploads the image to analyze to azure and then triggers the identification process. 
1. you will need to update the code and provide:
- Your "key 1" as Ocp-Apim-Subscription-Key
- The path to your image.
- The presonGroupID. 
- Your Datacenter location url
- I have marked the required variables with TODO. As I did not create an individual variable for each of them.

I am no programmer so my code is lousy… feel free to improve it. One thing I would immediately see as an improvement is loading the image directly from the source (e.g. camera) without persisting it on the local disc first.

2. Try and run the script. If everything runs ok, you should get a single resonse: Your personID.
3. Make sure you have the exec binding installed on you OH Instance.
4. Make sure you have a test image in the specified location
5. Create a little rule that triggers the script
```
rule "faceRecognition"
	when Item testSwitch received command ON
	then
		var String person = executeCommandLine("/opt/openhab2/conf/scripts/detect.py", 5000)
		logInfo("Azure","I can see " +person)	
	end
```
6. From here we have countless possibilites. The first would be to map the ID to a name. The second to write a rule that triggers the OH to store the camera image and start the recognition process. Then to act according to the detected person. E.g. release the hounds if the in-laws approaching...
