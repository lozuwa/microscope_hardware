# MQTT
import paho.mqtt.client as mqtt

# Subscribe topics
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Microscope hardware
    client.subscribe("/connect")

# Reply messages
def on_message(client, userdata, msg):
    print(msg.topic, msg.payload)

if __name__ == "__main__":
    client = mqtt.Client()
    client.connect("192.168.3.193", 1883, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()
