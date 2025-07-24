# hx_test.py
from STservo_sdk import *
import hx_PTZ


ptz = hx_PTZ.PTZ(v_id=1, h_id=2, v_pos_range=(1000, 3000), h_pos_range=(0, 1800), v_speed=2400, h_speed=2400, v_acc=50, h_acc=50, baudrate=1_000_000, com_port='COM13')

ptz.set_pos(ptz.v_min, ptz.h_min)
while True:
    time.sleep(0.5)
    ptz.add_pos(v_add=0, h_add=100)
    h_pos, _ = ptz.get_h_pos_speed()
    if h_pos >= ptz.h_max:
        break
    while True:
        v_pos, h_pos, v_speed, h_speed = ptz.get_pos_speed()
        print("pre-pos: V=%d, H=%d" % (v_pos, h_pos))

        v_moving, h_moving = ptz.get_moving()
        if not v_moving and not h_moving:
            break
ptz.close()
