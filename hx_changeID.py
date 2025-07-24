# hx_changeID.py
from STservo_sdk import *
import hx_PTZ
'''
请保证控制板仅连接一个总线舵机
'''
ptz = hx_PTZ.PTZ(baudrate=1_000_000, com_port='COM13')
try:
    ptz.change_id(old_id=1, new_id=2)
except Exception as e:
    print(e)