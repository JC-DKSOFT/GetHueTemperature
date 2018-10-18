
import urllib.request, json 

HueIP = "192.168.1.x"
HueKey = "KEY"

ThingSpeakKey = "KEY"

Sensors=[14,19,35,48]
SensorOffsets=[-0.6875, 0.03249999999999886, 0.12249999999999872, 0.5324999999999989]

SensorNames=['Køkken sensor','Gang sensor','Bryggers sensor','Kontor sensor']

def GetTemperatures(SensorIDs):
    
    GetSensorURL="http://"+HueIP+"/api/"+HueKey+"/sensors/"
    TemperatureReadings=[0]*len(SensorIDs)
    
    for sensor in range (len(SensorIDs)):
        with urllib.request.urlopen(GetSensorURL+str(Sensors[sensor])) as url:
            data = json.loads(url.read().decode('utf-8'))
            TemperatureReadings[sensor]=(data['state']['temperature']/100)
  
    return TemperatureReadings


def UpdateThingSpeak(Measurements):
    postStr ="https://api.thingspeak.com/update?api_key="+ThingSpeakKey+"&field1="+str(Measurements[2])+"&field2="+str(Measurements[0])+"&field3="+str(Measurements[1])+"&field4="+str(Measurements[3])
    f = urllib.request.urlopen(postStr)
   

def PerformOffsetAdjustments(SensorReadings,SensorOffsets):
    CorrectedMeasurement=[0]*len(SensorReadings)

    for Measurement in range(len(SensorReadings)):
        CorrectedMeasurement[Measurement]=SensorReadings[Measurement]+SensorOffsets[Measurement]

    return CorrectedMeasurement

def CalculateOffsets(SensorReadings):
    TempSum=0
    
    for Reading in SensorReadings:
        TempSum+=Reading
    
    #Create list with correct dimensions for sensor offsets
    NewSensorOffsets=[0] *len(SensorReadings)

    for sensor in range(len(SensorReadings)):
        NewSensorOffsets[sensor]=(TempSum/len(SensorReadings))-SensorReadings[sensor]

    return NewSensorOffsets
    
UpdateThingSpeak(PerformOffsetAdjustments(GetTemperatures(Sensors),SensorOffsets))    
