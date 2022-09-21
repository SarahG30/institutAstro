from atcore import *
from datetime import datetime
import time


def main():
    sdk3 = ATCore()
    hndl = sdk3.open(0)
    crt_temp = round(sdk3.get_float(hndl, "SensorTemperature"), 2)
    print("The current temperature is ", crt_temp, ".")
    targ_temp = float(input("Enter target temperature: "))

    sdk3.set_float(hndl, "TargetSensorTemperature", targ_temp)
    while abs(crt_temp - targ_temp) >= 0.1:
        time.clock()
        elapsed = 0
        start = time.time()
        message = "The camera has reached "
        while elapsed < 60:
            elapsed = time.time() - start
            new_temp = round(sdk3.get_float(hndl, "SensorTemperature"), 2)
            if round(elapsed) % 10 == 0 and round(elapsed) / 10 != 0:
                print(message, new_temp, " degrees.")
                #print(round(elapsed, 2))
                if abs(new_temp - targ_temp) <= 0.5:
                    sdk3.set_float(hndl, "TargetSensorTemperature", new_temp)
                    time.sleep(15)
                    print("The camera has reached target temperature.")
                    print(new_temp)
                    return 0
            time.sleep(1)
            if abs(new_temp - crt_temp) >= 5:
                sdk3.set_float(hndl, "TargetSensorTemperature", new_temp)
                crt_temp = new_temp
                message = "The camera stays at "
        crt_temp = new_temp



main()