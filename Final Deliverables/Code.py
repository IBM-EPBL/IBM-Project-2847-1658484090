import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
#Provide your IBM Watson Device Credentials
organization = "pq685h"
deviceType = "NodeMCU"
deviceId = "12345"
authMethod = "token"
authToken = "12345678"
# Initialize GPIO
def myCommandCallback(cmd):
 print("Command received: %s" % cmd.data['command'])
 status=cmd.data['command']
 if status=="alarmon":
  print ("Alarm is on")
 else:
  print ("Alarm is off")

 #print(cmd)


try:
    deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method":
                     authMethod, "auth-token": authToken}
    deviceCli = ibmiotf.device.Client(deviceOptions)
#..............................................
except Exception as e:
    print("Caught exception connecting device: %s" % str(e))
    sys.exit()
# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type"greeting" 10 times
deviceCli.connect()
while True:
 #Get Sensor Data from DHT11

 temp=random.randint(-20,125)
 Humid=random.randint(0,100)
 Gas=random.randint(0,1000);
 Flame=random.randint(200,1024);
 flame1 = random.randint(0,1)
 if flame1==0:
     flame_status = "No Fire"
     sprinkler_status="Not Working"
 else:
     flame_status = "Fire is Detected"
     sprinkler_status="Working"
 if Gas > 100:
     Gas_status="Gas Leakage is Detected"
     Exhaust_fan="Working"
 else:
     Gas_status="No Gas Leakage is Detected"
     Exhaust_fan="Not Working"

 data = { 'temp' : temp, 'Humid': Humid , 'Gas':Gas , 'Flame':Flame , 'flame_status':flame_status, 'sprinkler_status':sprinkler_status, 'Gas_status':Gas_status, 'Exhaust_fan':Exhaust_fan}
 #print data
 def myOnPublishCallback():
     print (" Temperature = %s C\n" % temp,"Gas = %s %%\n" % Gas ,"Humidity = %s %%\n" % Humid,"Flame = %s\n"%Flame,"Fire Status = %s\n"%flame_status,"Sprinkler_Status = %s\n"%sprinkler_status,"Gas_Status = %s\n"%Gas_status,"Exhaust_fan = %s\n"%Exhaust_fan)
 success = deviceCli.publishEvent("IoTSensor", "json", data, qos=0,
on_publish=myOnPublishCallback)
 time.sleep(10)
 if not success:
  print("Not connected to IoTF")
  time.sleep(10)

 deviceCli.commandCallback = myCommandCallback
# Disconnect the device and application from the cloud
deviceCli.disconnect()
