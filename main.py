import datetime
from datetime import timedelta



import MQTT
from FoodDispenserRepository import FoodDispenserRepository

pastDateMorning = datetime.datetime.utcnow() - timedelta(days=1)
pastDateEvening = datetime.datetime.utcnow() - timedelta(days=1)
earlyTime = 8
lateTime = 18

repository = FoodDispenserRepository

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
    MQTT.Mqtt()


   # repository.EnsureDBTable()


if __name__ == "__main__":
    run()
