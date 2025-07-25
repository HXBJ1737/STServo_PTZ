# hx_changeID.py
from STservo_sdk import *
from _hx_SERVO import SERVO
'''
请保证控制板仅连接一个总线舵机
'''
servo = SERVO(baudrate=1_000_000, com_port='COM16')
try:
    servo.change_id(old_id=3, new_id=4)
except Exception as e:
    print(e)
