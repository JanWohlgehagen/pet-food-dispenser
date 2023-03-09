import datetime
import paho.mqtt.client as mqtt
from datetime import timedelta



from FoodDispenserRepository import FoodDispenserRepository


class Mqtt:
    mqttc = mqtt.Client()

    repository = FoodDispenserRepository()

    pastDateMorning = datetime.datetime.utcnow() - timedelta(days=1)
    pastDateEvening = datetime.datetime.utcnow() - timedelta(days=1)

    def __init__(self):
        print("Hej")
        myhost = "mqtt.flespi.io"
        self.mqttc.on_message = self.on_message
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_publish = self.on_publish
        self.mqttc.on_subscribe = self.on_subscribe
        self.mqttc.username_pw_set("COjYLNDRgB04mkyUpvhqPdhgGW2qfnkHZttz6Wgal55xftgvMlJqoPuVBn9Gyjdn", "password")
        self.mqttc.connect(myhost, 1883)
        self.mqttc.subscribe("Dispenser/1/request")
        self.mqttc.loop_forever()
        print("farvel")


    #This happens when connecting
    def on_connect(self, this, obj, flags, rc):
        print("rc: " + str(rc))

    # Getting a message from subscribe
    def on_message(self, this, obj, msg):
        if self.checkTime():
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

    def checkTime(self) -> bool:
        earlyTime = 8
        lateTime = 18

        # check if it is past the first time of day to dispense food
        if datetime.datetime.now().hour >= lateTime:
            diff = datetime.datetime.utcnow() - Mqtt.pastDateEvening
            # check if food was dispensed today
            if diff.days != 0:
                Mqtt.pastDateEvening = datetime.datetime.utcnow()
                self.repository.saveData(Mqtt.pastDateMorning)
                return True

        # check if it is past the first time of day to dispense food
        if datetime.datetime.now().hour >= earlyTime:
            diff = datetime.datetime.utcnow() - Mqtt.pastDateMorning
            # check if food was dispensed today
            if diff.days != 0:
                Mqtt.pastDateMorning = datetime.datetime.utcnow()
                self.repository.saveData(Mqtt.pastDateMorning)
                return True

        return False


