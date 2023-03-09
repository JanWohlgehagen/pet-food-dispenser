import MQTT
from FoodDispenserRepository import FoodDispenserRepository


def run():
    FoodDispenserRepository().EnsureCreated()
    MQTT.Mqtt()

if __name__ == "__main__":
    run()
