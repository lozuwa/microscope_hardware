# MQTT library 
import paho.mqtt.client as mqtt
# Other libraries 
import numpy as np

# Subscribe topics 
def on_connect(client, userdata, rc):
	print("Connected with result code " + str(rc))
	client.subscribe("/test")

# Reply messages 
def on_message(client, userdata, msg):
	if msg.topic == "/test":
		print(msg.payload)
		print(type(msg.payload))

if __name__ == '__main__':
	client = mqtt.Client()
	client.connect('test.mosquitto.org', 1883, 60)
	#client.connect('192.168.43.209', 1883, 60)
	client.on_connect = on_connect
	client.on_message = on_message
	client.loop_forever()
