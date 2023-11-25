import json
import time
from paho import mqtt
import paho.mqtt.client as paho
from soil_saturation import sat_per
from datetime import datetime

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set("username", "WErock123")
client.on_connect = on_connect
client.connect("94e50a3aa3a041ddb033aad7d78701cd.s1.eu.hivemq.cloud", 8883)
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

# count = 0

LOCATION = "balcony"
SPECIES = "basil"
ID = "1"

while True:
    moisture = sat_per()
    currentDateAndTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = {
        'id': ID,
        'data': {
            'species': SPECIES,
            'location': LOCATION,
            'moisture': { 
                'currentDateAndTime' : currentDateAndTime,
                'reading': moisture
            }
        }
    }

    json_string = json.dumps(data)
    client.publish("plants", json_string)
    print(f"Published: {json_string}")
    time.sleep(5)