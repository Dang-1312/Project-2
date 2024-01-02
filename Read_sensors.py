import time
import datetime
import json
import psycopg2


import pymodbus.client as ModbusClient
from pymodbus.transaction import ModbusRtuFramer
from pymodbus import pymodbus_apply_logging_config

# import my files
import WD5
import MQTT_publish

# Ham in ra time now
def time_now():
    d = datetime.datetime.now()
    print(d.strftime('%Y/%m/%d %H:%M:%S'))
    
# Ham doc gui lenh de sensors do va phan hoi cac thong so
def read_sensor_rtu(client,register_address,num_registers,slave_address):
    response = client.read_holding_registers(register_address,num_registers,slave_address)
    list_data = []    
    if not response.isError():
        list_data = response.registers
    else:
        print("Error reading registers:", response)
        time.sleep(1)
        
        list_data = read_sensor_rtu(client,register_address,num_registers,slave_address)
        
        # if num_registers == 0x01:
        #     time.sleep(1)
        #     list_data = [0]
        # else:
        #     time.sleep(1)
        #     list_data = [0,0]
            
    client.close()
    
    return list_data
 

# Khai bao thong so va connect voi cac sensors

# Atmospheric sensor RK330-01
ip_1 = "192.168.1.201"
port_1 = 12345
register_address_1 = 0x00
num_registers_1 = 0x02
slave_address_1 = 0x01

client_1 = ModbusClient.ModbusTcpClient(host= ip_1 , 
                                        port= port_1, 
                                        framer= ModbusRtuFramer,
                                        baudrate=9600,
                                        bytesize=8,
                                        parity="N",
                                        stopbits=1,
                                        errorcheck="crc",
                                        )
connection_1 = client_1.connect()
print(f"connection: {connection_1}, {ip_1}")


# CO2 sensor RK300-03
ip_2 = "192.168.1.202"
port_2 = 12345
register_address_2 = 0x00
num_registers_2 = 0x01
slave_address_2 = 0x01

client_2 = ModbusClient.ModbusTcpClient(host= ip_2 , 
                                        port= port_2, 
                                        framer= ModbusRtuFramer,
                                        baudrate=9600,
                                        bytesize=8,
                                        parity="N",
                                        stopbits=1,
                                        errorcheck="crc",
                                        )
connection_2 = client_2.connect()
print(f"connection: {connection_2}, {ip_2}")


# pH sensor RK500-02
ip_3 = "192.168.1.203"
port_3 = 12345
register_address_3 = 0x00
num_registers_3 = 0x01
slave_address_3 = 0x01

client_3 = ModbusClient.ModbusTcpClient(host= ip_3 , 
                                        port= port_3, 
                                        framer= ModbusRtuFramer,
                                        baudrate=9600,
                                        bytesize=8,
                                        parity="N",
                                        stopbits=1,
                                        errorcheck="crc",
                                        )
connection_3 = client_3.connect()
print(f"connection: {connection_3}, {ip_3}")


# Main loop program
while True:
    time_now()
    
    # Measure sensors
    # Measure Atmospheric sensor RK330-01
    Atmostpheric_data = read_sensor_rtu(client_1,register_address_1,num_registers_1,slave_address_1)
    Temperature_Air = Atmostpheric_data[0]/10
    Humidity_Air = Atmostpheric_data[1]/10
    time.sleep(1)
    
    # Measure CO2 sensor RK300-03
    CO2 = read_sensor_rtu(client_2,register_address_2,num_registers_2,slave_address_2)[0]
    time.sleep(1)
    
    # Measure pH sensor RK500-02
    pH = read_sensor_rtu(client_3,register_address_3,num_registers_3,slave_address_3)[0] /100
    time.sleep(1)
    
    # Measure moisture sensor WD5
    data_wd5 = WD5.main_read()
    Vol = data_wd5[0]
    EC = data_wd5[1]
    Temp = data_wd5[2]
    
    # Check ERROR Data and Remeasure
    
        
    # Build message for publish to cloud
    message = {
                "Temp_air": Temperature_Air,
                "Hum_air": Humidity_Air,
                "CO2": CO2,
                "pH": pH,
                "Moisture_soil": Vol,
                "EC": EC,
                "Temperature_soil": Temp,
            }
    print(message)
    
    time_now()
    
    MQTT_publish.publish_data(message)
    
    time_now()
    
    time.sleep(300)