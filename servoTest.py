from ServoManager import ServoManager
import time

p = int(input("Physical Pin: "))
a = int(input("Angle: "))
t = int(input("Time: "))

servo = ServoManager(servoPin=p, startAngle=a)
try: time.sleep(t)
except: pass
servo.close()
