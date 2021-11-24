import json
import boto3
import random
import requests
from chalice import Chalice

app = Chalice(app_name='DialogFlow-Test')
#app.debug = True

@app.route('/')
def index():
  return '{"message":"Hello World!"}'

@app.route('/webhook',methods=['POST'])
def index():
      
   #Uncomment below to provide a simple hard coded reply.
  #  temperature = str(random.randint(-20,35))
  #  reply = '{"fulfillmentMessages": [ {"text": {"text": ["The temperature is ' +temperature +'C"] } } ]}'

  #Get the geo-city value from as sent by Dialogflow
    body = app.current_request.json_body
    city = body['queryResult']['parameters']['geo-city']
    
  #Step 1 find the WOEID of the geo-city. If multiple found use the first one.
    api_url='https://www.metaweather.com/api/location/search/?query=' + str(city)
    headers = {'Content-Type': 'application/json'}
    response = requests.get(api_url, headers=headers)
    r=response.json()
    woeid = str(r[0]["woeid"])

  #Step 2 Use the WOEID to find the current weather conditions for the city.
    api_url='https://www.metaweather.com/api/location/' + woeid
    headers = {'Content-Type': 'application/json'}
    response = requests.get(api_url, headers=headers)
  #Step 3 extract weather data
    r= response.json()
    city = str(r["title"])
    parent = str(r["parent"]["title"])
    weather = str(r["consolidated_weather"][0]["weather_state_name"])
    temp = int(r["consolidated_weather"][0]["the_temp"])
    humidity = str(r["consolidated_weather"][0]["humidity"])
    # #Step 3 build the reply for Dialogflow.
    reply = '{"fulfillmentMessages": [ {"text": {"text": ["Currently, in '+ city + ', '+ parent + ' it is ' + str(temp) + ' degrees C and ' + weather + '"] } } ]}'
    return reply