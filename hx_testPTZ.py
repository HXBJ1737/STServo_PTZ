# hx_test.py
from STservo_sdk import *
import _hx_PTZ as hx_PTZ
import _PTZ_data as data


ptz = hx_PTZ.PTZ(v_id=data.PTZ1["v_id"], h_id=data.PTZ1["h_id"], 
                 v_pos_range=data.PTZ1["v_pos_range"], h_pos_range=data.PTZ1["h_pos_range"],
                 v_speed=2400, h_speed=2400, v_acc=50, h_acc=50, baudrate=1_000_000, com_port='COM16')
vPos_list = [ptz.v_min, ptz.v_mid, ptz.v_max, ptz.v_mid,
             ptz.KEEP,  ptz.KEEP,  ptz.KEEP,  ptz.KEEP]
hPos_list = [ptz.KEEP,  ptz.KEEP,  ptz.KEEP,  ptz.KEEP,
             ptz.h_min, ptz.h_mid, ptz.h_max, ptz.h_mid]
ptz.set_pos(ptz.v_mid, ptz.h_mid)
time.sleep(0.5)
for v_pos, h_pos in zip(vPos_list, hPos_list):
    print("set pos: V=%d, H=%d" % (v_pos, h_pos))
    ptz.set_pos(v_pos, h_pos)
    while True:
        v_pos, h_pos, _, _ = ptz.get_pos_speed()
        print("pre-pos: V=%d, H=%d" % (v_pos, h_pos))
        v_moving, h_moving = ptz.get_moving()
        if not v_moving and not h_moving:
            break
    time.sleep(0.5)
ptz.close()
print("PTZ closed")
