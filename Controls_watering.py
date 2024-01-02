# from awscrt import io, mqtt, auth, http
# from awsiot import mqtt_connection_builder

import pymodbus.client as ModbusClient

from pymodbus.transaction import ModbusRtuFramer

import time
import json

from pytz import timezone


#Message demo 
msg = {'P1': 60, 'P2': 30, 'P3': 50, 'V1': 20, 'V2': 40}


# Control motor and solenoid valve
def control_relay(client,msg):
    P1= msg['P1']       # Thoi gian bat may bom vao thung tron
    P2= msg['P2']       # Thoi gian bat may bom tuoi nho giot
    P3= msg['P3']       # Thoi gian bat may bom tuoi phun suong
    V1= msg['V1']       # Thoi gian bat van dien tu thung dinh duong
    V2= msg['V2']       # Thoi gian bat van dien tu thung nuoc
    
    # ON Valve 1 (Van thung dinh duong)
    client.write_coil(0x00,0xFF,0x01)   # add_device=01 05 00 add_relay=00 value=FF 00 CRC
    print("On Valve 1")
    # ON Pump 1 (May bom vao thung tron)
    client.write_coil(0x02,0xFF,0x01)   # 01 05 00 02 FF 00 CRC
    print("On Pump 1")
    
    time.sleep(V1)
    
    # ON Valve 2 (Van thung nuoc)
    client.write_coil(0x01,0xFF,0x01)   # 01 05 00 01 FF 00 CRC
    print("On Valve 2")
    # OFF Valve 1
    client.write_coil(0x00,0x00,0x01)   # 01 05 00 00 00 00 CRC
    print("Off Valve 1")
    
    time.sleep(V2)
    
    # OFF Pump 1
    client.write_coil(0x02,0x00,0x01)   # 01 05 00 02 00 00 CRC
    print("Off Pump 1")
    # OFF Valve 2
    client.write_coil(0x01,0x00,0x01)   # 01 05 00 01 00 00 CRC
    print("Off Valve 2")
    # ON Pump 2 (May bom tuoi nho giot)
    client.write_coil(0x03,0xFF,0x01)   # 01 05 00 03 FF 00 CRC
    print("On Pump 2")
    
    time.sleep(P2)
    
    # OFF Pump 2
    client.write_coil(0x03,0x00,0x01)   # 01 05 00 03 00 00 CRC
    print("Off Pump 2")
    
    # ON Pump 3 (May bom phun suong)
    if not P2 == 0:
        client.write_coil(0x04,0xFF,0x01)   # 01 05 00 04 FF 00 CRC
        print("On Pump 3")
        time.sleep(P2)
        client.write_coil(0x04,0x00,0x01)   # 01 05 00 04 00 00 CRC
        print("Off Pump 3")
 
# Demo program
# Connect to POE ETH Relay
client = ModbusClient.ModbusTcpClient(host= '192.168.1.204' , 
                                          port= 12345, 
                                          framer= ModbusRtuFramer,
                                          baudrate=9600,
                                          bytesize=8,
                                          parity="N",
                                          stopbits=1,
                                          errorcheck="crc",
                                          )
connection = client.connect()
print(f"connection: {connection}")

while True:
    try:
        print(time.asctime(time.localtime(time.time())))
        control_relay(client,msg)
        print(time.asctime(time.localtime(time.time())))
        print(' ')
        time.sleep(60)
        
    except Exception as error:
        print("An error occurred:", type(error).__name__, "–", error)
        client.close()


# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
"""
ENDPOINT = "atqszz8y7vuob-ats.iot.ap-northeast-1.amazonaws.com"
CLIENT_ID = "Gateway_Pi"
PATH_TO_CERTIFICATE = "/home/pi/Downloads/KeyAWS/4cefbe72d270667f0397824c535c05a0d968b14e8b67fd715a44f6b22b888115-certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "/home/pi/Downloads/KeyAWS/4cefbe72d270667f0397824c535c05a0d968b14e8b67fd715a44f6b22b888115-private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "/home/pi/Downloads/KeyAWS/AmazonRootCA1.pem"
topic = "django/request
"""

# Received message from topic "django/request" on AWS IoT Core and using that control relay
"""def on_message_received(topic, payload, **kwargs):
    print("Received message from topic '{}': '{}'".format(topic, payload))
    msg= json.loads(payload.decode("utf-8"))
    print(msg)
    print(type(msg))
    control_relay(msg)"""
    
    
# Spin up resources
"""event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6
            )
print("Connecting to {} with client ID '{}'...".format(ENDPOINT, CLIENT_ID))"""

# Main program

# Make the connect() call
"""connect_future = mqtt_connection.connect()"""
# Future.result() waits until a result is available
"""connect_future.result()"""
print("Connected!")
# Subcribe topic "django/request"
"""mqtt_connection.subscribe(topic,qos=mqtt.QoS.AT_LEAST_ONCE,callback=on_message_received)

received_all_event.wait()
disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()"""