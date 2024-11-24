import sys
import ac
import acsys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib'))

ac.log(sys.path[-1])

from siminfo import info

UPDATE_RATE_HZ = 20
lastUpdateTime = 0
tracker = None # type: Optional["LapTracker"]


def format_time(time_ms):
    minutes = int(time_ms / 60000)
    seconds = int((time_ms % 60000) / 1000)
    millis = int(time_ms % 1000)
    return "%d:%d.%d" % (minutes, seconds, millis)


def acMain(ac_version):
    ac.log("LuumuLaps init")
    app_window = ac.newApp("LuumuLaps")
    ac.setSize(app_window, 200, 200)

    global tracker
    tracker = LapTracker()

    ac.log("LuumuLaps started")
    return "LuumuLaps"


def acUpdate(deltaT):
    try:
        global lastUpdateTime
        lastUpdateTime += deltaT

        if lastUpdateTime < float(1)/UPDATE_RATE_HZ:
            return

        lastUpdateTime = 0
        tracker.update()

    except Exception as e:
        ac.log("MultiLaps: Error in acUpdate: %s" % e)


class LapTracker():
    def __init__(self):
        self.laps_registered = 0

    def update(self):
        current_time = ac.getCarState(0, acsys.CS.LapTime)
        laps_done = ac.getCarState(0, acsys.CS.LapCount)

        # Apparently it takes a bit of time for the lap time to be updated
        ac.console("%d" % current_time)
        if laps_done > self.laps_registered and current_time > 100:
            self.new_lap()


        #ac.log("currentTime: %s - lap done: %d - last lap: %s" % (format_time(current_time), laps_done, format_time(last_lap_time)))

    def new_lap(self):
        last_lap_time = info.graphics.iLastTime
        self.laps_registered += 1

        ac.log("New lap! Lap %d - last lap: %s" % (self.laps_registered, format_time(last_lap_time)))
