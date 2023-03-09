import datetime
from datetime import timedelta

import paho.mqtt.client as mqtt

from FoodDispenserRepository import FoodDispenserRepository

pastDateMorning = datetime.datetime.utcnow() - timedelta(days=1)
pastDateEvening = datetime.datetime.utcnow() - timedelta(days=1)
earlyTime = 8
lateTime = 18

mqttc = mqtt.Client()
repository = FoodDispenserRepository

# This happens when connecting
def on_connect(self, obj, flags, rc):
    print("rc: " + str(rc))


# Getting a message from subscribe
def on_message(self, obj, msg):
    if checkTime():
        GiveFood()


# When something is published
def on_publish(self, mqttc, obj, mid):
    print("mid: " + str(mid))


# On subscribing to messages
def on_subscribe(self, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


# Taking care of logging
def on_log(self, mqttc, obj, level, string):
    print(string)


def checkTime() -> bool:
    global pastDateMorning
    global pastDateEvening
    global repository

    # check if it is past the first time of day to dispense food
    if datetime.datetime.now().hour >= lateTime:
        diff = datetime.datetime.utcnow() - pastDateEvening
        # check if food was dispensed today
        if diff.days != 0:
            pastDateEvening = datetime.datetime.utcnow()
            repository.saveData(pastDateMorning)
            return True

    # check if it is past the first time of day to dispense food
    if datetime.datetime.now().hour >= earlyTime:
        diff = datetime.datetime.utcnow() - pastDateMorning
        # check if food was dispensed today
        if diff.days != 0:
            pastDateMorning = datetime.datetime.utcnow()
            repository.saveData(pastDateMorning)
            return True

    return False


def GiveFood():
    global mqttc
    mqttc.publish("Dispenser/1/response", "Food")


def run():
    global repository
    global mqttc


    myhost = "mqtt.flespi.io"
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    mqttc.username_pw_set("COjYLNDRgB04mkyUpvhqPdhgGW2qfnkHZttz6Wgal55xftgvMlJqoPuVBn9Gyjdn", "password")
    mqttc.connect(myhost, 1883)
    mqttc.subscribe("Dispenser/1/request")
    mqttc.loop_forever()

   # repository.EnsureDBTable()


if __name__ == "__main__":
    run()
