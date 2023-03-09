from datetime import timedelta
import datetime
from FoodDispenserRepository import FoodDispenserRepository


class timeScheduler:

    repository = FoodDispenserRepository()

    pastDateMorning = datetime.datetime.utcnow() - timedelta(days=1)
    pastDateEvening = datetime.datetime.utcnow() - timedelta(days=1)

    def checkTime(self) -> bool:
        earlyTime = 8
        lateTime = 18

        # check if it is past the first time of day to dispense food
        if datetime.datetime.now().hour >= lateTime:
            diff = datetime.datetime.utcnow() - self.pastDateEvening + timedelta(hours=1)
            # check if food was dispensed today
            if diff.days != 0:
                self.pastDateEvening = datetime.datetime.utcnow() + timedelta(hours=1)
                self.repository.saveData(self.pastDateMorning)
                return True

        # check if it is past the first time of day to dispense food
        if datetime.datetime.now().hour >= earlyTime:
            diff = datetime.datetime.utcnow() - self.pastDateMorning + timedelta(hours=1)
            # check if food was dispensed today
            if diff.days != 0:
                self.pastDateMorning = datetime.datetime.utcnow() + timedelta(hours=1)
                self.repository.saveData(self.pastDateMorning)
                return True

        return False