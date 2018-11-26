import urllib.request, json 

HueIP = "192.168.1.x"
HueKey = "KEY"

ThingSpeakKey = "KEY"

Sensors=[16,21,37,50]

def GetLightLevels(SensorIDs):
#    print("Inside GetLightLevels")
    GetSensorURL="http://"+HueIP+"/api/"+HueKey+"/sensors/"
    LightLevelReadings=[0]*len(SensorIDs)
    
    for sensor in range (len(SensorIDs)):
        with urllib.request.urlopen(GetSensorURL+str(Sensors[sensor])) as url:
            data = json.loads(url.read().decode('utf-8'))
            LightLevelReadings[sensor]=(data['state']['lightlevel'])
  
    return LightLevelReadings


def UpdateThingSpeak(Measurements):
#    print("Inside UpdateThingSpeak")
    postStr ="https://api.thingspeak.com/update?api_key="+ThingSpeakKey+"&field1="+str(Measurements[2])+"&field2="+str(Measurements[0])+"&field3="+str(Measurements[1])+"&field4="+str(Measurements[3])
    f = urllib.request.urlopen(postStr)
   
UpdateThingSpeak(GetLightLevels(Sensors))    
