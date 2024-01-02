import time
# from paho.mqtt import client as mqtt_client
import paho.mqtt.publish as publish
# import psutil
import string

# Channel ID.
channel_ID = "2193827"

# API Key write
apiKey = "***************"

useUnsecuredTCP = False

useUnsecuredWebsockets = False

useSSLWebsockets = True

# The hostname of the ThingSpeak MQTT broker.
mqtt_host = "mqtt3.thingspeak.com"

# Your MQTT credentials for the device
mqtt_client_ID = "***********************"
mqtt_username  = "***********************"
mqtt_password  = "**************************"

tTransport = "websockets"
tPort = 80

# Create the topic string.
topic = "channels/" + channel_ID + "/publish"

def publish_data(data):
            
    # Creat data
    temp_air = data["Temp_air"]
    hum_air = data["Hum_air"]
    co2 = data["CO2"]
    pH = data["pH"]
    mois_soil = data["Moisture_soil"]
    ec = data["EC"]
    temp_soil = data["Temperature_soil"]
    
    tPayload = "field1=" + str(temp_air) + "&field2=" + str(hum_air) + "&field3=" + str(co2) + "&field4=" + str(pH) + "&field5=" + str(mois_soil) + "&field6=" + str(ec) + "&field7=" + str(temp_soil)
    print(tPayload)
    
    try:
        publish.single(topic, payload=tPayload, hostname=mqtt_host, transport=tTransport, port=tPort, client_id=mqtt_client_ID, auth={'username':mqtt_username,'password':mqtt_password})

    except (KeyboardInterrupt):
        print("Measurement has been cancelled.")
        return

    except:
        print ("There was an error while publishing the data.")
        return
