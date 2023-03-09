import paho.mqtt.client as mqtt

import TimeScheduler


class Mqtt:
    mqttc = mqtt.Client()
    timeScheduler = TimeScheduler.timeScheduler()

    def __init__(self):
        myhost = "mqtt.flespi.io"
        self.mqttc.on_message = self.on_message
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_publish = self.on_publish
        self.mqttc.on_subscribe = self.on_subscribe
        self.mqttc.username_pw_set("COjYLNDRgB04mkyUpvhqPdhgGW2qfnkHZttz6Wgal55xftgvMlJqoPuVBn9Gyjdn", "password")
        self.mqttc.connect(myhost, 1883)
        self.mqttc.subscribe("Dispenser/1/request")
        self.mqttc.loop_forever()


    #This happens when connecting
    def on_connect(self, this, obj, flags, rc):
        print("rc: " + str(rc))

    # Getting a message from subscribe
    def on_message(self, this, obj, msg):
        if self.timeScheduler.checkTime():
            self.mqttc.publish("Dispenser/1/response", "Food")

    # When something is published
    def on_publish(self, mqttc, obj, mid):
        print("mid: " + str(mid))

    # On subscribing to messages
    def on_subscribe(self, this, obj, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    # Taking care of logging
    def on_log(self, mqttc, obj, level, string):
        print(string)


